import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import MonthArchiveView, DateDetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from unidecode import unidecode

from artists.models import Artist, Band
from events.models import Event, Venue
from events.forms import EventForm

class VenueDetail(DetailView):
    model = Venue
    context_object_name = "venue"
    template_name = "events/venue_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VenueDetail, self).get_context_data(**kwargs)
        context['model_meta'] = Venue._meta
        return context

class EventDetail(DateDetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_detail.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == object.author)
        return context

class EventIndex(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_index.html"
    queryset = Event.current.all()
    VENUE_COUNT = 10
    def get_context_data(self, **kwargs):
        context = super(EventIndex, self).get_context_data(**kwargs)
        from django.db.models import Count
        context['popular_venues'] = Venue.objects.all() \
                                                 .annotate(event_count=Count('event')) \
                                                 .order_by('-event_count')[:EventIndex.VENUE_COUNT]
        return context


class EventMonthArchive(MonthArchiveView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_month_archive.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True
    allow_empty = True

class AddEvent(CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"
    success_url = reverse_lazy('event_index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        form.instance.slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.author = self.request.user
        return super(AddEvent, self).form_valid(form)

class EditEvent(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"

    date_field = "datetime"
    month_format = "%m"
    allow_future = True

    def get_object(self):
        import datetime, time
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']
        date_stamp = time.strptime(year+month+day, "%Y%m%d")
        event_date = datetime.date(*date_stamp[:3])
        return Event.objects.get(slug=slug,
                                 datetime__year=event_date.year,
                                 datetime__month=event_date.month,
                                 datetime__day=event_date.day)


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        event = self.get_object()
        if not (self.request.user.is_staff or self.request.user == event.author):
            raise Http404
        return super(EditEvent, self).dispatch(*args, **kwargs)

    def get_initial(self):
        return {
            'date': self.object.datetime,
            'time': self.object.datetime,
            'venue_selection': self.object.venue,
            'description_trevor': self.object.description_trevor,
        }

    def form_valid(self, form):
        venue = form.cleaned_data['venue_selection']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        form.instance.slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.pk = self.object.pk
        return super(EditEvent, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
