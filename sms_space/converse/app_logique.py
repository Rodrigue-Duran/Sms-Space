# Fichier contenant la logique métier spécifique.
# Séparation des fonctions complexes pour plus de clarté.


from django.db import models
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import *



# 🔹 Classe principale contenant la logique métier de l'application
class App:

    # 🔐 Vérifie si un utilisateur classique existe et si le mot de passe est correct
    def existUserClassique(self, pseudo, mot_de_passe):
        try:
            user = UtilisateurClassique.objects.get(pseudo=pseudo)
            # Vérifie le mot de passe en le comparant avec le hash stocké
            return check_password(mot_de_passe, user.mot_de_passe)
        except UtilisateurClassique.DoesNotExist:
            return False
        
        

    # 🔍 Récupère un utilisateur classique par son pseudo
    def getUserClassique(self, pseudo):
        return UtilisateurClassique.objects.get(pseudo=pseudo)
    
    

    # 📝 Inscription d’un nouvel utilisateur classique
    def inscrire_utilisateur_classique(self, nom, prenom, pseudo, adresse_mail, mot_de_passe):
        # Vérifie que tous les champs sont remplis
        if not all([nom, prenom, pseudo, adresse_mail, mot_de_passe]):
            raise ValueError("Tous les champs sont obligatoires.")

        # Vérifie l’unicité du mail et du pseudo
        if UtilisateurClassique.objects.filter(adresse_mail=adresse_mail).exists():
            raise ValueError("Adresse mail déjà utilisée.")
        if UtilisateurClassique.objects.filter(pseudo=pseudo).exists():
            raise ValueError("Pseudo déjà utilisé.")

        # Hash du mot de passe
        mot_de_passe_hache = make_password(mot_de_passe)

        # Création de l’utilisateur
        utilisateur = UtilisateurClassique.objects.create(
            nom=nom,
            prenom=prenom,
            pseudo=pseudo,
            adresse_mail=adresse_mail,
            mot_de_passe=mot_de_passe_hache
        )
        return utilisateur
    
    

    # 🔓 Connecte un utilisateur (modifie son état)
    def connecter_utilisateur(self, utilisateur):
        if utilisateur.situation == 'bloque':
            raise PermissionError("Connexion refusée : utilisateur bloqué.")
        utilisateur.etat = 'connecte'
        utilisateur.save()



    # 🔒 Déconnecte un utilisateur
    def deconnecter_utilisateur(self, utilisateur):
        utilisateur.etat = 'deconnecte'
        utilisateur.save()



    # 📬 Envoie une demande de conversation
    def envoyer_demande(self, expediteur, receveur):
        if expediteur == receveur:
            raise ValueError("Impossible d'envoyer une demande à soi-même.")
        if expediteur.situation == 'bloque' or receveur.situation == 'bloque':
            raise PermissionError("L'un des utilisateurs est bloqué.")
        DemandeDeConversation.objects.create(expediteur=expediteur, receveur=receveur)



    # ✅ Accepte une demande de conversation
    def accepter_demande(self, demande):
        if demande.statut != 'en_attente':
            raise ValueError("Demande déjà traitée.")
        demande.statut = 'acceptee'
        demande.save()

        # Crée ou récupère l’espace de conversation
        espace = self._get_espace_conversation(demande.expediteur, demande.receveur)
        if not espace:
            espace = EspaceDeConversation.objects.create()
            espace.participants.add(demande.expediteur, demande.receveur)

        # Crée le contact associé
        contact = Contact.objects.create(espace_de_conversation=espace)
        contact.participants.add(demande.expediteur, demande.receveur)  # ⚠️ Ce champ n’existe pas dans le modèle Contact



    # ❌ Refuse une demande de conversation
    def refuser_demande(self, demande):
        if demande.statut != 'en_attente':
            raise ValueError("Demande déjà traitée.")
        demande.statut = 'refusee'
        demande.save()

    # ✉️ Envoie un message dans une conversation existante
    def envoyer_message(self, expediteur, destinataire, contenu):
        if expediteur.situation == 'bloque':
            raise PermissionError("Utilisateur bloqué. Envoi de message interdit.")
        espace = self._get_espace_conversation(expediteur, destinataire)
        if not espace:
            raise ValueError("Pas d'espace de conversation entre ces utilisateurs.")
        Message.objects.create(
            contenu=contenu,
            expediteur=expediteur,
            destinataire=destinataire,
            conversation=espace
        )

    # 🔍 Recherche d’utilisateurs par pseudo ou email
    def rechercher_utilisateur(self, query):
        return UtilisateurClassique.objects.filter(
            models.Q(pseudo__icontains=query) |
            models.Q(adresse_mail__icontains=query)
        )

    # 🛠️ Création d’un administrateur
    def ajouter_admin(self, nom, prenom, pseudo, adresse_mail, mot_de_passe):
        return Admin.objects.create(
            nom=nom,
            prenom=prenom,
            pseudo=pseudo,
            adresse_mail=adresse_mail,
            mot_de_passe=mot_de_passe
        )

    # 🚫 Bloque un utilisateur
    def bloquer_utilisateur(self, utilisateur):
        utilisateur.situation = 'bloque'
        utilisateur.save()

    # ✅ Débloque un utilisateur
    def debloquer_utilisateur(self, utilisateur):
        utilisateur.situation = 'normal'
        utilisateur.save()

    # 🗑️ Supprime un utilisateur
    def supprimer_utilisateur(self, utilisateur):
        utilisateur.delete()

    # 🛎️ Consultation des problèmes signalés (réservé aux admins)
    def consulter_problemes(self, admin):
        if not isinstance(admin, Admin):
            raise PermissionError("Seuls les admins peuvent consulter les problèmes.")
        return Probleme.objects.all()

    # 🔧 Méthode interne pour retrouver une conversation entre deux utilisateurs
    def _get_espace_conversation(self, u1, u2):
        return EspaceDeConversation.objects.filter(participants=u1)\
            .filter(participants=u2).first()
