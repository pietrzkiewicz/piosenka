from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, RedirectView, TemplateView
from django.http import Http404

from artists.models import Entity
from events.models import EntityPerformance, Event, Venue
from events.forms import EventForm, PerformanceFormSet
from events.mixins import EventMenuMixin
from content.trevor import put_text_in_trevor
from content.views import (AddContentView, EditContentView, ApproveContentView,
                           ReviewContentView, ViewContentView)


class GetEventMixin(object):
    def get_object(self):
        import time
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']
        date_stamp = time.strptime(year+month+day, "%Y%m%d")
        event_date = datetime.fromtimestamp(time.mktime(date_stamp))
        return Event.objects.get(slug=slug,
                                 datetime__year=event_date.year,
                                 datetime__month=event_date.month,
                                 datetime__day=event_date.day)


class EventIndex(EventMenuMixin, TemplateView):
    template_name = "events/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.items_visible_to(self.request.user)\
                                 .filter(datetime__gte=datetime.now())\
                                 .order_by('datetime')
        return context


class VenueDetail(DetailView):
    model = Venue
    context_object_name = "venue"
    template_name = "events/venue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.items_visible_to(self.request.user)\
                                 .filter(venue=self.object)\
                                 .order_by('datetime')
        return context


class EntityDetail(DetailView):
    model = Entity
    context_object_name = "entity"
    template_name = "events/entity.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().still_plays:
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = [x.event for x in
                             EntityPerformance.objects.filter(
                                 entity=self.object)
                             if x.event.can_be_seen_by(self.request.user)]
        return context


class ViewEvent(GetEventMixin, ViewContentView):
    model = Event
    context_object_name = "event"
    template_name = "events/event.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True


class MonthArchiveRedirect(RedirectView):
    """ Redirect for the per-month archives which were replaced by per-year
    archives. """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('event_year', kwargs={'year': kwargs['year']})


class YearArchive(TemplateView):
    template_name = "events/year.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.items_visible_to(self.request.user)\
                                 .filter(datetime__year=kwargs['year'])
        context['year'] = kwargs['year']
        return context


class AddEvent(AddContentView):
    model = Event
    form_class = EventForm
    formset_classes = [("entityperformance", PerformanceFormSet)]
    template_name = "events/add_edit_event.html"

    def get_initial(self):
        initial_description = """Tutaj opisz wydarzenie. Zaznacz fragment tekstu
        aby dodać **pogrubienie** albo [odsyłacz](#)."""
        return {
            'description_trevor': put_text_in_trevor(initial_description)
        }

    def form_valid(self, form, formsets):
        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.combine(form.cleaned_data['date'],
                                                  form.cleaned_data['time'])
        return super().form_valid(form, formsets)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditEvent(GetEventMixin, EditContentView):
    model = Event
    form_class = EventForm
    formset_classes = [("entityperformance", PerformanceFormSet)]
    template_name = "events/add_edit_event.html"

    def get_initial(self):
        return {
            'date': self.object.datetime.strftime("%d.%m.%Y"),
            'time': self.object.datetime.strftime("%H:%M"),
            'venue_selection': self.object.venue,
            'description_trevor': self.object.description_trevor,
        }

    def form_valid(self, form, formsets):
        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.combine(form.cleaned_data['date'],
                                                  form.cleaned_data['time'])
        return super().form_valid(form, formsets)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewEvent(GetEventMixin, ReviewContentView):
    pass


class ApproveEvent(GetEventMixin, ApproveContentView):
    pass
