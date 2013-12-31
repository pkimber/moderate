from datetime import datetime

from django.conf import settings
from django.db import models

import reversion


class ModerateError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


def default_moderate_state():
    return ModerateState.pending()


class ModerateState(models.Model):
    """Accept, remove or pending."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Moderate'
        verbose_name_plural = 'Moderated'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    @staticmethod
    def pending():
        return ModerateState.objects.get(slug='pending')

    @staticmethod
    def published():
        return ModerateState.objects.get(slug='published')

    @staticmethod
    def removed():
        return ModerateState.objects.get(slug='removed')

reversion.register(ModerateState)


class ModerateModel(models.Model):
    """
    An abstract base class model that allows simple moderation.
    """
    moderate_state = models.ForeignKey(
        ModerateState,
        default=default_moderate_state
    )
    date_moderated = models.DateTimeField(blank=True, null=True)
    user_moderated = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )

    class Meta:
        abstract = True
        unique_together = ('section', 'moderate_state')

    def _is_pending(self):
        return self.moderate_state == ModerateState.pending()
    is_pending = property(_is_pending)

    def _is_published(self):
        return self.moderate_state == ModerateState.published()
    is_published = property(_is_published)

    def _is_removed(self):
        return self.moderate_state == ModerateState.removed()
    is_removed = property(_is_removed)

    def _set_moderated(self, user, moderate_state):
        self.date_moderated = datetime.now()
        self.user_moderated = user
        self.moderate_state = moderate_state

    def set_pending(self, user):
        self._set_moderated(user, ModerateState.pending())

    def set_published(self, user):
        self._set_moderated(user, ModerateState.published())

    def set_removed(self, user):
        self._set_moderated(user, ModerateState.removed())
