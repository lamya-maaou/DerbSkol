# Configuration CORS pour permettre les requêtes entre le frontend et le backend

# Autoriser toutes les origines (à restreindre en production)
CORS_ORIGIN_ALLOW_ALL = True

# Configuration CORS plus stricte pour la production
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # Adresse de votre frontend React
#     "http://127.0.0.1:3000",
# ]

# Configuration pour les en-têtes autorisés
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Configuration pour les méthodes autorisées
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Configuration pour les cookies cross-origin
CORS_ALLOW_CREDENTIALS = True
