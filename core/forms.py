from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))
    class Meta:
        model= get_user_model()
        fields= ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]

from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['nom', 'postnom', 'prenom', 'identifiant_client', 'categorie', 'montant_a_payer', 'id_transaction', 'numero_operant']
        widgets = {
            'montant_a_payer': forms.Select(choices=Payment.MONTANT_CHOICES, attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'postnom': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'prenom': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'identifiant_client': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'id_transaction': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'numero_operant': forms.TextInput(attrs={'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
        }




from .models import PaymentConfirmation

class PaymentConfirmationForm(forms.ModelForm):
    class Meta:
        model = PaymentConfirmation
        fields = ['id_transaction', 'numero_operant']

class ConfirmPaymentForm(forms.Form):
    transaction_id = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID de la transaction'}),
    )
    operant_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro opérant'}),
    )

from .models import Payment2


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Payment2
        fields = ['nom', 'prenom', 'postnom', 'numero_identifiant', 'numero_id', 'numero_transfert']

    def __init__(self, *args, **kwargs):
        # Si vous passez un objet cart à l'initialisation, cela permet de pré-remplir la station
        cart = kwargs.get('cart', None)
        if cart:
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['station_prepay'] = cart.station_prepay

        super().__init__(*args, **kwargs)

    def clean_numero_identifiant(self):
        numero_identifiant = self.cleaned_data.get('numero_identifiant')
        if len(numero_identifiant) < 5:
            raise forms.ValidationError("Le numéro identifiant doit contenir au moins 5 caractères.")
        return numero_identifiant
