from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Etudiant, Enseignant, Cours, Inscription
from .mongo_service import (
    sync_etudiant,
    sync_enseignant,
    sync_cours,
    sync_inscription, db
)
from pymongo import MongoClient



client = MongoClient('mongodb://localhost:27017')
mongo_db = client['school_db']
mongo_collection = mongo_db['etudiant']


@receiver(post_save, sender=Etudiant)
def etudiant_saved(sender, instance, **kwargs):
    sync_etudiant(instance)

@receiver(post_save, sender=Enseignant)
def sync_enseignant(sender, instance, created, **kwargs):
    data = {
        "numEns": instance.num_ens,
        "nom": instance.nom,
        "prenom": instance.prenoms,
        "email": instance.email,
        "grade": instance.grade,
        "specialite": instance.specialite,
    }

    db.enseignants.update_one(
        {"numEns": instance.num_ens},
        {"$set": data},
        upsert=True
    )

@receiver(post_save, sender=Cours)
def sync_cours_signal(sender, instance, **kwargs):
    try:
        sync_cours(instance)
    except Exception as e:
        print("Erreur MongoDB :", e)


@receiver(post_save, sender=Inscription)
def inscription_saved(sender, instance, **kwargs):
    sync_inscription(instance)


