from django.db import models
from django.core.validators import MinValueValidator

class Vehicule(models.Model):
    """Véhicule de transport scolaire"""
    TYPE_VEHICULE = [
        ('bus', 'Bus scolaire'),
        ('minibus', 'Minibus'),
        ('voiture', 'Voiture de service'),
        ('autre', 'Autre'),
    ]
    
    STATUT_VEHICULE = [
        ('en_service', 'En service'),
        ('en_maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
    ]
    
    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    annee = models.PositiveSmallIntegerField()
    capacite = models.PositiveSmallIntegerField(help_text="Nombre maximum de passagers")
    date_mise_en_service = models.DateField()
    date_derniere_revision = models.DateField(blank=True, null=True)
    date_prochaine_revision = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_VEHICULE, default='en_service')
    assurance_numero = models.CharField(max_length=50, blank=True, null=True)
    assurance_expiration = models.DateField(blank=True, null=True)
    controle_technique = models.DateField(blank=True, null=True)
    kilometrage = models.PositiveIntegerField(default=0, help_text="Kilométrage actuel")
    conducteur_attitre = models.ForeignKey('Conducteur', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicules')
    notes = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_type_vehicule_display()} - {self.marque} {self.modele} ({self.immatriculation})"
    
    class Meta:
        ordering = ['type_vehicule', 'marque', 'modele']
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"


class Conducteur(models.Model):
    """Conducteur de véhicule scolaire"""
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='conducteurs/photos/', null=True, blank=True)
    
    # Permis de conduire
    numero_permis = models.CharField(max_length=50)
    categorie_permis = models.CharField(max_length=10)
    date_emission_permis = models.DateField()
    date_expiration_permis = models.DateField()
    
    # Informations professionnelles
    date_embauche = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=[
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ], default='actif')
    
    # Informations complémentaires
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"
    
    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Conducteur"
        verbose_name_plural = "Conducteurs"


class Itineraire(models.Model):
    """Itinéraire de transport scolaire"""
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Points de ramassage
    points_ramassage = models.TextField(help_text="Liste des arrêts, un par ligne")
    
    # Horaires
    heure_depart = models.TimeField()
    heure_retour = models.TimeField()
    
    # Véhicule et conducteur
    vehicule = models.ForeignKey(Vehicule, on_delete=models.SET_NULL, null=True, blank=True, related_name='itineraires')
    conducteur = models.ForeignKey(Conducteur, on_delete=models.SET_NULL, null=True, blank=True, related_name='itineraires')
    
    # Capacité et occupation
    capacite_max = models.PositiveSmallIntegerField()
    
    # Statut
    actif = models.BooleanField(default=True)
    
    # Jours de fonctionnement
    lundi = models.BooleanField(default=True)
    mardi = models.BooleanField(default=True)
    mercredi = models.BooleanField(default=True)
    jeudi = models.BooleanField(default=True)
    vendredi = models.BooleanField(default=True)
    samedi = models.BooleanField(default=False)
    dimanche = models.BooleanField(default=False)
    
    # Tarification
    frais_mensuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def places_disponibles(self):
        return self.capacite_max - self.abonnes_actifs().count()
    
    def abonnes_actifs(self):
        return self.abonnements.filter(statut='actif')
    
    def __str__(self):
        return f"{self.nom} ({self.code}) - {self.heure_depart.strftime('%H:%M')}"
    
    class Meta:
        ordering = ['heure_depart', 'code']
        verbose_name = "Itinéraire"
        verbose_name_plural = "Itinéraires"


class AbonnementTransport(models.Model):
    """Abonnement d'un élève au transport scolaire"""
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('en_attente', 'En attente'),
        ('suspendu', 'Suspendu'),
        ('annule', 'Annulé'),
        ('expire', 'Expiré'),
    ]
    
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='abonnements_transport')
    itineraire = models.ForeignKey(Itineraire, on_delete=models.PROTECT, related_name='abonnements')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    
    # Arrêts spécifiques
    point_embarquement = models.CharField(max_length=200)
    point_debarquement = models.CharField(max_length=200)
    
    # Informations de facturation
    montant_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Suivi
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculer le montant total si nécessaire
        if not self.montant_total:
            self.montant_total = self.montant_mensuel - self.reduction
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.eleve} - {self.itineraire} ({self.get_statut_display()})"
    
    class Meta:
        ordering = ['-date_debut', 'eleve__nom', 'eleve__prenom']
        verbose_name = "Abonnement transport"
        verbose_name_plural = "Abonnements transport"


class TrajetJournalier(models.Model):
    """Suivi des trajets quotidiens"""
    itineraire = models.ForeignKey(Itineraire, on_delete=models.PROTECT, related_name='trajets')
    date = models.DateField()
    heure_depart_reelle = models.TimeField(null=True, blank=True)
    heure_arrivee_reelle = models.TimeField(null=True, blank=True)
    conducteur_remplacement = models.ForeignKey(Conducteur, on_delete=models.SET_NULL, null=True, blank=True, related_name='trajets_remplacement')
    vehicule_remplacement = models.ForeignKey(Vehicule, on_delete=models.SET_NULL, null=True, blank=True, related_name='trajets_remplacement')
    kilometrage_depart = models.PositiveIntegerField(null=True, blank=True)
    kilometrage_arrivee = models.PositiveIntegerField(null=True, blank=True)
    nombre_passagers = models.PositiveSmallIntegerField(default=0)
    incidents = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.itineraire} - {self.date}"
    
    class Meta:
        unique_together = ('itineraire', 'date')
        ordering = ['-date', 'itineraire__heure_depart']
        verbose_name = "Trajet journalier"
        verbose_name_plural = "Trajets journaliers"
