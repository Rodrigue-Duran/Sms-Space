# Fichier de routage principal du projet.
# Redirige les URLs vers les applications Django (ex: converse).


from django.contrib import admin
from django.urls import path, include
from converse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('converse.urls')),
    
]
