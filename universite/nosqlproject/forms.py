from django import forms
from .models import Cours
from .models import Etudiant
from .models import Enseignant
from .models import Inscription
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        exclude = ['etudiants']  # ⚠️ On exclut le ManyToMany via Inscription



class EtudiantsForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'



class EnseignantsForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = '__all__'




class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'
        widgets = {
            'date_cours': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-select'}),
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
        }