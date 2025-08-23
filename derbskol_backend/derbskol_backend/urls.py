from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API DerbSkoL 🚀"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # page d'accueil
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),  # ton app API
]
