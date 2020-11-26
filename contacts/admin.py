from django.contrib import admin

# Register your models here.
from .models import Contact, Email, Phone, Nickname, Address, Date, Name
from .models import Language, WorkInfo, File, Social, Relationship

admin.site.register(Contact)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Nickname)
admin.site.register(Address)
admin.site.register(Date)
admin.site.register(Name)
admin.site.register(Language)
admin.site.register(WorkInfo)
admin.site.register(File)
admin.site.register(Social)
admin.site.register(Relationship)