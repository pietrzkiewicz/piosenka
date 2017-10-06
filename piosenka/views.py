from datetime import datetime

from django.views.generic import TemplateView
from django.contrib.auth.models import User

from articles.models import Article
from blog.models import Post
from events.models import Event, get_events_for
from songs.models import ArtistNote, SongNote, Song


class SiteIndex(TemplateView):
    template_name = 'frontpage/index.html'
    POST_COUNT = 1
    SONG_COUNT = 8
    ANNOTATION_COUNT = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = (Article.items_visible_to(self.request.user)
                                 .order_by('-pub_date').first())
        context['events'] = get_events_for(self.request.user)
        context['posts'] = (Post.items_visible_to(self.request.user)
                            .order_by('-pub_date')[:SiteIndex.POST_COUNT])
        context['songs'] = (Song.items_visible_to(self.request.user)
                            .order_by('-pub_date')[:SiteIndex.SONG_COUNT])
        context['annotation'] = (SongNote.items_visible_to(self.request.user)
                                 .order_by('-pub_date').first())
        context['annotations'] = (
            SongNote.items_visible_to(self.request.user)
            .order_by('-pub_date')[:SiteIndex.ANNOTATION_COUNT])
        return context


class About(TemplateView):
    ARTICLE_FACTOR = 5
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = []
        for user in User.objects.filter(is_active=True):
            author = {}
            author['user'] = user
            author['annotations'] = SongNote.items_live().filter(
                author=user).count() + ArtistNote.items_live().filter(
                    author=user).count()
            author['songs'] = Song.items_live().filter(author=user).count()
            author['articles'] = Article.items_live().filter(
                author=user).count()
            author['total'] = (
                author['annotations'] + author['songs'] +
                self.ARTICLE_FACTOR * author['articles'])
            if author['total']:
                authors.append(author)
        context['authors'] = sorted(
            authors, key=lambda k: k['total'], reverse=True)
        return context


class Format(TemplateView):
    template_name = 'format.generated'


class Search(TemplateView):
    template_name = 'search.html'
