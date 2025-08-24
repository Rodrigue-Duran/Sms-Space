# Définition de filtres et tags personnalisés pour les templates Django.
# Permet d’ajouter des fonctionnalités dans les fichiers HTML.



from django import template
register = template.Library()

@register.filter
def dict_key(d, key):
    return d.get(key, 0)
