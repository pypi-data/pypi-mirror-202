from muid import MUID
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def muid_validator(value):
    try:
        MUID(value)
    except (TypeError, ValueError):
        raise ValidationError(
            _("“%(value)s” is not a valid MUID."),
            code="invalid",
            params={"value": value},
        )
