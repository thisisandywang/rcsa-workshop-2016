from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from haystack.forms import HighlightedSearchForm
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from main.views import SearchViewSCGrid, SearchViewFAQ
from main.models import ScholarContactProfileFormPreview, ScholarContactProfileForm
from django import forms

# For password protection
from password_required.decorators import password_required

from main.models import ScholarContactProfile, FAQEntry

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^about/$', 'main.views.about', name='about'),
    url(r'^association/$', 'main.views.association', name='the_association'),
    url(r'^scholarship/$', 'main.views.scholarship', name='the_scholarship'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^student_services/test_bank$', 'main.views.test_bank', name='test_bank'),
    url(r'^student_services/yearbook$', 'main.views.yearbook', name='yearbook'),
    url(r'^student_services/newsletters$', 'main.views.newsletters', name='newsletters'),
    url(r'^student_services$', 'main.views.student_services', name='student_services'),
    url(r'^rohp$', 'main.views.rohp_prospect', name='rohp_prospect'),
    url(r'^rohp_prospect$', 'main.views.rohp_prospect', name='rohp_prospect'),
    url(r'^get-involved/committees$', 'main.views.committees', name='committees'),  
    url(r'^yearbook$', 'main.views.yearbook', name='yearbook'),
    url(r'^leadership/$', 'main.views.leadership'),
    url(r'^get-involved/leadership$', 'main.views.leadership', name='leadership'),
    url(r'^dashboard/$', 'main.views.dashboard'),
    url(r'^sign-in/(?P<event_pk_attempt>.*)$', 'main.views.signin'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^dashboard/choose-event$', 'main.views.choose_event'),
    url(r'^dashboard/all-events/(?P<modify>modify)?$', 'main.views.all_events'),
    url(r'^dashboard/event_info/(?P<event_pk>.*)$', 'main.views.event_info'),
    url(r'^dashboard/house-point-additions/(?P<modify>modify)?$', 'main.views.house_point_additions'),
    url(r'^dashboard/all-scholars$', 'main.views.all_scholars'),
    url(r'^dashboard/event/(?P<event_pk>.*)$', 'main.views.event'),
    url(r'^dashboard/house-point-addition/(?P<name>.*)$', 'main.views.house_point_addition'),
    url(r'^dashboard/student/(?P<student_email>.*)$', 'main.views.events_attended'),
    url(r'^scholarconnect/sc-profile/(?P<student_name>.*)$', 'main.views.sc_profile', name='sc_profile'),
    url(r'^submit[Ff][Aa][Qq]/$', 'main.views.submit_FAQ'),
    url(r'^createprofile/$', ScholarContactProfileFormPreview(ScholarContactProfileForm)),
    url(r'^password_required/$', 'password_required.views.login'),
    url(r'^scholarconnect/$', 'main.views.sc_init', name='scholarconnect'),
)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^scholarconnect/cs-results/.*$', password_required(SearchViewSCGrid(
        template='sc_cs_profile_grid.html',
        searchqueryset=SearchQuerySet().models(ScholarContactProfile),
        form_class=HighlightedSearchForm,
        results_per_page=10
    )),),
)

urlpatterns += patterns('',
    url(r'^scholarconnect/ps-results/.*$', password_required(SearchViewSCGrid(
        template='sc_ps_profile_grid.html',
        searchqueryset=SearchQuerySet().models(ScholarContactProfile).filter(opt_out=False),
        form_class=HighlightedSearchForm,
        results_per_page=10
    )),),
)

urlpatterns += patterns('',
    url(r'^scholarconnect-FAQ/$', password_required(SearchViewFAQ(
        template='sc_FAQ.html',
        searchqueryset=SearchQuerySet().models(FAQEntry),
        form_class=HighlightedSearchForm,
        results_per_page=10
    )),),
)
