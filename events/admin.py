from django.contrib import admin
from events.models import Participant, Category, Event

admin.site.register(Event),
admin.site.register(Category),
admin.site.register(Participant),
# Register your models here.
