# DerbSkol - Application de Gestion Scolaire

Application web de gestion scolaire développée avec Django (backend) et Flutter (frontend mobile), permettant une gestion complète des étudiants, des factures et des paiements.

## Fonctionnalités

- **Authentification sécurisée** avec Firebase Authentication
- Gestion des étudiants (ajout, modification, suppression)
- Gestion des factures et des paiements
- Tableau de bord administratif
- Synchronisation en temps réel avec Firebase

## Prérequis

### Backend (Django)
- Python 3.8+
- Django 4.2+
- Django REST framework
- Base de données SQLite (par défaut) ou PostgreSQL

### Frontend (Flutter)
- Flutter SDK (version 3.8.1 ou supérieure)
- Dart SDK (version compatible avec Flutter 3.8.1)
- Android Studio / Xcode pour le développement
- Un appareil physique ou un émulateur

## Installation

### Backend (Django)
1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/derbschool.git
   cd derbschool/derbskol_backend
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Sur Windows
   source venv/bin/activate  # Sur macOS/Linux
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

### Frontend (Flutter)
1. **Accéder au dossier du frontend**
   ```bash
   cd ../derb_skol
   ```

2. **Installer les dépendances**
   ```bash
   flutter pub get
   ```

3. **Lancer l'application**
   ```bash
   flutter run
   ```

## Structure du projet

```
derbschool/
├── derbskol_backend/     # Backend Django
│   ├── derbskol_backend/ # Configuration du projet
│   ├── school/           # Application principale
│   │   ├── migrations/   # Migrations de la base de données
│   │   ├── models.py     # Modèles de données
│   │   ├── serializers.py# Sérialiseurs pour l'API
│   │   └── views.py      # Vues de l'API
│   └── manage.py         # Utilitaire de gestion Django
│
└── derb_skol/           # Frontend Flutter
    ├── lib/
    │   ├── models/      # Modèles de données
    │   ├── screens/     # Écrans de l'application
    │   ├── services/    # Services (API, authentification)
    │   └── widgets/     # Widgets réutilisables
    └── pubspec.yaml     # Dépendances Flutter
```

## Dépendances principales

### Backend (Django)
- Django 4.2+
- djangorestframework
- django-cors-headers
- python-dotenv

### Frontend (Flutter)
- `http`: ^1.1.0 (pour les appels API)
- `provider`: ^6.1.1 (gestion d'état)
- `shared_preferences`: ^2.2.2 (stockage local)
- `intl`: ^0.18.1 (formatage des dates et nombres)

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

