from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.generic_tests import GenericTestsMixin
from songs.models import ArtistNote, Artist


class ArtistNoteTest(GenericTestsMixin, TestCase):
    item_cls = ArtistNote

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        author = testing.create_user()
        artist = Artist.create_for_testing(author)
        artist.featured = True
        artist.save()
        return artist.get_add_note_url()

    @overrides(GenericTestsMixin)
    def assertServedOk(self, item, response):
        self.assertContains(response, item.get_id(), html=False)

    @overrides(GenericTestsMixin)
    def assertNotServedOk(self, item, response):
        self.assertNotContains(response, item.get_id(), html=False)
