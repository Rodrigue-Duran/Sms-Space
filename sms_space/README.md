
---
# 📱 SMS Space

![Django](https://img.shields.io/badge/Django-5.2.5-green)
![Python](https://img.shields.io/badge/Python-3.13.5-blue)
![Statut](https://img.shields.io/badge/Version-v1.0-yellow)

SMS Space est une application web développée avec Django, conçue pour permettre aux utilisateurs d’échanger des messages, gérer leurs contacts et contrôler leurs interactions. Ce projet est né dans le cadre de mon apprentissage de la programmation.

SMS Space is a Django-based web application designed to let users exchange messages, manage contacts, and control their interactions. This project was created as part of my journey to learn programming.

---

## 📚 Sommaire

- [🎯 Objectif](#-objectif)
- [📌 Version actuelle](#-version-actuelle)
- [⚙️ Fonctionnalités](#-fonctionnalités)
- [🛠️ Technologies utilisées](#-technologies-utilisées)
- [🚀 Installation et lancement du projet](#-installation-et-lancement-du-projet)
- [📁 Structure du projet](#-structure-du-projet)
- [🔮 Roadmap](#-roadmap)
- [🤝 Contribuer](#-contribuer)
- [👤 Auteur](#-auteur)

---

## 🎯 Objectif

L’objectif de SMS Space est de simuler une messagerie privée entre utilisateurs, avec des fonctionnalités avancées comme le blocage, les demandes de contact et les notifications. Ce projet me permet d’explorer les bases du développement web avec Django, tout en construisant une application fonctionnelle.

---

## 📌 Version actuelle

Cette version est une **première ébauche**. Certaines fonctionnalités sont encore en cours d’amélioration. Le projet évoluera progressivement pour intégrer plus d’interactions, de sécurité et de personnalisation.

---

## ⚙️ Fonctionnalités

- 🔐 Inscription et connexion sécurisée  
- 💬 Envoi et réception de messages  
- 👥 Ajout, suppression et blocage de contacts  
- 📩 Gestion des demandes de conversation  
- 🔔 Notifications sonores (envoi/réception)  
- 🌐 Interface web avec templates HTML/CSS  
- 🧭 Filtres personnalisés via Django templatetags  

---

## 🛠️ Technologies utilisées

- Python 3.13  
- Django 5.2  
- SQLite  
- HTML5 / CSS3 / JavaScript  
- Django Templates  
- WAV pour les sons de notification  

---

## 🚀 Installation et lancement du projet


# 1. Cloner le dépôt
git clone https://github.com/Rodrigue-Duran/Sms-Space.git
cd Sms-Space/sms_space

# 2. Créer un environnement virtuel
python -m venv env
source env/bin/activate  # Sur Linux/macOS
env\Scripts\activate     # Sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Lancer le serveur
python manage.py runserver

👉 Ouvrez votre navigateur à l’adresse suivante :  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Structure du projet

```
sms_space/
│
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
│
├── converse/
│   ├── admin.py, models.py, views.py, urls.py, etc.
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── templatetags/
│
└── sms_space/
    ├── settings.py, urls.py, wsgi.py, etc.
```

---

## 🔮 Roadmap

Fonctionnalités prévues pour les prochaines versions :

- 📡 Messagerie en temps réel via WebSockets  
- 📱 Version mobile responsive  
- 🧠 Suggestions de contacts intelligentes  
- 🌍 Déploiement sur un serveur distant (Render, Heroku, etc.)  
- 🧪 Tests automatisés et CI/CD  

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Pour participer :

1. Fork le dépôt  
2. Crée une branche (`git checkout -b feature/ma-fonctionnalite`)  
3. Commits tes modifications (`git commit -m 'Ajout d'une fonctionnalité'`)  
4. Push ta branche (`git push origin feature/ma-fonctionnalite`)  
5. Ouvre une Pull Request  

N’hésite pas à ouvrir une issue pour discuter d’une idée ou d’un bug.

---

## 👤 Auteur

Développé avec passion par **Rodrigue Nguetsa**  
💡 *“Chaque ligne de code est une marche vers la maîtrise. SMS Space est mon terrain d’entraînement.”*
