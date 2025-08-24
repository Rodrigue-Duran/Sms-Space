# Fichier de routage spécifique à l’application 'converse'.
# Associe les URLs aux vues correspondantes.


from django.urls import path
from . import views





urlpatterns = [
    path('', views.page_accueil_principal, name='page_accueil_principal'),
    path('page_accueil_uc/<int:user_id>/', views.page_accueil_uc, name='page_accueil_uc'),
    path('page_accueil_principal/', views.page_accueil_principal, name='page_accueil_principal'),
    path('page_contact_liste_selection_uc/<int:user_id>/', views.page_contact_liste_selection_uc, name='page_contact_liste_selection_uc'),
    path('page_contact_liste_uc/<int:user_id>/', views.page_contact_liste_uc, name='page_contact_liste_uc'),
    path('page_contact_particulier_uc/<int:user_id>/<int:autre_id>', views.page_contact_particulier_uc, name='page_contact_particulier_uc'),
    path('page_demandes_envoyees_uc/<int:user_id>/', views.page_demandes_envoyees_uc, name='page_demandes_envoyees_uc'),
    path('page_demandes_recus_uc/<int:user_id>/', views.page_demandes_recus_uc, name='page_demandes_recus_uc'),
    path('page_form_connexion_uc/', views.page_form_connexion_uc, name='page_form_connexion_uc'),
    path('page_form_contact_dev/', views.page_form_contact_dev, name='page_form_contact_dev'),
    path('page_form_contact_dev_confirmation/', views.page_form_contact_dev_confirmation, name='page_form_contact_dev_confirmation'),
    path('page_form_inscription_uc/', views.page_form_inscription_uc, name='page_form_inscription_uc'),
    path('page_mon_profil_uc/<int:user_id>/', views.page_mon_profil_uc, name='page_mon_profil_uc'),
    path('page_mon_profil_uc_modifier/<int:user_id>/', views.page_mon_profil_uc_modifier, name='page_mon_profil_uc_modifier'),
    path('page_rechercher_uc_uc/<int:user_id>/', views.page_rechercher_uc_uc, name='page_rechercher_uc_uc'),
    path('page_signaler_probleme_uc/<int:user_id>/', views.page_signaler_probleme_uc, name='page_signaler_probleme_uc'),
    path('page_se_deconnecter_uc/<int:user_id>/', views.page_se_deconnecter_uc, name='page_se_deconnecter_uc'),
    path('bloquer_contact/<int:user_id>/<int:autre_id>/', views.bloquer_contact, name='bloquer_contact'),
    path('debloquer_contact/<int:user_id>/<int:autre_id>/', views.debloquer_contact, name='debloquer_contact'),
    path('ajax/rechercher_uc/<int:user_id>/', views.rechercher_ajax_uc, name='rechercher_ajax_uc'),
    path('envoyer-message/<int:user_id>/<int:autre_id>/', views.envoyer_message_uc, name='envoyer_message_uc'),
    path('messages_ajax/<int:user_id>/<int:autre_id>/', views.messages_ajax, name='messages_ajax'),

    path('set_typing_status/<int:user_id>/<int:autre_id>/', views.set_typing_status, name='set_typing_status'),
    path('get_typing_status/<int:user_id>/<int:autre_id>/', views.get_typing_status, name='get_typing_status'),


]
