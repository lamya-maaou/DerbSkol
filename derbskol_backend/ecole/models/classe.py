from django.db import models

class NiveauScolaire(models.Model):
    CYCLE_CHOICES = [
        ('maternelle', 'Maternelle'),
        ('primaire', 'Primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('superieur', 'Supérieur'),
    ]
    
    nom = models.CharField(max_length=100)
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    ordre = models.PositiveSmallIntegerField(help_text="Ordre d'affichage")
    
    def __str__(self):
        return f"{self.get_cycle_display()} - {self.nom}"
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Niveau scolaire"
        verbose_name_plural = "Niveaux scolaires"


class Classe(models.Model):
    niveau = models.ForeignKey(NiveauScolaire, on_delete=models.CASCADE, related_name='classes')
    nom = models.CharField(max_length=100)
    capacite_max = models.PositiveSmallIntegerField(default=30)
    responsable = models.ForeignKey('Enseignant', on_delete=models.SET_NULL, null=True, blank=True, related_name='classes_dirigees')
    
    # Horaires
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    
    # Options
    est_actif = models.BooleanField(default=True)
    
    # Frais spécifiques à la classe
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_mensuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_dossier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def effectif_actuel(self):
        return self.inscriptions.filter(statut='validee').count()
    
    def places_disponibles(self):
        return self.capacite_max - self.effectif_actuel()
    
    def __str__(self):
        return f"{self.niveau.nom} - {self.nom}"
    
    class Meta:
        ordering = ['niveau__ordre', 'nom']
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
