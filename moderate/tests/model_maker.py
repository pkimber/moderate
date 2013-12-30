from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from moderate.models import (
    ModerateState,
)


def make_moderate_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(unicode(name)),
    )
    defaults.update(kwargs)
    return clean_and_save(ModerateState(**defaults))
