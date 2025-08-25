from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='api-home'),
    
    # URLs pour la gestion des élèves
    path('eleves/', views.eleves_liste, name='eleves_liste'),
    path('eleves/ajouter/', views.eleves_ajouter, name='eleves_ajouter'),
    
    # URLs pour la gestion des cours
    path('cours/', views.cours_liste, name='cours_liste'),
    path('cours/ajouter/', views.cours_ajouter, name='cours_ajouter'),
    
    # URLs pour la gestion des factures
    path('factures/', views.factures_liste, name='factures_liste'),
    path('factures/creer/', views.factures_creer, name='factures_creer'),
    
    # URLs pour la gestion des enseignants
    path('enseignants/', views.enseignants_liste, name='enseignants_liste'),
    path('enseignants/ajouter/', views.enseignants_ajouter, name='enseignants_ajouter'),
]
