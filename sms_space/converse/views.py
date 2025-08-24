# Contient les vues (fonctions ou classes) qui traitent les requêtes HTTP.
# Gère la logique d’affichage et d’interaction avec les templates.


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  # Pour afficher un message de confirmation
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from converse import app_logique
from .models import *
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json








# Initialisation de l'application logique (fonctions métier)
app = app_logique.App()

# 🔹 Page d’accueil de l’utilisateur classique
def page_accueil_uc(request, user_id):
    user = UtilisateurClassique.objects.get(id=user_id)
    messages_non_lus = Message.objects.filter(destinataire=user, lu=False)
    demandes_recues = DemandeDeConversation.objects.filter(receveur=user, statut='en_attente')

    # Affiche le nombre de messages non lus et de demandes reçues
    return render(request, 'converse/page_accueil_uc.html', {
        'user': user,
        'messages_non_lus': messages_non_lus.count(),
        'demandes_recues': demandes_recues.count()
    })

# 🔹 Page d’accueil principale (avant connexion)
def page_accueil_principal(request: HttpRequest):
    return render(request, 'converse/page_accueil_principal.html')

# 🔹 Page de sélection de contact (interface intermédiaire)
def page_contact_liste_selection_uc(request):
    return render(request, 'converse/page_contact_liste_selection_uc.html')

# 🔹 Liste des contacts de l’utilisateur
def page_contact_liste_uc(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    espaces = EspaceDeConversation.objects.filter(participants=user)
    autres_utilisateurs = []

    # Pour chaque espace, on récupère l’autre utilisateur et les infos du contact
    for espace in espaces:
        contact = Contact.objects.get(espace_de_conversation=espace)
        autre = espace.participants.exclude(id=user.id).first()
        messages_non_lus = Message.objects.filter(conversation=espace, destinataire=user, lu=False).count()

        autres_utilisateurs.append({
            'autre': autre,
            'contact': contact,
            'count': messages_non_lus,
            'est_bloqueur': contact.bloque_par == user,
            'est_bloque': contact.bloque_par and contact.bloque_par != user,
        })

    return render(request, 'converse/page_contact_liste_uc.html', {
        'user': user,
        'autres_utilisateurs': autres_utilisateurs
    })

# 🔹 Page de conversation avec un contact particulier
def page_contact_particulier_uc(request, user_id, autre_id):
    user = get_object_or_404(Utilisateur, pk=user_id)
    autre = get_object_or_404(Utilisateur, pk=autre_id)

    # Recherche ou création de l’espace de conversation
    conversation = EspaceDeConversation.objects.filter(participants=user).filter(participants=autre).first()
    if not conversation:
        conversation = EspaceDeConversation.objects.create()
        conversation.participants.add(user, autre)

    messages = Message.objects.filter(conversation=conversation).order_by('date_envoie')

    return render(request, 'converse/page_contact_particulier_uc.html', {
        'user': user,
        'autre': autre,
        'messages': messages
    })

# 🔹 Envoi d’un message dans une conversation
def envoyer_message_uc(request, user_id, autre_id):
    if request.method == 'POST':
        expediteur = get_object_or_404(Utilisateur, pk=user_id)
        destinataire = get_object_or_404(Utilisateur, pk=autre_id)
        contenu = request.POST.get('text')

        # Recherche ou création de la conversation
        conversation = EspaceDeConversation.objects.filter(participants=expediteur).filter(participants=destinataire).first()
        if not conversation:
            conversation = EspaceDeConversation.objects.create()
            conversation.participants.add(expediteur, destinataire)

        # Création du message
        Message.objects.create(
            contenu=contenu,
            expediteur=expediteur,
            destinataire=destinataire,
            conversation=conversation
        )

    return redirect('page_contact_particulier_uc', user_id=user_id, autre_id=autre_id)

# 🔹 Chargement des messages via AJAX
def messages_ajax(request, user_id, autre_id):
    expediteur = get_object_or_404(Utilisateur, pk=user_id)
    destinataire = get_object_or_404(Utilisateur, pk=autre_id)
    conversation = EspaceDeConversation.objects.filter(participants=expediteur).filter(participants=destinataire).first()
    messages = Message.objects.filter(conversation=conversation).order_by('date_envoie')

    return render(request, 'converse/messages_ajax.html', {
        'messages': messages,
        'user': expediteur
    })

# 🔹 Mise à jour du statut de frappe (écriture en cours)
@csrf_exempt
def set_typing_status(request, user_id, autre_id):
    if request.method == "POST":
        est_en_train_decrire = request.POST.get("typing") == "true"
        statut, created = StatutDeFrappe.objects.get_or_create(utilisateur_id=user_id, cible_id=autre_id)
        statut.est_en_train_decrire = est_en_train_decrire
        statut.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

# 🔹 Récupération du statut de frappe de l’autre utilisateur
def get_typing_status(request, user_id, autre_id):
    try:
        statut = StatutDeFrappe.objects.get(utilisateur_id=autre_id, cible_id=user_id)
        typing = statut.est_en_train_decrire
        nom = statut.utilisateur.prenom
    except StatutDeFrappe.DoesNotExist:
        typing = False
        nom = ""
    return JsonResponse({"typing": typing, "nom": nom})

# 🔹 Page listant les demandes envoyées par l’utilisateur
def page_demandes_envoyees_uc(request, user_id):
    utilisateur = get_object_or_404(UtilisateurClassique, id=user_id)
    demandes_envoyees = DemandeDeConversation.objects.filter(expediteur=utilisateur).order_by('-date_denvoie')

    return render(request, 'converse/page_demandes_envoyees_uc.html', {
        'utilisateur': utilisateur,
        'demandes_envoyees': demandes_envoyees,
        'user': utilisateur
    })

# 🔹 Page listant les demandes reçues et gestion de leur statut
def page_demandes_recus_uc(request, user_id):
    user = UtilisateurClassique.objects.get(id=user_id)
    demandes = DemandeDeConversation.objects.filter(receveur=user, statut='en_attente')

    if request.method == 'POST':
        action = request.POST.get('action')
        demande_id = request.POST.get('demande_id')
        demande = DemandeDeConversation.objects.get(id=demande_id)

        if action == 'accepter':
            demande.statut = 'acceptee'
            demande.save()
            espace = EspaceDeConversation.objects.create()
            espace.participants.add(demande.expediteur, demande.receveur)
            Contact.objects.create(espace_de_conversation=espace)
            confirmation = f"Demande de {demande.expediteur.pseudo} acceptée ✅"

        elif action == 'refuser':
            demande.statut = 'refusee'
            demande.save()
            confirmation = f"Demande de {demande.expediteur.pseudo} refusée ❌"

        demandes = DemandeDeConversation.objects.filter(receveur=user, statut='en_attente')
        return render(request, 'converse/page_demandes_recus_uc.html', {
            'user': user,
            'demandes': demandes,
            'confirmation': confirmation
        })

    return render(request, 'converse/page_demandes_recus_uc.html', {
        'user': user,
        'demandes': demandes
    })

# 🔹 Formulaire de connexion utilisateur classique
def page_form_connexion_uc(request: HttpRequest):
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        mot_de_passe = request.POST.get('mot_de_passe')

        print("Tentative de connexion avec :", pseudo, mot_de_passe)
        if app.existUserClassique(pseudo, mot_de_passe):
            user = app.getUserClassique(pseudo)
            print(" user est bloquer  ->" + str(user.est_bloquer()))

            if not user.est_bloquer():
                app.connecter_utilisateur(user)
                return redirect('page_accueil_uc', user.id)
            messages.error(request, "Votre compte a été bloqué !")
        else:
            messages.error(request, "Le mot de passe ou le pseudo est incorrecte !")

    return render(request, 'converse/page_form_connexion_uc.html')

# 🔹 Formulaire de contact avec le développeur
def page_form_contact_dev(request):
    return render(request, 'converse/page_form_contact_dev.html')

# 🔹 Page de confirmation après envoi du formulaire de contact
def page_form_contact_dev_confirmation(request):
    return render(request, 'converse/page_form_contact_dev_confirmation.html')



# 🔹 Formulaire d’inscription pour un utilisateur classique
def page_form_inscription_uc(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')  # Récupère le nom
        prenom = request.POST.get('prenom')  # Récupère le prénom
        pseudo = request.POST.get('pseudo')  # Récupère le pseudo
        mot_de_passe = request.POST.get('mot_de_passe')  # Récupère le mot de passe
        adresse_mail = request.POST.get('adresse_mail')  # Récupère l'adresse mail

        try:
            # Tente d’inscrire l’utilisateur via la logique métier
            utilisateur = app.inscrire_utilisateur_classique(nom, prenom, pseudo, adresse_mail, mot_de_passe)
            messages.success(request, "Inscription réussie !")
            return redirect('page_form_connexion_uc')
        except ValueError as e:
            # Affiche une erreur si l’inscription échoue
            messages.error(request, str(e))

    return render(request, 'converse/page_form_inscription_uc.html')

# 🔹 Page affichant le profil de l’utilisateur
def page_mon_profil_uc(request, user_id):
    user = UtilisateurClassique.objects.get(id=user_id)
    return render(request, 'converse/page_mon_profil_uc.html', {'user': user})

# 🔹 Page permettant à l’utilisateur de modifier son profil
def page_mon_profil_uc_modifier(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)

    if request.method == 'POST':
        # Met à jour les champs du profil
        user.pseudo = request.POST.get('pseudo')
        user.adresse_mail = request.POST.get('adresse_mail')
        user.nom = request.POST.get('nom')
        user.prenom = request.POST.get('prenom')

        mot_de_passe = request.POST.get('mot_de_passe')
        if mot_de_passe:
            # Hash le mot de passe avant de le sauvegarder
            user.mot_de_passe = make_password(mot_de_passe)

        user.save()
        return redirect('page_mon_profil_uc', user_id=user.id)

    return render(request, 'converse/page_mon_profil_uc_modifier.html', {'user': user})






# 🔹 Page de recherche d’utilisateurs pour envoyer une demande de conversation
def page_rechercher_uc_uc(request, user_id):
    user = UtilisateurClassique.objects.get(id=user_id)
    query = request.GET.get('q', '')  # Terme de recherche saisi par l'utilisateur

    # Recherche des utilisateurs correspondant au pseudo (hors soi-même)
    resultats = UtilisateurClassique.objects.filter(pseudo__icontains=query).exclude(id=user.id)

    # Liste des utilisateurs à qui une demande est déjà envoyée
    demandes_en_attente = DemandeDeConversation.objects.filter(
        expediteur=user,
        statut='en_attente'
    ).values_list('receveur_id', flat=True)

    confirmation = None
    if request.method == 'POST':
        # Envoi d'une nouvelle demande de conversation
        receveur_id = request.POST.get('receveur_id')
        receveur = UtilisateurClassique.objects.get(id=receveur_id)
        DemandeDeConversation.objects.create(expediteur=user, receveur=receveur, date_denvoie=timezone.now())
        confirmation = receveur.pseudo

        # Mise à jour des résultats et des demandes
        resultats = UtilisateurClassique.objects.filter(pseudo__icontains=query).exclude(id=user.id)
        demandes_en_attente = list(demandes_en_attente) + [receveur.id]

    return render(request, 'converse/page_rechercher_uc_uc.html', {
        'user': user,
        'resultats': resultats,
        'demandes_en_attente': demandes_en_attente,
        'confirmation': confirmation,
    })

# 🔹 Page statique pour signaler un problème (formulaire)
def page_signaler_probleme_uc(request):
    return render(request, 'converse/page_signaler_probleme_uc.html')

# 🔹 Action pour bloquer un contact
def bloquer_contact(request, user_id, autre_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    autre = get_object_or_404(Utilisateur, id=autre_id)

    # Récupère l’espace de conversation entre les deux utilisateurs
    espace = EspaceDeConversation.objects.filter(participants=user).filter(participants=autre).first()
    contact = Contact.objects.get(espace_de_conversation=espace)

    # Vérifie que seul l'utilisateur peut bloquer
    if contact.bloque_par and contact.bloque_par != user:
        return HttpResponseForbidden("Vous ne pouvez pas modifier ce blocage.")

    contact.bloque_par = user
    contact.save()
    return redirect('page_contact_liste_uc', user_id=user_id)

# 🔹 Action pour débloquer un contact
def debloquer_contact(request, user_id, autre_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    autre = get_object_or_404(Utilisateur, id=autre_id)

    espace = EspaceDeConversation.objects.filter(participants=user).filter(participants=autre).first()
    contact = Contact.objects.get(espace_de_conversation=espace)

    # Seul le bloqueur peut débloquer
    if contact.bloque_par != user:
        return HttpResponseForbidden("Vous ne pouvez pas débloquer ce contact.")

    contact.bloque_par = None
    contact.save()
    return redirect('page_contact_liste_uc', user_id=user_id)

# 🔹 Déconnexion de l’utilisateur
def page_se_deconnecter_uc(request, user_id):
    user = UtilisateurClassique.objects.get(id=user_id)
    app.deconnecter_utilisateur(user)
    return redirect('page_form_connexion_uc')

# 🔹 Recherche AJAX d’utilisateurs pour envoi de demande
def rechercher_ajax_uc(request, user_id):
    query = request.GET.get('q', '')
    user = UtilisateurClassique.objects.get(id=user_id)

    # Recherche des utilisateurs correspondant au pseudo
    resultats = UtilisateurClassique.objects.filter(pseudo__icontains=query).exclude(id=user_id)

    # Identifie les demandes déjà envoyées
    demandes_en_attente = DemandeDeConversation.objects.filter(
        expediteur=user,
        statut='en_attente'
    ).values_list('receveur_id', flat=True)

    html = ""
    for utilisateur in resultats:
        html += f"""
        <div class="result-card">
            <div class="result-info">
                <h2>{utilisateur.pseudo}</h2>
                <p>{utilisateur.nom} {utilisateur.prenom}</p>
                {'<span class="etat-demande">⏳ En attente d\'acceptation</span>' if utilisateur.id in demandes_en_attente else ''}
            </div>
            {'' if utilisateur.id in demandes_en_attente else f'''
            <form method="POST" action="/page_rechercher_uc_uc/{user.id}/">
                <input type="hidden" name="receveur_id" value="{utilisateur.id}">
                <button type="submit" class="send-request-btn">📨 Envoyer une demande</button>
            </form>
            '''}
        </div>
        """

    if not resultats:
        html = "<p class='no-result'>😕 Aucun utilisateur trouvé.</p>"

    return JsonResponse({'html': html})
