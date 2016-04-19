from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from external import google
# For the login
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# For paging the scholar connect database
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from main.models import Student, Event, HousePointsOther, EventForm, HousePointsOtherForm, ScholarContactProfile, \
                        FAQEntry, FAQForm, ScholarContactProfileForm, ScholarContactProfileView

from main.utils import in_current_semester

import random

import haystack.views

from datetime import datetime, tzinfo

# Create your views here.

def home(request):
    return render(request,
        'home.html',
        {'events':google.fetch_google_cal_events()})

def test_bank(request):
    return render(
        request,
        'test_bank.html')

def yearbook(request):
    return render(
        request,
        'yearbook.html')

def newsletters(request):
    return render(
        request,
        'newsletters.html')

def error_page(request):
    return render(
        request,
        'error_page.html')

def student_services(request):
    return render(
        request,
        'student_services.html')

def about(request):
    return render(
        request,
        'about.html'
    )

def association(request):
    return render(
        request,
        'association.html'
    )

def scholarship(request):
    return render(
        request, 
        'scholarship.html'
    )

def rohp_prospect(request):
    return render(
        request,
        'rohp_prospect.html'
    )

def committees(request):
    return render(
        request,
        'committees.html'
    )

def leadership(request):
    return render(
        request,
        'leadership.html'
    )

def yearbook(request):
    return render(
        request,
        'yearbook.html'
    )

def sc_init(request):
    return render(
        request,
        'sc_init.html'
    )

def sc_cs_profile_grid(request):
    return render(
        request,
        'sc_cs_profile_grid.html'
    )

def sc_ps_profile_grid(request):
    return render(
        request,
        'sc_ps_profile_grid.html'
    )

def sc_FAQ(request):
    return render(
        request,
        'sc_FAQ.html'
    )

@login_required
def signin(request, event_pk_attempt):
    if (not event_pk_attempt):
        event = Event.objects.order_by("-date")[0]
    else:
        try:
            event = Event.objects.get(pk=event_pk_attempt)
        except Event.DoesNotExist:
            raise Http404

    state = ""
    if request.POST:
        email = request.POST.get('email').lower()
        house = request.POST.get('House')
        if house == 'N':
            non_scholar = Student(first_name="Not in",last_name="RCSA",
                sid=-1,email=email,house='N')
            non_scholar.save()
            event.attendees.add(non_scholar)
            state = "Success!"
        else:
            try:
                student = Student.objects.get(email=email)
                event.attendees.add(student)
                state = "Success!"
            except:
                state = "Failed. Try again."
    return render(request,
        'sign-in.html',
        {'state': state,
         'event':event})

@login_required
def dashboard(request):
    r_points, c_points, s_points, a_points = get_house_points()

    house_points = {"R":r_points,
                    "C":c_points,
                    "S":s_points,
                    "A":a_points}

    top_5_scholars = Student.all_scholars_hp()[1][:5]
    top_5_events = Event.all_events_attendance()[:5]
    user_name = request.user.first_name + " " + request.user.last_name

    return render(request,
        'dashboard.html',
        {"house_points":house_points,
         "top_5_scholars":top_5_scholars,
         "top_5_events":top_5_events,
         "user_name":user_name,
        })

@login_required
def choose_event(request):
    now = datetime.now()
    semester = str(now.year)
    if now.month in range(1, 6):
        semester = "Spring " + semester
    elif now.month in range(8, 13):
        semester = "Fall " + semester
    events = Event.events_by_semester()[semester]
    return render(request,
        'choose_event.html',
        {'events':events})

# Used to sort the semesters for events and house point additions
def sort_semesters(semester_event_pair):
    semester = semester_event_pair[0]
    semester_proper, year = semester.split(" ")
    val = float(year)
    if semester_proper == "Fall":
        val += .5
    return -val

@login_required
def all_events(request, modify):
    if modify:
        modify = True
    else:
        modify = False
    events_by_semester = Event.events_by_semester()
    semester_event_pair = [(semester, [event for event in events_by_semester[semester]]) for semester in events_by_semester.keys()]
    events_by_semester = sorted(semester_event_pair, key=sort_semesters)
    return render(request,
        'all_events.html',
        {'events_by_semester':events_by_semester,
         'modify':modify})


@login_required
def event_info(request, event_pk):
    if (not event_pk):
        event = Event.objects.order_by("-date")[0]
    else:
        try:
            event = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            raise Http404

    return render(request,
            'event_info.html',
            {'event': event})


@login_required
def house_point_additions(request, modify):
    if modify:
        modify = True
    else:
        modify = False
    hpa_by_semester = HousePointsOther.hpa_by_semester()
    semester_hpa_pair = [(semester, [hpa for hpa in hpa_by_semester[semester]]) for semester in hpa_by_semester.keys()]
    hpa_by_semester = sorted(semester_hpa_pair, key=sort_semesters)
    print(hpa_by_semester)
    return render(request,
        'house_point_additions.html',
        {'hpa_by_semester': hpa_by_semester,
         'modify':modify})

@login_required
def all_scholars(request):
    all_scholars = Student.all_scholars_hp()[0]
    return render(request,
        'all_scholars.html',
        {'all_scholars':all_scholars})

@login_required
def events_attended(request, student_email):
    # Select student
    # Go through all events, go through attendees variable
    # Check if your student is same as this student instance
    # If true, put that event inside a set or list and display
    events = Event.objects.all()
    student = Student.objects.get(email=student_email)
    first_name = student.first_name
    last_name = student.last_name
    total_events = []
    for event in events:
        if event.attendees.filter(email=student_email).exists():
            total_events.append(event)

    return render(request, 'events_attended.html',
        {'total_events':total_events,
        'name':student.first_name + ' ' + student.last_name
        })

def sc_profile(request, student_name):
    try:
        student = ScholarContactProfile.objects.get(name=student_name)
        if not ScholarContactProfileView.objects.filter(scholar_contact_profile=student, ip=request.META['REMOTE_ADDR'], created__day=datetime.now().day):
            view = ScholarContactProfileView(scholar_contact_profile=student,
                            ip=request.META['REMOTE_ADDR'],
                            created=datetime.now())
            view.save()
    except ScholarContactProfile.DoesNotExist:
        raise Http404
    return render(
        request,
        'sc_profile.html',
        {'student': student}
    )

current_event_pk = ''

@login_required
def event(request, event_pk):
    global current_event_pk
    if event_pk:
        current_event_pk = event_pk

    if request.POST:
        if current_event_pk:
            try:
                event = Event.objects.get(pk=current_event_pk)
                form = EventForm(request.POST, instance=event)
            except Event.DoesNotExist:
                raise Http404

        else:
            form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            current_event_pk = ''
            return HttpResponseRedirect('/dashboard')

    elif current_event_pk:
        try:
            event = Event.objects.get(pk=current_event_pk)
            form = EventForm(request.POST, instance=event)
        except Event.DoesNotExist:
            raise Http404
        form = EventForm(instance = event)
    else:
        form = EventForm()
    return render(request, 'event.html', {'form':form})

@login_required
def house_point_addition(request, name):
    if request.POST:
        if name:
            try:
                hpa = HousePointsOther.objects.get(name=name)
                form = HousePointsOtherForm(request.POST, instance=hpa)
            except Event.DoesNotExist:
                raise Http404
        else:
            form = HousePointsOtherForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard')
    elif not name:
        form = HousePointsOtherForm()
    elif name:
        try:
            hpa = HousePointsOther.objects.get(name=name)
            form = HousePointsOtherForm(request.POST, instance=hpa)
        except Event.DoesNotExist:
            raise Http404
        form = HousePointsOtherForm(instance=hpa)
    return render(request,
        'house_point_addition.html',
        {'form':form})

@login_required
def submit_FAQ(request):
    success = False
    if request.POST:
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = FAQForm()
    return render(request, 'submit_faq.html', {'form': form, 'success':success})

def create_scholar_profile(request):
    success = False
    if request.POST:
        form = ScholarContactProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            for tag in form.cleaned_data['tags']:
                profile.tags.add(str(tag))
            profile.save()
            success = True
    else:
        form = ScholarContactProfileForm()
    return render(request, 'create_scholar_profile.html', {'form': form, 'success':success})

# A function to calculate the house points.
def get_house_points():
    r_points, c_points, s_points, a_points = 0, 0, 0, 0

    events = Event.objects.all()
    other_house_points = HousePointsOther.objects.all()

    for event in events:
        if not event.house_points or not in_current_semester(event.date):
            continue
        event_attendees = event.attendees.all()

        for student in event_attendees:
            house = student.house
            if house == "N":
                break
            elif house == "R":
                r_points += 1
            elif house == "C":
                c_points += 1
            elif house == "S":
                s_points += 1
            elif house == "A":
                a_points += 1

    # for other in other_house_points:
    #     r_points += other.points_R
    #     c_points += other.points_C
    #     s_points += other.points_S
    #     a_points += other.points_A

    return (r_points, c_points, s_points, a_points)

class SearchViewSCGrid(haystack.views.SearchView):
    """
    We subclass haystack's SearchView class in order to pass extra context
    to our scholar contact profile grid (i.e. we pass it all of the scholar
        contact profiles).
    """

    def extra_context(self):
        actual_results = True
        multiple = False
        path = self.request.path
        path_components = path.split("/scholarconnect/")
        page_path = path_components[1].split('&page=')
        tags_path = page_path[0]
        if len(page_path) > 1:
            page = int(page_path[1])
        else:
            page = 1
        tags_list = tags_path.split("&tag=")

        if len(tags_list) > 1:
            if len(tags_list) > 2:
                multiple = True
            selected_profiles = ScholarContactProfile.objects.filter(tags__name__in=[str(tag) for tag in tags_list if not tag == ""]).distinct()
            if not self.request.session.get('random_seed', False):
                self.request.session['random_seed'] = random.randint(1, 10000)
            seed = self.request.session['random_seed']
            self.request.session.set_expiry(86400)
            random.seed(seed)
            selected_profiles = list(selected_profiles)
            random.shuffle(selected_profiles)
            if len(selected_profiles) == 0:
                actual_results = False
        else:
            selected_profiles = ScholarContactProfile.objects.all()

        profile_pages = Paginator(selected_profiles, 10)
        profiles = None
        try:
            profiles = profile_pages.page(page)
        except PageNotAnInteger:
            profiles = profile_pages.page(1)
        except EmptyPage:
            profiles = profile_pages.page(profile_pages.num_pages)

        all_tags = ScholarContactProfile.tags.all().order_by('name')
        return {'profiles': profiles,
                'actual_results': actual_results,
                'multiple': multiple,
                'tags_path':tags_path,
                'all_tags':all_tags}

class SearchViewFAQ(haystack.views.SearchView):
    """
    We subclass haystack's SearchView class in order to pass extra context
    to our scholar contact profile grid (i.e. we pass it all of the scholar
        contact profiles).
    """

    def extra_context(self):
        faqs_scholarship = FAQEntry.objects.filter(category="Regents' Scholarship")
        faqs_academic = FAQEntry.objects.filter(category="Academic")
        faqs_social = FAQEntry.objects.filter(category="Social")
        return {'faqs_scholarship': faqs_scholarship,
                'faqs_academic':faqs_academic,
                'faqs_social':faqs_social}
