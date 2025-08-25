from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

# Enregistrement des modèles de base
admin.site.register(NiveauScolaire)
admin.site.register(Classe)
admin.site.register(Matiere)
admin.site.register(Poste)
admin.site.register(PersonnelAdministratif)
admin.site.register(Enseignant)
admin.site.register(ContratEnseignant)
admin.site.register(Vehicule)
admin.site.register(Conducteur)
admin.site.register(Itineraire)
admin.site.register(AbonnementTransport)
admin.site.register(TrajetJournalier)
admin.site.register(DomaineFormation)
admin.site.register(Formation)
admin.site.register(Module)
admin.site.register(SessionFormation)
admin.site.register(InscriptionFormation)
admin.site.register(PaiementFormation)
admin.site.register(FraisScolarite)
admin.site.register(Facture)
admin.site.register(LigneFacture)
admin.site.register(Paiement)

# Personnalisation de l'interface d'administration
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# Désenregistrer le modèle User par défaut
admin.site.unregister(User)
# Enregistrer notre version personnalisée
admin.site.register(User, CustomUserAdmin)

# Configuration du site d'administration
admin.site.site_header = "Administration de DerbSkoL"
admin.site.site_title = "Portail d'administration"
admin.site.index_title = "Tableau de bord"
