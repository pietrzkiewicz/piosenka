import datetime

from django.contrib.auth.models import User
from django.db import models


class LiveContentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reviewed=True)


class ContentItem(models.Model):
    """ A class that extends this has to have:
     - objects default manager
     - live manager (LiveContentManager above) """

    # Cards are item types that are displayed alongside the parent item. They
    # don't have an absolute url of their own, but defer to the parent instead.
    is_card = False

    author = models.ForeignKey(User, editable=False)
    reviewed = models.BooleanField(default=False, editable=False)
    pub_date = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = datetime.datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def items_visible_to(cls, user):
        """Returns the manager representing the set of instances visible to the
        particular user.
        """
        # TODO call this objects_visible_to as it returns a manager, not items.
        if user and user.is_authenticated():
            return cls.objects
        return cls.live

    @classmethod
    def items_reviewable_by(cls, user):
        if user and user.is_authenticated() and user.has_perm('content.review'):
            return cls.objects.filter(reviewed=False).exclude(author=user)
        else:
            return []

    def can_be_seen_by(self, user):
        return self.is_live() or (user.is_active and user.is_authenticated())

    def can_be_edited_by(self, user):
        return (user.is_active and
                user.is_authenticated() and
                (user == self.author or user.has_perm('content.review')))

    def can_be_approved_by(self, user):
        return (not self.is_live() and
                user.is_active and
                user.is_authenticated() and
                user.has_perm('content.review') and
                user != self.author)

    def is_live(self):
        return self.reviewed

    def status_str(self):
        return "opublikowany" if self.reviewed else "w korekcie"


class Permissions(models.Model):
    """Dummy model used to define additional permissions not tied to a
    particular model.
    """

    class Meta:
        permissions = [('review', 'Can review content items.')]
