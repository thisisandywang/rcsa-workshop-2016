from django.contrib import admin
from main.models import Student, Event, HousePointsOther, ScholarContactProfile, FAQEntry, ScholarContactProfileView
# Register your models here.

admin.site.register(Student)
admin.site.register(Event)
admin.site.register(HousePointsOther)
admin.site.register(ScholarContactProfile)
admin.site.register(FAQEntry)
admin.site.register(ScholarContactProfileView)
