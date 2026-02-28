from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import *


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
# COURS
    path('cours/', views.cours_list, name='cours_list'),
    path('cours/ajouter/', views.cours_create, name='cours_create'),
    path('cours/update/<int:pk>/', views.cours_update, name='cours_update'),
    path('cours/delete/<int:pk>/', views.cours_delete, name='cours_delete'),

# ETUDIANTS
    path('etudiants/', views.etudiants_list, name='etudiants_list'),
    path('etudiants/ajouter/', views.etudiants_create, name='etudiants_create'),
    path('etudiants/update/<int:pk>/', views.etudiants_update, name='etudiants_update'),
    path('etudiants/delete/<int:pk>/', views.etudiants_delete, name='etudiants_delete'),

# ENSEIGNANTS
    path('enseignants/', views.enseignants_list, name='enseignants_list'),
    path('enseignants/ajouter/', views.enseignants_create, name='enseignants_create'),
    path('enseignants/update/<int:pk>/', views.enseignants_update, name='enseignants_update'),
    path('enseignants/delete/<int:pk>/', views.enseignants_delet, name='enseignants_delete'),

# INSCRIPTIONS
    path('inscriptions/', views.inscriptions_list, name='inscriptions_list'),
    path('inscriptions/create/', views.inscriptions_create, name='inscriptions_create'),
    path('inscriptions/update/<int:pk>/', views.inscriptions_update, name='inscriptions_update'),
    path('inscriptions/delete/<int:pk>/', views.inscriptions_delete, name='inscriptions_delete'),
    path('api/stats/', views.stats_api, name='stats_api'),
    path('mongo_dashboard/', views.mongo_dashboard, name='mongo_dashboard'),

]

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet)
router.register(r'Enseignants', EnseignantViewSet)
router.register(r'cours', CoursViewSet)
router.register(r'Inscriptions', InscriptionViewSet)

urlpatterns += router.urls