from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class DomaineFormation(models.Model):
    """Domaine de formation (ex: Informatique, Langues, Gestion, etc.)"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, blank=True, null=True, help_text="Classe d'icône (ex: fa-laptop-code)")
    couleur = models.CharField(max_length=20, default='#3498db', help_text="Code couleur hexadécimal")
    ordre_affichage = models.PositiveSmallIntegerField(default=0)
    est_actif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['ordre_affichage', 'nom']
        verbose_name = "Domaine de formation"
        verbose_name_plural = "Domaines de formation"


class Formation(models.Model):
    """Formation proposée par l'établissement"""
    TYPE_FORMATION = [
        ('presentiel', 'Présentiel'),
        ('distanciel', 'Distanciel'),
        ('hybride', 'Hybride'),
    ]
    
    NIVEAU = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    reference = models.CharField(max_length=20, unique=True)
    intitule = models.CharField(max_length=200)
    domaine = models.ForeignKey(DomaineFormation, on_delete=models.PROTECT, related_name='formations')
    type_formation = models.CharField(max_length=20, choices=TYPE_FORMATION, default='presentiel')
    niveau = models.CharField(max_length=20, choices=NIVEAU, default='debutant')
    duree_heures = models.PositiveIntegerField(help_text="Durée totale en heures")
    duree_mois = models.PositiveSmallIntegerField(help_text="Durée en mois")
    
    # Description détaillée
    objectifs = models.TextField(help_text="Objectifs pédagogiques")
    programme = models.TextField(help_text="Détail du programme")
    prerequis = models.TextField(blank=True, null=True, help_text="Prérequis pour suivre la formation")
    public_cible = models.TextField(blank=True, null=True, help_text="Public cible")
    
    # Informations pratiques
    lieu = models.TextField(blank=True, null=True)
    horaires = models.CharField(max_length=200, blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    
    # Tarification
    prix_ht = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=20, help_text="TVA en pourcentage")
    prix_ttc = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Options de paiement
    paiement_echelonne = models.BooleanField(default=False)
    nombre_tranches = models.PositiveSmallIntegerField(default=1, help_text="Nombre de tranches de paiement")
    
    # Visibilité et statut
    est_certifiante = models.BooleanField(default=False)
    certification = models.CharField(max_length=200, blank=True, null=True)
    places_disponibles = models.PositiveSmallIntegerField()
    est_public = models.BooleanField(default=True, help_text="Visible sur le site web public")
    est_actif = models.BooleanField(default=True)
    
    # Métadonnées
    image_couverture = models.ImageField(upload_to='formations/couverture/', null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True)
    mots_cles = models.CharField(max_length=250, blank=True, null=True, help_text="Mots-clés pour la recherche, séparés par des virgules")
    
    # Suivi
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculer le prix TTC si nécessaire
        if not self.prix_ttc and self.prix_ht is not None:
            self.prix_ttc = self.prix_ht * (1 + self.tva / 100)
        
        # Générer un slug à partir de l'intitulé si non fourni
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.reference}-{self.intitule}")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference} - {self.intitule}"
    
    @property
    def places_restantes(self):
        return self.places_disponibles - self.inscriptions_actives().count()
    
    def inscriptions_actives(self):
        return self.inscriptions.filter(statut__in=['confirme', 'en_cours', 'termine'])
    
    class Meta:
        ordering = ['domaine', 'niveau', 'intitule']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"


class Module(models.Model):
    """Module d'une formation"""
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='modules')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    duree_heures = models.PositiveIntegerField(help_text="Durée en heures")
    ordre = models.PositiveSmallIntegerField(default=0, help_text="Ordre d'affichage")
    
    # Contenu pédagogique
    objectifs = models.TextField(help_text="Objectifs d'apprentissage")
    contenu = models.TextField(help_text="Contenu détaillé")
    prerequis = models.TextField(blank=True, null=True)
    
    # Ressources
    supports_pedagogiques = models.TextField(blank=True, null=True, help_text="Liens ou références des supports")
    
    def __str__(self):
        return f"{self.formation} - {self.titre}"
    
    class Meta:
        ordering = ['formation', 'ordre', 'titre']
        unique_together = ('formation', 'titre')
        verbose_name = "Module"
        verbose_name_plural = "Modules"


class SessionFormation(models.Model):
    """Session spécifique d'une formation"""
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='sessions')
    reference = models.CharField(max_length=50, unique=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    horaires = models.CharField(max_length=200, help_text="Ex: Lundi et jeudi de 18h à 21h")
    lieu = models.TextField(blank=True, null=True)
    
    # Formateurs
    formateurs = models.ManyToManyField('Enseignant', related_name='sessions_formation')
    
    # Capacité
    places_disponibles = models.PositiveSmallIntegerField()
    
    # Statut
    statut = models.CharField(max_length=20, choices=[
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ], default='planifiee')
    
    # Suivi
    notes = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Générer une référence si vide
        if not self.reference:
            from django.utils import timezone
            annee = timezone.now().year % 100
            dernier_id = SessionFormation.objects.count() + 1
            self.reference = f"SES-{annee}-{self.formation.reference}-{dernier_id:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.formation} - Session du {self.date_debut}"
    
    @property
    def places_restantes(self):
        return self.places_disponibles - self.inscriptions_actives().count()
    
    def inscriptions_actives(self):
        return self.inscriptions.filter(statut__in=['confirme', 'en_cours'])
    
    class Meta:
        ordering = ['date_debut', 'formation']
        verbose_name = "Session de formation"
        verbose_name_plural = "Sessions de formation"


class InscriptionFormation(models.Model):
    """Inscription d'un apprenant à une formation"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
        ('en_cours', 'En cours'),
        ('abandon', 'Abandon'),
        ('termine', 'Terminée'),
    ]
    
    session = models.ForeignKey(SessionFormation, on_delete=models.PROTECT, related_name='inscriptions')
    apprenant = models.ForeignKey('Eleve', on_delete=models.PROTECT, related_name='inscriptions_formation')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Informations complémentaires
    motivation = models.TextField(blank=True, null=True, help_text="Pourquoi souhaitez-vous suivre cette formation ?")
    experience = models.TextField(blank=True, null=True, help_text="Votre expérience dans le domaine")
    attentes = models.TextField(blank=True, null=True, help_text="Vos attentes par rapport à cette formation")
    
    # Paiement
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    solde_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Évaluation
    note_finale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    mention = models.CharField(max_length=50, blank=True, null=True)
    certificat_delivre = models.BooleanField(default=False)
    date_delivrance_certificat = models.DateField(null=True, blank=True)
    
    # Suivi
    notes = models.TextField(blank=True, null=True, help_text="Notes internes")
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculer le solde restant
        self.solde_restant = self.montant_total - self.montant_paye - self.reduction
        
        # Mettre à jour le statut en fonction du paiement
        if self.solde_restant <= 0 and self.statut == 'en_attente':
            self.statut = 'confirme'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.apprenant} - {self.session}"
    
    class Meta:
        unique_together = ('session', 'apprenant')
        ordering = ['-date_inscription']
        verbose_name = "Inscription à une formation"
        verbose_name_plural = "Inscriptions aux formations"


class PaiementFormation(models.Model):
    """Paiement pour une inscription à une formation"""
    MODE_PAIEMENT = [
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('prelevement', 'Prélèvement'),
        ('carte', 'Carte bancaire'),
        ('autre', 'Autre'),
    ]
    
    inscription = models.ForeignKey(InscriptionFormation, on_delete=models.PROTECT, related_name='paiements')
    reference = models.CharField(max_length=50, unique=True)
    date_paiement = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    banque_emetteur = models.CharField(max_length=100, blank=True, null=True)
    
    # Suivi
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    def save(self, *args, **kwargs):
        # Générer une référence si vide
        if not self.reference:
            from django.utils import timezone
            annee = timezone.now().year % 100
            dernier_id = PaiementFormation.objects.count() + 1
            self.reference = f"PAY-FORM-{annee}-{dernier_id:05d}"
        
        super().save(*args, **kwargs)
        
        # Mettre à jour le montant payé sur l'inscription
        inscription = self.inscription
        inscription.montant_paye = sum(p.montant for p in inscription.paiements.all())
        inscription.save()
    
    def __str__(self):
        return f"{self.reference} - {self.inscription.apprenant} - {self.montant} DH"
    
    class Meta:
        ordering = ['-date_paiement', '-created_at']
        verbose_name = "Paiement formation"
        verbose_name_plural = "Paiements formations"
