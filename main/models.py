import operator
import datetime
from django import forms
from django.db import models
from django.forms import ModelForm, widgets
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import render
from taggit.managers import TaggableManager
from django.forms.widgets import SplitDateTimeWidget
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from formtools.preview import FormPreview
from main.utils import in_current_semester

# Imported for image name creation
import os
from uuid import uuid4
# Create your models here.

# This class represents a student in RCSA
class Student(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    # This is the school year you entered
    year = models.CharField(max_length=200)

    # This is every student's SID
    sid = models.IntegerField()


    ROCKEFELLER = 'R'
    CHAVEZ = 'C'
    SAVIO = 'S'
    APPERSON = 'A'
    NONE = 'N'

    RCSA_HOUSE_CHOICES = (
        (ROCKEFELLER, "Rockefeller"),
        (CHAVEZ, "Chavez"),
        (SAVIO, "Savio"),
        (APPERSON, "Apperson"),
        (NONE, "Not Applicable"))


    house = models.CharField(max_length=1,
                            choices=RCSA_HOUSE_CHOICES)

    @property
    def house_name(self):
        if self.house == "R":
            return "Rockefeller"
        if self.house == "C":
            return "Chavez"
        if self.house == "S":
            return "Savio"
        if self.house == "A":
            return "Apperson"

    # This method returns a sorted list of scholars by the
    # house points they've contributed.
    @staticmethod
    def all_scholars_hp():
        events = Event.objects.all()
        students = Student.objects.all()
        student_points = dict()
        for student in students:
            student_points[student] = 0

        for event in events:
            if not event.house_points or not in_current_semester(event.date):
                continue
            attendees = event.attendees.all()
            for attendee in attendees:
                student_points[attendee] += 1


        sorted_student_points_tup = sorted(student_points.iteritems(),
            key=operator.itemgetter(1), reverse=True)
        sorted_student_points = []

        for student_tup in sorted_student_points_tup:
            student = student_tup[0]
            student_name = student.first_name + " " + student.last_name
            sorted_student_points.append([student_name, student_tup[1]])
        return (sorted_student_points_tup, sorted_student_points)

    def __unicode__(self):
        return self.first_name + " " + self.last_name



class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    date = models.DateTimeField('Date and Time', default=timezone.now)

    attendees = models.ManyToManyField(Student)

    house_points = models.BooleanField()

    @property
    def num_attendees(self):
        return self.attendees.count()

    @staticmethod
    def all_events_attendance():
        events = list(filter(lambda event: in_current_semester(event.date), Event.objects.all()))
        sorted_events = sorted(events, key=lambda event: event.num_attendees, reverse = True)
        return sorted_events

    @staticmethod
    def all_events_time():
        return list(Event.objects.order_by("-date"))

    @staticmethod
    def events_by_semester():
        events_per_semester = {}
        for event in Event.objects.order_by("-date"):
            semester = ""
            date = event.date
            semester += str(date.year)
            if date.month in range(1, 6):
                semester = "Spring " + semester
            elif date.month in range(8, 13):
                semester = "Fall " + semester
            else:
                # It should never reach this case.
                print("I am not here. Trust me.")
            if semester in events_per_semester:
                events_per_semester[semester].append(event)
            else:
                events_per_semester[semester] = [event]
        return events_per_semester


    def __unicode__(self):
        return self.name


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['attendees']
        widgets = {
            'date' : SplitDateTimeWidget()
        }


# This class is for House Points given out not for attendance at events
class HousePointsOther(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    points_R = models.IntegerField()
    points_C = models.IntegerField()
    points_S = models.IntegerField()
    points_A = models.IntegerField()
    date = models.DateTimeField('Date and Time', null=True, default=timezone.now)

    def __unicode__(self):
        return self.name

    @staticmethod
    def hpa_by_semester():
        hpa_per_semester = {}
        for hpa in HousePointsOther.objects.order_by("-date"):
            semester = ""
            date = hpa.date
            semester += str(date.year)
            if date.month in range(1, 6):
                semester = "Spring " + semester
            elif date.month in range(8, 13):
                semester = "Fall " + semester
            else:
                # It should never reach this case.
                print("I am not here. Trust me.")
            if semester in hpa_per_semester:
                hpa_per_semester[semester].append(hpa)
            else:
                hpa_per_semester[semester] = [hpa]
        return hpa_per_semester


class HousePointsOtherForm(ModelForm):
    class Meta:
        model = HousePointsOther
        fields = ['name', 'description', 'points_R', 'points_C', 'points_S', 'points_A', 'date']
        widgets = {
            'date' : SplitDateTimeWidget()
        }


@deconstructible
class PlacePicture(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        image_path = os.path.join(self.path,
            "{0}.{1}".format(instance.name, ext))
        return image_path


place_picture = PlacePicture("img/scholar_contacts")


class ScholarContactProfile(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    majors = models.CharField(max_length=200)
    minors = models.CharField(max_length=200, blank=True)
    opt_out = models.BooleanField(default=False)

    #change year choices to freshman - grad year?
    #so then it'd be probably be a positiveSmallIntegerField
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1000),
                                      MaxValueValidator(10000)])

    #combine these into two
    interests_extracurriculars = models.TextField()
    blurb = models.TextField()
    tags = TaggableManager(blank=True)

    @property
    def get_tags(self):
        return self.tags.names()

    @property
    def is_alumni(self):
        if (datetime.now().year > year):
            return True
        elif (datetime.now().year == year):
            return datetime.now().month > 4
        else:
            return False

    picture = models.ImageField(
            upload_to=place_picture, null=True, blank=True)


    def __unicode__(self):
        return self.name + "'s Profile"

class ScholarContactProfileForm(ModelForm):
    tag_options = (
        ("Engineering", "Engineering"), ("Computer Science", "Computer Science"),
        ("Biology", "Biology"), ("Pre-med", "Pre-med"),
        ("Business&Pre-Haas", "Business&Pre-Haas"), ("Dance", "Dance"),
        ("Music", "Music"), ("Research", "Research"),
        ("Pre-law", "Pre-law"), ("Art", "Art"),
        ("Humanities", "Humanities"), ("CNR", "CNR"),
        ("Chemistry", "Chemistry"),
        ("ASUC", "ASUC"), ("Greek life", "Greek life"),
        ("Community Service", "Community Service"), ("Intramural Sports", "Intramural Sports"))
    tags = forms.MultipleChoiceField(choices=tag_options, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = ScholarContactProfile

        fields = ['name', 'email', 'opt_out', 'majors', 'minors', 'year', 'interests_extracurriculars',
            'blurb', 'picture']

        labels = {
                'majors': _('Major(s)'),
                'minors': _('Minor(s)'),
                'year': _('Expected Year of Graduation'),
                'interests_extracurriculars': _('Interests and Extracurriculars'),
                'opt_out': _('I do not want to be contacted by prospective scholars.'),
                }


class ScholarContactProfileFormPreview(FormPreview):
    form_template = 'create_scholar_profile.html'
    preview_template = 'sc_profile_preview.html'

    def process_preview(self, request, form, context):
        form = ScholarContactProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            old_profile_name = ScholarContactProfile.objects.filter(name=profile.name)
            if old_profile_name:
                old_profile_name[0].delete()
            else:
                old_profile_email = ScholarContactProfile.objects.filter(email=profile.email)
                if old_profile_email:
                    old_profile_email[0].delete()
            profile.save()
            for tag in form.cleaned_data['tags']:
                profile.tags.add(str(tag))
            profile.save()
            context['student'] = profile
            context['form'] = form

    def done(self, request, cleaned_data):
        success = True
        return render(request, 'create_scholar_profile.html', {'success':success})

class ScholarContactProfileView(models.Model):
    scholar_contact_profile = models.ForeignKey(ScholarContactProfile)
    ip = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)


class FAQEntry(models.Model):
    question = models.TextField()
    answer = models.TextField()

    CATEGORIES = (
        ("Regents' Scholarship", "Regents' Scholarship"),
        ("Academic", "Academic"),
        ("Social", "Social"))

    category = models.CharField(max_length=25, choices=CATEGORIES)

    def __unicode__(self):
        return self.question

class FAQForm(ModelForm):
    class Meta:
        model = FAQEntry
        fields = ['category', 'question', 'answer',]
