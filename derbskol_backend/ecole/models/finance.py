from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class FraisScolarite(models.Model):
    """Configuration des frais de scolarité par niveau/classe"""
    TYPE_FRAIS = [
        ('inscription', 'Frais d\'inscription'),
        ('mensualite', 'Mensualité'),
        ('dossier', 'Frais de dossier'),
        ('assurance', 'Assurance scolaire'),
        ('transport', 'Transport scolaire'),
        ('fourniture', 'Fournitures scolaires'),
        ('activite', 'Activités'),
        ('autre', 'Autre'),
    ]
    
    niveau = models.ForeignKey('NiveauScolaire', on_delete=models.CASCADE, null=True, blank=True)
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, null=True, blank=True)
    type_frais = models.CharField(max_length=20, choices=TYPE_FRAIS)
    libelle = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    periodicite = models.CharField(max_length=20, choices=[
        ('unique', 'Paiement unique'),
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('annuel', 'Annuel'),
    ], default='unique')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_type_frais_display()} - {self.libelle} ({self.montant} DH)"
    
    class Meta:
        verbose_name = "Frais de scolarité"
        verbose_name_plural = "Frais de scolarité"


class Facture(models.Model):
    """Facture émise à un élève"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('emise', 'Emise'),
        ('payee', 'Payée'),
        ('en_retard', 'En retard'),
        ('annulee', 'Annulée'),
    ]
    
    reference = models.CharField(max_length=20, unique=True)
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='factures')
    inscription = models.ForeignKey('Inscription', on_delete=models.SET_NULL, null=True, blank=True, related_name='factures')
    date_emission = models.DateField(default=timezone.now)
    date_echeance = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    montant_ht = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    tva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_ttc = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    montant_restant = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True)
    
    # Suivi
    date_paiement = models.DateField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=50, blank=True, null=True)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer une référence unique (ex: FACT-2023-001)
            last_id = Facture.objects.count() + 1
            self.reference = f"FACT-{timezone.now().year}-{last_id:03d}"
        
        # Calculer le montant TTC si nécessaire
        if not self.montant_ttc:
            self.montant_ttc = self.montant_ht + self.tva
        
        # Mettre à jour le statut
        if self.statut == 'payee' and not self.date_paiement:
            self.date_paiement = timezone.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference} - {self.eleve} - {self.montant_ttc} DH"
    
    class Meta:
        ordering = ['-date_emission', 'reference']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"


class LigneFacture(models.Model):
    """Ligne détaillée d'une facture"""
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    libelle = models.CharField(max_length=200)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2)
    tva_taux = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # en pourcentage
    tva_montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Calculer les montants
        self.montant_ht = self.quantite * self.prix_unitaire
        self.tva_montant = (self.montant_ht * self.tva_taux) / 100
        self.montant_ttc = self.montant_ht + self.tva_montant
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.libelle} - {self.quantite} x {self.prix_unitaire} DH"


class Paiement(models.Model):
    """Paiement effectué par un élève"""
    MODE_PAIEMENT = [
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('prelevement', 'Prélèvement'),
        ('carte', 'Carte bancaire'),
        ('autre', 'Autre'),
    ]
    
    reference = models.CharField(max_length=20, unique=True)
    facture = models.ForeignKey(Facture, on_delete=models.PROTECT, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date_paiement = models.DateField(default=timezone.now)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    banque_emetteur = models.CharField(max_length=100, blank=True, null=True)
    date_encaissement = models.DateField(blank=True, null=True)
    encaisse = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer une référence unique (ex: PAI-2023-001)
            last_id = Paiement.objects.count() + 1
            self.reference = f"PAI-{timezone.now().year}-{last_id:05d}"
        
        # Mettre à jour la facture associée
        if self.pk is None:  # Nouveau paiement
            self.facture.montant_restant -= self.montant
            if self.facture.montant_restant <= 0:
                self.facture.statut = 'payee'
            self.facture.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference} - {self.facture.eleve} - {self.montant} DH"
    
    class Meta:
        ordering = ['-date_paiement', '-created_at']
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
