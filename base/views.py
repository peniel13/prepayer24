
from django.shortcuts import render
from core.models import StationPrepay  # Importation depuis l'app 'core'
from django.db.models import Q
from django.contrib import messages
from base.models import Contact
import string 
# Create your views here.
def index(request):
    query = request.GET.get('q', '')  # Récupérer la requête de recherche

    if query:
        # Filtrer les stations de manière flexible sur le nom, commune, ou quartier
        stations = StationPrepay.objects.filter(
            Q(nom__icontains=query) | 
            Q(commune__icontains=query) | 
            Q(quartier__icontains=query)
        )
    else:
        stations = StationPrepay.objects.all()

    context = {
        'stations': stations,
        'query': query,
    }
    return render (request, "base/index.html",context)

# base/views.py


def station_list(request):
    query = request.GET.get('q', '')  # Récupérer la requête de recherche

    if query:
        # Filtrer les stations de manière flexible sur le nom, commune, ou quartier
        stations = StationPrepay.objects.filter(
            Q(nom__icontains=query) | 
            Q(commune__icontains=query) | 
            Q(quartier__icontains=query)
        )
    else:
        stations = StationPrepay.objects.all()

    context = {
        'stations': stations,
        'query': query,
    }
    return render(request, 'base/station_list.html', context)

def apropos(request):
    return render(request,'base/apropos.html')


punc = string.punctuation  
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        content = request.POST['content']

        if len(name) > 1 and len(name) < 30:
            pass
        else:
            messages.error(request, 'Le nom doit comporter entre 2 et 30 caractères.')
            return render(request, 'base/contact.html')

        if len(email) > 1 and len(email) < 30:
            pass
        else:
            messages.error(request, 'L\'email n\'est pas valide.')
            return render(request, 'base/contact.html')

        if len(number) > 9 and len(number) < 13:
            pass
        else:
            messages.error(request, 'Le numéro n\'est pas correct.')
            return render(request, 'base/contact.html')

        # Sauvegarde dans la base de données
        contact = Contact(name=name, email=email, content=content, number=number)
        contact.save()
        messages.success(request, 'Merci de nous avoir contactés ! Votre message a été envoyé.')

    return render(request, 'base/contact.html')