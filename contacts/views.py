from django.shortcuts import render
from django.template import loader

from .models import Contact, Name

def contacts(request):
    contacts = Contact.objects.all()
    context = {
        'contact_list': contacts,
    }
    return render(request, 'contacts/contact_list.html', context)


def detail(request, contact_id):
    return HttpResponse("You're looking at contact %s." % contact_id)