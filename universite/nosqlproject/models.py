from django.db import models


# ---------------------------
# ETUDIANTS
# ---------------------------
class Etudiant(models.Model):

    FILIERE_CHOICES = [
        ('BDGL', 'BDGL'),
        ('RSI', 'RSI'),
        ('SI', 'SI'),
    ]

    num_carte = models.CharField(max_length=45, unique=True, null=False, blank=False)
    nom = models.CharField(max_length=45, null=True, blank=True)
    prenoms = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=45, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    filiere = models.CharField(max_length=10, choices=FILIERE_CHOICES, null=True, blank=True)
    annee_entree = models.IntegerField(null=True, blank=True)
    date_naiss = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenoms}"


# ---------------------------
# ENSEIGNANTS
# ---------------------------
class Enseignant(models.Model):

    DEPARTEMENT_CHOICES = [
        ('Maths - Info', 'Maths - Info'),
        ('Anglais', 'Anglais'),
    ]

    GRADE_CHOICES = [
        ('PT', 'PT'),
        ('MC', 'MC'),
    ]

    num_ens = models.CharField(max_length=10, unique=True, null=False, blank=False)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    departement = models.CharField(max_length=100, choices=DEPARTEMENT_CHOICES)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# ---------------------------
# COURS
# ---------------------------
class Cours(models.Model):

    DEPARTEMENT_CHOICES = [
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
        ('Geographie', 'Geographie'),
        ('Math-info', 'Math-info'),
    ]

    code_cours = models.CharField(max_length=20)
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    credit_ects = models.IntegerField()
    semestre = models.CharField(max_length=10)
    niveau = models.CharField(max_length=10)
    departement = models.CharField(max_length=100)
    prerequis = models.CharField(max_length=200, blank=True, null=True)
    enseignant = models.ForeignKey('Enseignant', on_delete=models.CASCADE)

    def __str__(self):
        return self.intitule


# ---------------------------
# TABLE D’ASSOCIATION
# ---------------------------
class Inscription(models.Model):

    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    date_cours = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('cours', 'etudiant')

    def __str__(self):
        return f"{self.etudiant} - {self.cours}"