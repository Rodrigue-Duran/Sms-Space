# Enregistrement des modèles dans l’interface d’administration Django.
# Permet de gérer les objets via le back-office.


from django.contrib import admin
from django.apps import apps



# Récupère tous les modèles de l'application courante
app_models = apps.get_app_config('converse').get_models()

# Enregistre chaque modèle dans l'admin
for model in app_models:
    admin.site.register(model)


