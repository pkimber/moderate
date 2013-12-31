from moderate.models import (
    ModerateState,
)
from moderate.tests.model_maker import (
    make_moderate_state,
)


def default_moderate_state():
    try:
        ModerateState.pending()
    except ModerateState.DoesNotExist:
        make_moderate_state('pending')
    try:
        ModerateState.published()
    except ModerateState.DoesNotExist:
        make_moderate_state('published')
    try:
        ModerateState.removed()
    except ModerateState.DoesNotExist:
        make_moderate_state('removed')
