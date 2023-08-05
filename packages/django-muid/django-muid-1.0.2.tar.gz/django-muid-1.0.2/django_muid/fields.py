from django.db.models import Field
from .muid import MUID
from .validators import muid_validator

class MUIDField(Field):
    description = "MUID field"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 16)
        super().__init__(*args, **kwargs)
        self.validators.append(muid_validator)

    @staticmethod
    def generate_value(instance):
        return MUID()

    def get_internal_type(self):
        return 'CharField'

    @staticmethod
    def from_db_value(value, expression, connection):
        if value is None:
            return value
        return MUID(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, MUID):
            value = self.to_python(value)
        return value.id

    def to_python(self, value):
        if value is not None and not isinstance(value, MUID):
            try:
                value = MUID(value)
            except (TypeError, ValueError):
                raise ValidationError(
                    self.error_messages["invalid"],
                    code="invalid",
                    params={"value": value},
                )
        return value

    def value_to_string(self, obj):
        return str(obj)
