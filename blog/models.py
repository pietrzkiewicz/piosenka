import uuid

from django.core.urlresolvers import reverse_lazy
from django.db import models

from content.trevor import render_trevor, put_text_in_trevor
from content.models import ContentItem
from content.slug import SlugFieldMixin


class Post(SlugFieldMixin, ContentItem):
    HELP_TITLE = "Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'."

    title = models.CharField(max_length=100,
                             help_text=HELP_TITLE)
    post_trevor = models.TextField()
    more_trevor = models.TextField(null=True, blank=True)

    post_html = models.TextField(null=True, editable=False)
    more_html = models.TextField(null=True, editable=False)

    @staticmethod
    def create_for_testing(author):
        post = Post()
        post.author = author
        post.title = str(uuid.uuid4()).replace("-", "")
        post.post_trevor = put_text_in_trevor("Abc")
        post.more_trevor = put_text_in_trevor("Abc")
        post.save()
        return post

    class Meta(ContentItem.Meta):
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    # SlugFieldMixin:
    def get_slug_elements(self):
        assert self.title
        return [self.title]

    def save(self, *args, **kwargs):
        self.post_html = render_trevor(self.post_trevor)
        if self.more_trevor:
            self.more_html = render_trevor(self.more_trevor)
        else:
            self.more_html = ""
        super().save(*args, **kwargs)

    def get_url_params(self):
        return {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug
        }

    @staticmethod
    def get_add_url():
        return str(reverse_lazy('add_post'))

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), self.get_url_params())

    @models.permalink
    def get_edit_url(self):
        return ('edit_post', (), self.get_url_params())

    @models.permalink
    def get_review_url(self):
        return ('review_post', (), self.get_url_params())

    @models.permalink
    def get_approve_url(self):
        return ('approve_post', (), self.get_url_params())
