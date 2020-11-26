import uuid
import pytz
import pycountry

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

DATE_OPTIONS = ['birthday', 'anniversary', 'related birthday', 'other', 'death date']
DATE_TYPES = tuple(zip(DATE_OPTIONS, DATE_OPTIONS))

PRONOUN_OPTIONS = ['She/her/hers', 'He/him/his', 'They/them/theirs', 'None (name only)', 'Not in list'] ## could make a look up table later so people can provide their own...
PRONOUNS = tuple(zip(PRONOUN_OPTIONS, PRONOUN_OPTIONS))

CALENDAR_OPTIONS = ['Western (Gregorian)', 'Chinese (Traditional Lunar)', ' Shaka Samvat',  'Buddhist', 'Iranian', 'Hijiri', 'Hebrew']
CALENDARS = tuple(zip(CALENDAR_OPTIONS, CALENDAR_OPTIONS))

SOCIAL_OPTIONS = ['LinkedIn', 'Instagram','WeChat', 'Facebook', 'Twitter', 'YouTube', 'TikTok', 'Other']
SOCIALS = tuple(zip(SOCIAL_OPTIONS, SOCIAL_OPTIONS))

## pycountry lists a bajillion languages, so many it takes seconds to load the drop down.  Ah well, simple and hardcoded for now...
LANGUAGE_OPTIONS = ['English', 'Mandarin', 'Cantonese', 'Spanish', 'Arabic', 'German', 'Italian', 'Russian', 'Hindi', 'Bengali', 'Japanese', 'French', 'Portuguese', 'Turkish', 'Korean', 'Farsi', 'Hebrew', 'Urdu', 'Indonesian', 'Vietnamese', 'Javanese', 'Filipino', 'Swahili', 'Telugu', 'Tamil', 'Thai', 'Dutch', 'Polish']
LANGUAGES = tuple(zip(LANGUAGE_OPTIONS, LANGUAGE_OPTIONS))

RELATIONSHIP_OPTIONS = ['co-worker', 'spouse', 'friend', 'parent', 'child', 'sibling', 'acquaintance', 'neighbor', 'relative', 'significant other', 'ex-spouse', 'ex-significant other', 'roommate', 'agent', 'other']
RELATIONSHIPS = tuple(zip(RELATIONSHIP_OPTIONS, RELATIONSHIP_OPTIONS))

COUNTRIES = [(country.name, country.name) for country in pycountry.countries]
TIMEZONES = tuple(zip(pytz.common_timezones, pytz.common_timezones))

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # Need this to use taggit with UUID PK

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    primary_name = models.OneToOneField('Name', on_delete=models.DO_NOTHING, related_name='primary_name', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField(blank=True, upload_to='avatar_images/', max_length=150)
    timezone = models.CharField(max_length=64, choices=TIMEZONES, blank=True)
    comment = models.TextField(blank=True)
    pronouns = models.CharField(
        max_length = 32, 
        choices = PRONOUNS, 
        blank = True
    )

    tags = TaggableManager(through=UUIDTaggedItem, blank=True)
    birth_place = models.CharField(max_length=128, blank=True)
    is_deceased = models.BooleanField()
    death_place = models.CharField(max_length=128, blank=True)
    food_preference = models.TextField(blank=True, help_text='Likes, dislikes, allergies, etc...')

    def __str__(self):
        return str(self.id)

class WorkInfo(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    company = models.CharField(max_length=64)
    team = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=64, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    language = models.CharField(
        max_length = 64,
        choices = LANGUAGES,
        default = 'English',
        blank=True
    )

    def __str__(self):
        return self.company

class WorkInfoInline(admin.TabularInline):
    model = WorkInfo

class Address(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    work = models.ForeignKey(WorkInfo, on_delete=models.DO_NOTHING, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True)
    street_extra = models.CharField(max_length=256, blank=True)
    suite = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=64, blank=True)
    post_code = models.CharField(max_length=16, blank=True)
    province = models.CharField(max_length=64, blank=True)
    in_date = models.DateField(blank=True, null=True)
    out_date = models.DateField(blank=True, null=True)
    country = models.CharField(
        max_length=64,
        choices = COUNTRIES,
        default = 'Canada',
        blank = True
    )
    type = models.CharField(
        max_length = 12, 
        choices = [('work','work'), ('home', 'home')], 
        default = 'home'
    )
    language = models.CharField(
        max_length = 64,
        choices = LANGUAGES,
        default = 'English',
        blank=True
    )
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.city + "_" + str(self.id)

class AddressInline(admin.TabularInline):
    model = Address

class Date(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    type = models.CharField(
        max_length = 16, 
        choices = DATE_TYPES, 
        default = 'birthday'
    )
    year_only = models.CharField(max_length=4, blank=True)
    day_month_only = models.CharField(max_length=20, blank=True)
    calendar = models.CharField(
        max_length = 64, 
        choices = CALENDARS, 
        default = 'Western (Gregorian)'
    )
    alternate_representation = models.CharField(max_length=32, blank=True, help_text='If western representation is not appropriate.')
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.type

class DateInline(admin.TabularInline):
    model = Date

class Email(models.Model):
   contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
   work = models.ForeignKey(WorkInfo, on_delete=models.DO_NOTHING, blank=True, null=True)
   type = models.CharField(
        max_length = 12, 
        choices = [('work','work'), ('home', 'home')], 
        default = 'home'
    )
   email = models.EmailField()
   comment = models.CharField(max_length=64, blank=True)
   is_preferred = models.BooleanField(default=False)  ## Todo, business logic to only allow a single preferred email per contact

   def __str__(self):
        return self.email

class EmailInline(admin.TabularInline):
    model = Email

class File(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    file = models.FileField(max_length=150)
    comment = models.CharField(max_length=64, blank=True)
    language = models.CharField(
        help_text = 'Language used in the file.',
        max_length = 64,
        choices = LANGUAGES,
        default = 'English'
    )

    def __str__(self):
        return self.name

class FileInline(admin.TabularInline):
    model = File

class Language(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    language = models.CharField(
        help_text = 'A language this contact speaks.',
        max_length = 64,
        choices = LANGUAGES,
        default = 'English'
    )
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.language + '_' + str(self.id)

class LanguageInline(admin.TabularInline):
    model = Language

class Name(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64, blank=True)
    formatted_name = models.CharField(max_length=256, blank=True)
    prefix = models.CharField(max_length=32, blank=True)
    suffix = models.CharField(max_length=32, blank=True)
    language = models.CharField(
        max_length = 64,
        choices = LANGUAGES,
        default = 'English',
        blank=True
    )
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.given_name

class NameInline(admin.TabularInline):
    model = Name

class Nickname(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64)
    comment = models.CharField(max_length=64, blank=True)
    language = models.CharField(
        max_length = 64,
        choices = LANGUAGES,
        default = 'English',
        blank=True
    )

    def __str__(self):
            return self.nickname

class NicknameInline(admin.TabularInline):
    model = Nickname

class Phone(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    work = models.ForeignKey(WorkInfo, on_delete=models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(
        max_length = 12, 
        choices = [('work','work'), ('home', 'home'), ('cell', 'mobile'), ('text', 'text'), ('voice', 'voice'), ('fax', 'fax'), ('pager', 'pager')], 
        default = 'cell'
    )
    phone = models.CharField(max_length=64)
    comment = models.CharField(max_length=64, blank=True)
    is_preferred = models.BooleanField(default=False)  ## Todo, business logic to only allow a single preferred email per contact

    def __str__(self):
        return self.phone

class PhoneInline(admin.TabularInline):
    model = Phone

class Relationship(models.Model):
    owner = models.ForeignKey(Contact, related_name='relationship_owner', on_delete=models.CASCADE)
    related = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    type = models.CharField(
        max_length = 40, 
        choices = RELATIONSHIPS, 
        default = 'friend'
    )
    is_emergency_contact = models.BooleanField(default=False)
    comment = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.type + '_' + str(self.id)

class RelationshipInline(admin.TabularInline):
    model = Relationship

class Social(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    type = models.CharField(
        max_length = 32, 
        choices = SOCIALS, 
        default = 'Facebook'
    )
    value = models.CharField(max_length=256, help_text='Link, username or other relevant relevant info.')
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.type + '_' + str(self.id)

class SocialInline(admin.TabularInline):
    model = Social

class ContactAdmin(admin.ModelAdmin):
    inlines = [
        EmailInline,
        PhoneInline,
        NicknameInline,
        AddressInline,
        DateInline,
        NameInline,
        AddressInline,
        LanguageInline,
        WorkInfoInline,
        FileInline,
        SocialInline,
        RelationshipInline
    ]