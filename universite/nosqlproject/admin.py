from django.contrib import admin
from .models import Etudiant, Enseignant, Cours, Inscription


admin.site.site_header = "Administration universtité"
admin.site.site_title = "Université Admin"
admin.site.index_title = "Gestion universitaire"




# -----------------------------
# INLINE POUR INSCRIPTION
# -----------------------------
class InscriptionInline(admin.TabularInline):
    model = Inscription
    extra = 1
    autocomplete_fields = ['etudiant']



# -----------------------------
# ETUDIANT ADMIN
# -----------------------------
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = (
        'num_carte',
        'nom',
        'prenoms',
        'email',
        'filiere',
        'annee_entree'
    )
    search_fields = ('num_carte', 'nom', 'prenoms', 'email')
    list_filter = ('filiere', 'annee_entree')
    ordering = ('nom',)
    list_per_page = 20


# -----------------------------
# ENSEIGNANT ADMIN
# -----------------------------
@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = (
        'num_ens',
        'nom',
        'prenoms',
        'email',
        'departement',
        'grade',
        'specialite'
    )
    search_fields = ('num_ens', 'nom', 'prenoms', 'email')
    list_filter = ('departement', 'grade')
    ordering = ('nom',)
    list_per_page = 20


# -----------------------------
# COURS ADMIN
# -----------------------------
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = (
        'code_cours',
        'intitule',
        'credit_ects',
        'semestre',
        'niveau',
        'departement',
        'enseignant'
    )

    # Filtres à droite
    list_filter = ('semestre', 'niveau', 'departement')

    # Barre de recherche
    search_fields = ('code_cours', 'intitule')

    # Organisation du formulaire
    fieldsets = (
        ("Informations principales", {
            'fields': ('code_cours', 'intitule', 'credit_ects')
        }),
        ("Organisation", {
            'fields': ('semestre', 'niveau', 'departement')
        }),
        ("Responsable", {
            'fields': ('enseignant',)
        }),
    )

    # CSS personnalisé
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# -----------------------------
# INSCRIPTION ADMIN
# -----------------------------
@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'cours',
        'etudiant',
        'date_cours',
        'heure_debut',
        'heure_fin'
    )
    search_fields = ('cours__intitule', 'etudiant__nom', 'etudiant__prenoms')
    list_filter = ('date_cours',)
    autocomplete_fields = ['cours', 'etudiant']
    list_per_page = 20