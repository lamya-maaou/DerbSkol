from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Eleve(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='eleves/photos/', null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    nationalite = models.CharField(max_length=50, default='Marocaine')
    nom_pere = models.CharField(max_length=100)
    profession_pere = models.CharField(max_length=100)
    telephone_pere = models.CharField(max_length=20)
    nom_mere = models.CharField(max_length=100)
    profession_mere = models.CharField(max_length=100)
    telephone_mere = models.CharField(max_length=20)
    
    # Informations médicales
    groupe_sanguin = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    maladies_chroniques = models.TextField(blank=True, null=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    date_sortie = models.DateField(null=True, blank=True)
    motif_sortie = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"
    
    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"
        ordering = ['nom', 'prenom']


class Inscription(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='inscriptions')
    annee_scolaire = models.CharField(max_length=9)  # Format: 2024-2025
    date_inscription = models.DateField(auto_now_add=True)
    classe = models.ForeignKey('Classe', on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2)
    frais_scolarite_mensuels = models.DecimalField(max_digits=10, decimal_places=2)
    frais_dossier = models.DecimalField(max_digits=10, decimal_places=2)
    frais_assurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    
    # Informations sur le transport
    utilise_transport = models.BooleanField(default=False)
    itineraire = models.ForeignKey('Itineraire', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Documents
    dossier_complet = models.BooleanField(default=False)
    documents_manquants = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calcul du montant total
        self.montant_total = sum([
            self.frais_inscription,
            self.frais_dossier,
            self.frais_assurance,
            self.frais_transport,
            -self.reduction
        ])
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.eleve} - {self.classe} ({self.annee_scolaire})"
    
    class Meta:
        unique_together = ('eleve', 'annee_scolaire')
        ordering = ['-annee_scolaire', 'eleve__nom', 'eleve__prenom']
