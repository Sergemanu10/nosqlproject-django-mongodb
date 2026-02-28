from pymongo import MongoClient
from datetime import datetime, timedelta

# ================================
# 🔹 Connexion MongoDB
# ================================
client = MongoClient("mongodb://localhost:27017/")
db = client["universite_mongodb"]

# 🔹 Collections
etudiant_collection = db["etudiants"]
enseignant_collection = db["enseignants"]
cours_collection = db["cours"]
inscription_collection = db["inscriptions"]

# ================================
# 🔹 Statistiques globales
# ================================
def get_mongo_stats():
    return {
        "total_etudiants": etudiant_collection.count_documents({}),
        "total_enseignants": enseignant_collection.count_documents({}),
        "total_cours": cours_collection.count_documents({}),
        "total_inscriptions": inscription_collection.count_documents({})
    }

# ================================
# 🔹 Synchronisation ETUDIANT
# ================================
def sync_etudiant(instance):

    data = {
        "django_id": instance.id,
        "nom": instance.nom,
        "prenom": instance.prenoms,
        "email": instance.email,
        "numCarte": instance.num_carte,
        "date_creation": datetime.now()
    }

    etudiant_collection.update_one(
        {"django_id": instance.id},
        {"$set": data},
        upsert=True
    )

# ================================
# 🔹 Synchronisation ENSEIGNANT
# ================================
def sync_enseignant(instance):

    data = {
        "django_id": instance.id,
        "nom": instance.nom,
        "prenom": instance.prenoms,
        "email": instance.email,
        "specialite": instance.specialite,
        "date_creation": datetime.now()
    }

    enseignant_collection.update_one(
        {"django_id": instance.id},
        {"$set": data},
        upsert=True
    )

# ================================
# 🔹 Synchronisation COURS
# ================================
def sync_cours(instance):

    data = {
        "django_id": instance.id,
        "code_cours": instance.code_cours,
        "intitule": instance.intitule,
        "description": instance.description,
        "credit_ects": instance.credit_ects,
        "semestre": instance.semestre,
        "niveau": instance.niveau,
        "departement": instance.departement,
        "prerequis": instance.prerequis,
        "enseignant_id": instance.enseignant.id,
        "enseignant_nom": instance.enseignant.nom,
        "date_creation": datetime.now()
    }

    cours_collection.update_one(
        {"django_id": instance.id},
        {"$set": data},
        upsert=True
    )

# ================================
# 🔹 Synchronisation INSCRIPTION
# ================================
def sync_inscription(inscription):

    data = {
        "django_id": inscription.id,
        "cours": {
            "code_cours": inscription.cours.code_cours,
            "intitule": inscription.cours.intitule,
        },
        "etudiant": {
            "num_carte": inscription.etudiant.num_carte,
            "nom": inscription.etudiant.nom,
            "prenoms": inscription.etudiant.prenoms,
        },
        "date_cours": inscription.date_cours.isoformat() if inscription.date_cours else None,
        "heure_debut": inscription.heure_debut.strftime("%H:%M:%S") if inscription.heure_debut else None,
        "heure_fin": inscription.heure_fin.strftime("%H:%M:%S") if inscription.heure_fin else None,
        "date_creation": datetime.now()
    }

    inscription_collection.update_one(
        {"django_id": inscription.id},
        {"$set": data},
        upsert=True
    )

# ================================
# 🔹 Derniers étudiants
# ================================
def get_recent_etudiants(limit=5):
    return list(
        etudiant_collection.find().sort("date_creation", -1).limit(limit)
    )

# ================================
# 🔹 Inscriptions des 7 derniers jours
# ================================
def get_inscriptions_par_jour():
    seven_days_ago = datetime.now() - timedelta(days=7)

    pipeline = [
        {"$match": {"date_creation": {"$gte": seven_days_ago}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$date_creation"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    return list(inscription_collection.aggregate(pipeline))