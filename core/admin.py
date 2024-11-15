from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
    
# core/admin.py
from django.contrib import admin
from .models import StationPrepay, Payment, PaymentConfirmation, Communication

# StationPrepay Admin
from .models import  PaymentNumber

class PaymentNumberInline(admin.TabularInline):
    model = PaymentNumber
    extra = 3 

class StationPrepayAdmin(admin.ModelAdmin):
    inlines = [PaymentNumberInline]  # Ajouter l'inline pour les numéros de paiement
    list_display = ('nom', 'slug', 'commune', 'quartier', 'created_at', 'image_preview')
    search_fields = ('nom', 'commune', 'quartier')
    list_filter = ('commune',)
    prepopulated_fields = {'slug': ('nom',)}

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return '-'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

# Enregistrement du modèle StationPrepay et PaymentNumber dans l'admin
admin.site.register(StationPrepay, StationPrepayAdmin)

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    # Affichage des colonnes dans la liste des paiements
    list_display = (
        'user', 
        'station', 
        'montant_a_payer', 
        'categorie', 
        'statut_paiement', 
        'paiement_verifie', 
        'id_transaction',  # Nouveau champ ajouté
        'numero_operant',  # Nouveau champ ajouté
        'date_creation'
    )
    
    # Filtres dans l'interface d'administration
    list_filter = ('categorie', 'statut_paiement', 'paiement_verifie')
    
    # Champs sur lesquels on peut effectuer des recherches dans l'interface d'administration
    search_fields = ('user__username', 'station__nom', 'identifiant_client', 'id_transaction', 'numero_operant')  # Recherche sur les nouveaux champs
    
    # Champs que l'on peut éditer directement dans la liste (en inline)
    list_editable = ('statut_paiement', 'paiement_verifie')
    
    # Définition d'une action personnalisée pour valider les paiements
    actions = ['validate_payments']

    def validate_payments(self, request, queryset):
        # Action personnalisée pour marquer les paiements comme validés
        queryset.update(paiement_verifie=True)
        self.message_user(request, "Les paiements ont été validés avec succès.")
    validate_payments.short_description = "Valider les paiements sélectionnés"

# Enregistrer le modèle Payment avec la classe d'administration personnalisée


# PaymentConfirmation Admin
class PaymentConfirmationAdmin(admin.ModelAdmin):
    list_display = ('payment', 'id_transaction', 'numero_operant', 'date_confirmation', 'statut_confirmation')
    list_filter = ('statut_confirmation',)
    search_fields = ('payment__user__username', 'id_transaction', 'numero_operant')

    def has_add_permission(self, request, obj=None):
        # Empêche la création manuelle de confirmation, uniquement à partir du modèle Payment
        return False

# Communication Admin
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('station', 'titre', 'date_creation', 'image_preview')
    list_filter = ('station',)
    search_fields = ('titre', 'station__nom')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return '-'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

# Enregistrement des modèles dans l'admin

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentConfirmation, PaymentConfirmationAdmin)
admin.site.register(Communication, CommunicationAdmin)

from django.contrib import admin
from .models import Cart, Payment2, StationPrepay



class Payment2Admin(admin.ModelAdmin):
    # Méthode pour récupérer le nom de la station à partir du modèle Cart
    def station_prepay(self, obj):
        return obj.cart.station_prepay.nom  # Accès à la station via le modèle Cart
    station_prepay.admin_order_field = 'cart__station_prepay'  # Optionnel: permet de trier dans l'admin
    station_prepay.short_description = 'Station'

    # Liste des champs à afficher dans l'admin
    list_display = ('cart', 'station_prepay', 'montant', 'payement_valide', 'created_at', 'user')

admin.site.register(Payment2, Payment2Admin)


from .models import Cart,BaseClientStation

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'station_prepay', 'montant', 'commission', 'total', 'created_at')  # Assurez-vous que 'created_at' est bien là

admin.site.register(Cart, CartAdmin)


@admin.register(BaseClientStation)
class BaseClientStationAdmin(admin.ModelAdmin):
    list_display = ['station_prepay', 'nom', 'prenom', 'postnom', 'identifiant', 'created_at']
    search_fields = ['nom', 'prenom', 'identifiant', 'station_prepay__nom']
    list_filter = ['station_prepay']
