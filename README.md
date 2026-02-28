# Projet Django + MongoDB

## Installation

1. Cloner le projet
git clone https://github.com/tonusername/nosqlproject-django-mongodb.git

2. Créer environnement virtuel
python -m venv venv

3. Installer dépendances
pip install -r requirements.txt

4. Lancer migrations
python manage.py migrate

5. Lancer serveur
python manage.py runserver


MANUEL D’UTILISATION
Projet : Application Django avec Synchronisation MongoDB
1. Présentation du Projet
Cette application a été développée avec Python, Django, SQLite3 (base relationnelle) et MongoDB
(base NoSQL synchronisée).
• Gestion des étudiants
• Gestion des cours
• Gestion des inscriptions
• Synchronisation automatique vers MongoDB
• Dashboard MongoDB avec statistiques
2. Prérequis
Avant l’exécution du projet, installer :
• Python 3.10 ou version supérieure
• Pip
• MongoDB Server
3. Installation du Projet
• 1. Extraire le dossier du projet.
• 2. Créer un environnement virtuel : python -m venv venv
• 3. Activer l’environnement virtuel.
• 4. Installer les dépendances : pip install -r requirements.txt
• 5. Appliquer les migrations : python manage.py migrate
• 6. Créer un super utilisateur : python manage.py createsuperuser
• 7. Lancer le serveur : python manage.py runserver
• 8. Ouvrir le navigateur à l’adresse : http://127.0.0.1:8000
4. Accès à l’Application
Interface Admin : http://127.0.0.1:8000/admin
Permet d’ajouter des étudiants, des cours et des inscriptions.
5. Vérification MongoDB
• 1. Ouvrir le terminal MongoDB avec : mongosh
• 2. Sélectionner la base : use nom_de_la_base
• 3. Afficher les collections : show collections
• 4. Vérifier les données : db.etudiants.find().pretty()
6. Dashboard MongoDB
Accès : http://127.0.0.1:8000/mongo-dashboard/
• Statistiques MongoDB
• Liste des derniers étudiants
• Bouton Actualiser
• Graphiques de données
Conclusion
Ce projet démontre l’intégration d’une base relationnelle (SQLite3) et d’une base NoSQL
(MongoDB) avec synchronisation automatique et dashboard personnalisé.
