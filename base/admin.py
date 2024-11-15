from django.contrib import admin
from .models import Contact
from .forms import ContactForm

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm  # Utiliser le formulaire personnalisé
    list_display = ('name', 'email', 'number')  # Champs à afficher dans la liste
    search_fields = ('name', 'email')  # Champs de recherche
    ordering = ('name',)