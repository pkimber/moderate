from django.conf import settings
from django.db import models

import reversion


def default_moderate_state():
    return ModerateState.pending()


class ModerateState(models.Model):
    """Accept, remove or pending.

    Copy of class in `story.models'.

    """
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

    def set_pending(self):
        self.moderate_state = ModerateState.pending()

    def set_published(self):
        self.moderate_state = ModerateState.published()

    def set_removed(self):
        self.moderate_state = ModerateState.removed()

    def _pending(self):
        return self.moderate_state == ModerateState.pending()
    pending = property(_pending)

    def _published(self):
        return self.moderate_state == ModerateState.published()
    published = property(_published)
