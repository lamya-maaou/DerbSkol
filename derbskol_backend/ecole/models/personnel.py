from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poste(models.Model):
    """Poste occupé par un membre du personnel"""
    TYPE_POSTE = [
        ('direction', 'Direction'),
        ('administration', 'Administration'),
        ('enseignement', 'Enseignement'),
        ('vie_scolaire', 'Vie scolaire'),
        ('comptabilite', 'Comptabilité'),
        ('maintenance', 'Maintenance'),
        ('autre', 'Autre'),
    ]
    
    intitule = models.CharField(max_length=100)
    type_poste = models.CharField(max_length=20, choices=TYPE_POSTE)
    description = models.TextField(blank=True, null=True)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avantages = models.TextField(blank=True, null=True)
    actif = models.BooleanField(default=True)
    
    def __str__(self):
        return self.intitule
    
    class Meta:
        ordering = ['type_poste', 'intitule']
        verbose_name = "Poste"
        verbose_name_plural = "Postes"


class PersonnelAdministratif(models.Model):
    """Membre du personnel administratif"""
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
    photo = models.ImageField(upload_to='personnel/photos/', null=True, blank=True)
    
    # Informations professionnelles
    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)
    date_embauche = models.DateField()
    numero_cnss = models.CharField(max_length=50, blank=True, null=True)
    numero_cimr = models.CharField(max_length=50, blank=True, null=True)
    
    # Informations bancaires
    banque = models.CharField(max_length=100, blank=True, null=True)
    rib = models.CharField(max_length=50, blank=True, null=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    date_depart = models.DateField(null=True, blank=True)
    motif_depart = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"
    
    class Meta:
        verbose_name = "Personnel administratif"
        verbose_name_plural = "Personnel administratif"
        ordering = ['nom', 'prenom']


class Enseignant(PersonnelAdministratif):
    """Enseignant de l'école"""
    NIVEAU_ETUDE = [
        ('bac_plus_2', 'Bac +2'),
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]
    
    specialite = models.CharField(max_length=100)
    niveau_etude = models.CharField(max_length=20, choices=NIVEAU_ETUDE)
    diplome = models.CharField(max_length=100)
    annee_experience = models.PositiveIntegerField(default=0)
    
    # Matières enseignées
    matieres = models.ManyToManyField('Matiere', related_name='enseignants')
    
    # Disponibilités
    temps_plein = models.BooleanField(default=True)
    heures_semaine = models.PositiveSmallIntegerField(default=20)
    
    # Informations complémentaires
    cv = models.FileField(upload_to='enseignants/cv/', null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"


class Matiere(models.Model):
    """Matière enseignée dans l'établissement"""
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    coefficient = models.PositiveSmallIntegerField(default=1)
    niveaux = models.ManyToManyField('NiveauScolaire', related_name='matieres')
    
    # Volume horaire
    heures_semaine = models.FloatField(help_text="Nombre d'heures par semaine")
    
    # Options
    est_obligatoire = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    class Meta:
        ordering = ['code', 'nom']
        verbose_name = "Matière"
        verbose_name_plural = "Matières"


class ContratEnseignant(models.Model):
    """Contrat d'un enseignant"""
    TYPE_CONTRAT = [
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('vacataire', 'Vacataire'),
        ('stagiaire', 'Stagiaire'),
        ('autre', 'Autre'),
    ]
    
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='contrats')
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT)
    reference = models.CharField(max_length=50, unique=True)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2)
    prime = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avantages = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('resilie', 'Résilié'),
    ], default='en_cours')
    
    # Documents
    fichier_contrat = models.FileField(upload_to='contrats/enseignants/', null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    # Suivi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.enseignant} - {self.get_type_contrat_display()} ({self.date_debut})"
    
    class Meta:
        ordering = ['-date_debut', 'enseignant__nom']
        verbose_name = "Contrat enseignant"
        verbose_name_plural = "Contrats enseignants"
