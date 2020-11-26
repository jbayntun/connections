from django.urls import path

from . import views

urlpatterns = [
    path('', views.contacts, name='contacts'),
    ## ex: /contacts/[uuid]/
    path('<uuid:contact_id>/', views.detail, name='detail'),
]