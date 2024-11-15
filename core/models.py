from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Le champ `is_active` est défini par défaut à False
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email


from django.db import models
from django.utils.text import slugify


# Modèle pour la station de distribution
class StationPrepay(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    commune = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='stations/', blank=True, null=True)  # Ajout du champ image
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Payment(models.Model):
    CATEGORIE_CHOICES = [
        ('menage', 'Ménage'),
        ('bar', 'Bar'),
        ('entreprise', 'Entreprise'),
        ('eglise', 'Église'),
        ('autres', 'Autres'),
    ]
    
    # Référence à la station
    station = models.ForeignKey(StationPrepay, on_delete=models.CASCADE, related_name='payments')
    
    # Informations sur l'utilisateur
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    identifiant_client = models.CharField(max_length=50, unique=True)
    
    # Categorie (Ménage, Bar, Entreprise, etc)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    
    # Montant à payer (dropdown des options)
    MONTANT_CHOICES = [
        (10000, '10 000 FCFA'),
        (20000, '20 000 FCFA'),
        (50000, '50 000 FCFA'),
    ]
    montant_a_payer = models.IntegerField(choices=MONTANT_CHOICES)

    # Statut de validation du paiement
    statut_paiement = models.BooleanField(default=False)  # False signifie "Non confirmé"
    
    # Champ pour savoir si le paiement a été vérifié par l'admin
    paiement_verifie = models.BooleanField(default=False)  # True si vérifié par admin, False sinon
    
    # Nouveaux champs
    id_transaction = models.CharField(max_length=255, null=True, blank=True, help_text="ID de transaction unique")
    numero_operant = models.CharField(max_length=100, null=True, blank=True, help_text="Numéro de l'opérant traitant la transaction")
    
    # Date de création
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Paiement pour {self.user.username} - {self.station.nom}"

    def save(self, *args, **kwargs):
        # Si le paiement est confirmé, on désactive le formulaire
        if self.paiement_verifie:
            self.statut_paiement = True  # Le paiement est confirmé
        super().save(*args, **kwargs)


# Modèle pour la confirmation du paiement par l'admin
class PaymentConfirmation(models.Model):
    # Référence au paiement
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='confirmation')
    
    # ID de transaction et numéro opérant
    id_transaction = models.CharField(max_length=255, help_text="ID de transaction unique")
    numero_operant = models.CharField(max_length=100, help_text="Numéro de l'opérant traitant la transaction")
    
    # Date de confirmation
    date_confirmation = models.DateTimeField(auto_now_add=True)

    # Statut de confirmation (True si vérifié, False si non confirmé)
    statut_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return f"Confirmation de paiement pour {self.payment.user.username} - {self.payment.station.nom}"


class Communication(models.Model):
    station = models.ForeignKey(StationPrepay, on_delete=models.CASCADE, related_name='communications')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="communications/")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class PaymentNumber(models.Model):
    station = models.ForeignKey(StationPrepay, on_delete=models.CASCADE, related_name='payment_numbers')
    numero = models.CharField(max_length=20, unique=True, help_text="Numéro de paiement associé à cette station")
    image = models.ImageField(upload_to="payment_numbers/", blank=True, null=True, help_text="Image associée au numéro de paiement")

    def __str__(self):
        return f"Numéro de paiement {self.numero} pour {self.station.nom}"



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    station_prepay = models.ForeignKey('StationPrepay', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=4000, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si la commission est None, la définir par défaut à 4000
        if self.commission is None:
            self.commission = 4000
        
        # Calculer le total en ajoutant la commission au montant
        self.total = (self.montant or 0) + self.commission
        
        super().save(*args, **kwargs)



# models.py

class Payment2(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Lier le paiement au panier
    station_prepay = models.ForeignKey('StationPrepay', on_delete=models.CASCADE, null=True, blank=True)  # Ajouter la relation vers StationPrepay
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    postnom = models.CharField(max_length=255)
    numero_identifiant = models.CharField(max_length=255)
    numero_id = models.CharField(max_length=255)
    numero_transfert = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payement_valide = models.BooleanField(default=False)  # À valider manuellement

    def __str__(self):
        return f"Payment for {self.cart.id} by {self.user.username}"

    @property
    def montant(self):
        return self.cart.montant

    @property
    def total(self):
        return self.cart.total

class BaseClientStation(models.Model):
    station_prepay = models.ForeignKey(StationPrepay, on_delete=models.CASCADE, related_name="clients")
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    postnom = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    avenue = models.CharField(max_length=255)
    numparcel = models.CharField(max_length=255)
    identifiant = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.station_prepay.nom}"