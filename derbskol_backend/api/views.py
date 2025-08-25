from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    # On passe toujours la requête au contexte pour le template
    context = {'request': request}
    # Si l'utilisateur est authentifié, on affiche le tableau de bord
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', context)
    # Sinon, on pourrait rediriger vers la page de connexion
    # ou afficher une page d'accueil publique
    return render(request, 'dashboard.html', context)  # Pour l'instant, on affiche le dashboard à tout le monde

def eleves_liste(request):
    # Vue pour afficher la liste des élèves
    context = {'request': request}
    return render(request, 'eleves/liste.html', context)

def eleves_ajouter(request):
    # Vue pour ajouter un nouvel élève
    context = {'request': request}
    return render(request, 'eleves/ajouter.html', context)

# Vues pour le module Cours
def cours_liste(request):
    context = {'request': request}
    return render(request, 'cours/liste.html', context)

def cours_ajouter(request):
    context = {'request': request}
    return render(request, 'cours/ajouter.html', context)

# Vues pour le module Factures
def factures_liste(request):
    context = {'request': request}
    return render(request, 'factures/liste.html', context)

def factures_creer(request):
    context = {'request': request}
    return render(request, 'factures/creer.html', context)

# Vues pour le module Enseignants
def enseignants_liste(request):
    context = {'request': request}
    return render(request, 'enseignants/liste.html', context)

def enseignants_ajouter(request):
    context = {'request': request}
    return render(request, 'enseignants/ajouter.html', context)
