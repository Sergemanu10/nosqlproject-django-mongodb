from django.contrib import messages
from .models import Cours
from .forms import CoursForm
import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Etudiant
from .forms import EtudiantsForm
from .models import Enseignant
from .forms import EnseignantsForm
from .models import Inscription
from .forms import InscriptionForm
from django.http import JsonResponse
from .mongo_service import get_mongo_stats, get_recent_etudiants, get_inscriptions_par_jour




def dashboard(request):
    total_cours = Cours.objects.count()
    total_enseignants = Enseignant.objects.count()
    total_etudiants = Etudiant.objects.count()

    # 👇 Total des étudiants ayant au moins une inscription
    total_inscrits = Inscription.objects.values('etudiant').distinct().count()

    context = {
        'total_cours': total_cours,
        'total_enseignants': total_enseignants,
        'total_etudiants': total_etudiants,
        'total_inscrits': total_inscrits,
    }

    return render(request, 'nosqlproject/dashboard.html', context)


def cours_list(request):
    cours = Cours.objects.all()
    paginator = Paginator(cours, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'nosqlproject/cours_list.html', {
        'cours_list': cours
    })


def cours_create(request):
    if request.method == "POST":
        form = CoursForm(request.POST)

        # 👇 METS LES PRINTS ICI
        print("POST DATA:", request.POST)
        print("VALID:", form.is_valid())

        if form.is_valid():
            form.save()
            print("SAVED SUCCESSFULLY")
            return redirect('cours_list')
        else:
            print("ERRORS:", form.errors)

    else:
        form = CoursForm()

    return render(request, 'nosqlproject/cours_form.html', {'form': form})



def cours_update(request, pk):
    cours = Cours.objects.get(pk=pk)

    if request.method == "POST":
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            return redirect('cours_list')
    else:
        form = CoursForm(instance=cours)

    return render(request, 'nosqlproject/cours_form.html', {'form': form})


def cours_delete(request, pk):
    cours = Cours.objects.get(pk=pk)

    if request.method == "POST":
        cours.delete()
        return redirect('cours_list')

    return render(request, 'nosqlproject/cours_confirm_delete.html', {'cours': cours})




def etudiants_list(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'nosqlproject/etudiants_list.html', {
        'etudiants_list': etudiants
    })


def etudiants_create(request):
    form = EtudiantsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('etudiants_list')
    return render(request, 'nosqlproject/etudiants_form.html', {'form': form})


def etudiants_update(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    form = EtudiantsForm(request.POST or None, instance=etudiant)
    if form.is_valid():
        form.save()
        return redirect('etudiants_list')
    return render(request, 'nosqlproject/etudiants_form.html', {'form': form})


def etudiants_delete(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    etudiant.delete()
    return redirect('etudiants_list')



def enseignants_list(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'nosqlproject/enseignants_list.html', {'enseignants_list':enseignants})


def enseignants_create(request):
    if request.method == "POST":
        form = EnseignantsForm(request.POST)

        if form.is_valid():
            num_ens = form.cleaned_data['num_ens']

            # Vérification manuelle du doublon
            if Enseignant.objects.filter(num_ens=num_ens).exists():
                messages.error(request, "⚠️ Ce numéro enseignant existe déjà.")
            else:
                form.save()
                messages.success(request, "✅ Enseignant ajouté avec succès.")
                return redirect("enseignants_list")
    else:
        form = EnseignantsForm()

    return render(request, "nosqlproject/enseignants_form.html", {"form": form})


def enseignants_update(request, pk):
    enseignant = get_object_or_404(Etudiant, pk=pk)
    form = EnseignantsForm(request.POST or None, instance=enseignant)
    if form.is_valid():
        form.save()
        return redirect('enseignants_list')
    return render(request, 'nosqlproject/enseignants_form.html', {'form': form})


def enseignants_delet(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    enseignant.delete()
    return redirect('enseignants_list')



# =========================
# LISTE DES INSCRIPTIONS
# =========================
def inscriptions_list(request):
    inscriptions = Inscription.objects.select_related('cours', 'etudiant').all()
    return render(request, 'nosqlproject/inscriptions_list.html', {
        'inscriptions_list': inscriptions
    })


# =========================
# CREER UNE INSCRIPTION
# =========================
def inscriptions_create(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inscriptions_list')
    else:
        form = InscriptionForm()

    return render(request, 'nosqlproject/inscriptions_form.html', {
        'form': form,
        'title': "Nouvelle Inscription"
    })


# =========================
# MODIFIER UNE INSCRIPTION
# =========================
def inscriptions_update(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)

    if request.method == 'POST':
        form = InscriptionForm(request.POST, instance=inscription)
        if form.is_valid():
            form.save()
            return redirect('inscriptions_list')
    else:
        form = InscriptionForm(instance=inscription)

    return render(request, 'nosqlproject/inscriptions_form.html', {
        'form': form,
        'title': "Modifier l'inscription"
    })


# =========================
# SUPPRIMER UNE INSCRIPTION
# =========================
def inscriptions_delete(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)

    if request.method == 'POST':
        inscription.delete()
        return redirect('inscriptions_list')

    return render(request, 'nosqlproject/inscriptions_confirm_delete.html', {
        'object': inscription
    })


def stats_api(request):
    data = {
        "total_cours": Cours.objects.count(),
        "total_enseignants": Enseignant.objects.count(),
        "total_etudiants": Etudiant.objects.count(),
        "total_inscriptions": Inscription.objects.count(),
    }
    return JsonResponse(data)



def mongo_dashboard(request):
    stats = get_mongo_stats()

    context = {
        "total_etudiants": stats["total_etudiants"],
        "total_enseignants": stats["total_enseignants"],
        "total_cours": stats["total_cours"],
        "total_inscriptions": stats["total_inscriptions"],
        "recent_etudiants": get_recent_etudiants(),
        "chart_data": json.dumps(get_inscriptions_par_jour())
    }

    return render(request, "nosqlproject/mongo_dashboard.html", context)