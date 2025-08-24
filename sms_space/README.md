# 📱 SMS Space

Une application Django permettant la gestion de conversations par SMS entre utilisateurs. Elle inclut des fonctionnalités de messagerie, de gestion de contacts, de profil utilisateur et de signalement de problèmes.

## 🚀 Fonctionnalités

- Connexion / Inscription
- Envoi et réception de messages
- Gestion des contacts (ajout, blocage)
- Interface utilisateur personnalisée
- Notifications sonores
- Signalement de problèmes

## 🧰 Technologies

- Python 3.13
- Django
- SQLite (base de données locale)
- HTML/CSS/JS
- WAV pour les sons

## 📦 Structure du projet

- `converse/` : logique métier, vues, modèles, templates
- `sms_space/` : configuration du projet Django
- `static/` : fichiers CSS, JS, sons
- `templates/` : pages HTML
- `templatetags/` : filtres personnalisés Django

## ⚙️ Installation

```bash
git clone https://github.com/Rodrigue-Duran/Sms-Space.git
cd sms_space
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
