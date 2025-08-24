from django.db import models

# 🔹 Modèle représentant un utilisateur de la plateforme.
class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)  # Nom de l'utilisateur
    prenom = models.CharField(max_length=100)  # Prénom de l'utilisateur
    pseudo = models.CharField(max_length=100, unique=True)  # Identifiant unique visible
    adresse_mail = models.EmailField(unique=True)  # Adresse email unique
    mot_de_passe = models.CharField(max_length=128)  # Mot de passe (hashé recommandé)

    # État de connexion de l'utilisateur
    ETAT_CHOICES = [
        ('connecte', 'Connecté'),
        ('deconnecte', 'Déconnecté'),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='deconnecte')

    # Situation de l'utilisateur (ex: bloqué, normal, terminé)
    SITUATION_CHOICES = [
        ('bloque', 'Bloqué'),
        ('normal', 'Normal'),
        ('termine', 'Terminé'),
    ]
    situation = models.CharField(max_length=20, choices=SITUATION_CHOICES, default='normal')

    def __str__(self):
        # Représentation textuelle de l'utilisateur
        return f"{self.prenom} {self.nom} ({self.pseudo})"
    
    def est_bloquer(self):
        # Vérifie si l'utilisateur est bloqué
        return self.situation == 'bloque'


# 🔹 Modèle représentant un administrateur (hérite d'Utilisateur)
class Admin(Utilisateur):
    pass  # Peut être enrichi avec des permissions spécifiques


# 🔹 Modèle représentant un utilisateur classique (non admin)
class UtilisateurClassique(Utilisateur):
    pass


# 🔹 Modèle représentant un espace de conversation entre utilisateurs
class EspaceDeConversation(models.Model):
    participants = models.ManyToManyField(Utilisateur)  # Liste des participants
    date_creation = models.DateTimeField(auto_now_add=True)  # Date de création de l'espace


# 🔹 Modèle représentant un message échangé entre deux utilisateurs
class Message(models.Model):
    contenu = models.TextField()  # Contenu du message
    expediteur = models.ForeignKey(Utilisateur, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='messages_recus', on_delete=models.CASCADE)
    date_envoie = models.DateTimeField(auto_now_add=True)  # Date d'envoi
    conversation = models.ForeignKey(EspaceDeConversation, related_name='messages', on_delete=models.CASCADE)
    lu = models.BooleanField(default=False)  # Indique si le message a été lu

    def __str__(self):
        # Affichage du message avec date et noms
        return f"{self.date_envoie} - {self.expediteur.nom} → {self.destinataire.nom}"


# 🔹 Modèle représentant un contact entre deux utilisateurs
class Contact(models.Model):
    espace_de_conversation = models.OneToOneField(EspaceDeConversation, on_delete=models.CASCADE)
    bloque_par = models.ForeignKey(
        Utilisateur, null=True, blank=True, on_delete=models.SET_NULL, related_name='contacts_bloques'
    )  # Utilisateur ayant bloqué le contact

    def est_bloque(self, user):
        # Vérifie si le contact est bloqué par quelqu’un d’autre que l’utilisateur courant
        return self.bloque_par and self.bloque_par != user

    def est_bloqueur(self, user):
        # Vérifie si l’utilisateur courant est celui qui a bloqué
        return self.bloque_par == user

    def autre_utilisateur(self, user):
        # Retourne l'autre participant de la conversation
        return self.espace_de_conversation.participants.exclude(id=user.id).first()


# 🔹 Modèle représentant un problème signalé par un utilisateur
class Probleme(models.Model):
    contenu = models.TextField()  # Description du problème
    date_signalement = models.DateTimeField(auto_now_add=True)  # Date de signalement
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='problemes_signales')

    STATUT_CHOICES = [
        ('en_attente', 'En attente de résolution'),
        ('resolu', 'Résolu'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        # Affichage du problème avec nom et date
        return f"Problème signalé par {self.utilisateur.nom} le {self.date_signalement.strftime('%Y-%m-%d')}"


# 🔹 Modèle représentant une demande de conversation entre deux utilisateurs
class DemandeDeConversation(models.Model):
    expediteur = models.ForeignKey(Utilisateur, related_name='demandes_envoyees', on_delete=models.CASCADE)
    receveur = models.ForeignKey(Utilisateur, related_name='demandes_recues', on_delete=models.CASCADE)
    date_denvoie = models.DateTimeField(auto_now_add=True)  # Date d'envoi de la demande

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        # Affichage de la demande avec noms et statut
        return f"Demande de {self.expediteur.nom} à {self.receveur.nom} - {self.get_statut_display()}"


# 🔹 Modèle indiquant si un utilisateur est en train d’écrire à un autre
class StatutDeFrappe(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='statuts_de_frappe')
    cible = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='cibles_de_frappe')
    est_en_train_decrire = models.BooleanField(default=False)  # Indique si l'utilisateur écrit
    date_mise_a_jour = models.DateTimeField(auto_now=True)  # Dernière mise à jour

    class Meta:
        unique_together = ('utilisateur', 'cible')  # Un seul statut par paire utilisateur/cible
