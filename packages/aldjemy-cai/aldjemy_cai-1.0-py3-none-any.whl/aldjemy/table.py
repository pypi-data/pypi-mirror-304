from django.apps import apps
from django.conf import settings
from django.db.models.fields.related import OneToOneField, ManyToManyField
from sqlalchemy import Column, ForeignKey, Table, types
from sqlalchemy.dialects.postgresql import ARRAY, DATERANGE, JSONB
from sqlalchemy import UUID
from django.db import models as django_models


def simple(typ):
    return lambda field: typ()


def varchar(field):
    return types.String(length=field.max_length)


def foreign_key(field):
    parent_model = field.related_model
    target = parent_model._meta
    target_table = target.db_table
    target_pk = target.pk.column
    if isinstance(parent_model._meta.pk, django_models.UUIDField):
        return UUID(as_uuid=True), ForeignKey("%s.%s" % (target_table, target_pk))
    return types.Integer, ForeignKey("%s.%s" % (target_table, target_pk))


def array_type(field):
    """
    Allows conversion of Django ArrayField to SQLAlchemy Array.
    Takes care of mapping the type of the array element.
    """
    internal_type = field.base_field.get_internal_type()

    # currently no support for multi-dimensional arrays
    if internal_type in DATA_TYPES and internal_type != "ArrayField":
        sub_type = DATA_TYPES[internal_type](field)
    else:
        raise RuntimeError("Unsupported array element type")

    return ARRAY(sub_type)


DATA_TYPES = {
    "AutoField": simple(types.Integer),
    "BigAutoField": simple(types.BigInteger),
    "BooleanField": simple(types.Boolean),
    "CharField": varchar,
    "CommaSeparatedIntegerField": varchar,
    "DateField": simple(types.Date),
    "DateTimeField": simple(types.DateTime),
    "DecimalField": lambda field: types.Numeric(
        scale=field.decimal_places, precision=field.max_digits
    ),
    "DurationField": simple(types.Interval),
    "FileField": varchar,
    "FilePathField": varchar,
    "FloatField": simple(types.Float),
    "IntegerField": simple(types.Integer),
    "BigIntegerField": simple(types.BigInteger),
    "IPAddressField": lambda field: types.CHAR(length=15),
    "NullBooleanField": simple(types.Boolean),
    "OneToOneField": foreign_key,
    "ForeignKey": foreign_key,
    "PositiveIntegerField": simple(types.Integer),
    "PositiveSmallIntegerField": simple(types.SmallInteger),
    "SlugField": varchar,
    "SmallIntegerField": simple(types.SmallInteger),
    "TextField": simple(types.Text),
    "TimeField": simple(types.Time),
    # PostgreSQL-specific types
    "ArrayField": array_type,
    "UUIDField": simple(UUID),
    "JSONField": simple(JSONB),
    "DateRangeField": simple(DATERANGE),
}


def generate_tables(metadata):
    # Update with user specified data types
    COMBINED_DATA_TYPES = dict(DATA_TYPES)
    COMBINED_DATA_TYPES.update(getattr(settings, "ALDJEMY_DATA_TYPES", {}))

    models = apps.get_models(include_auto_created=True)
    for model in models:
        name = model._meta.db_table
        qualname = (metadata.schema + "." + name) if metadata.schema else name
        if qualname in metadata.tables or model._meta.proxy:
            continue
        columns = []
        model_fields = [
            (f, f.model if f.model != model else None)
            for f in model._meta.get_fields()
            if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)
        ]
        private_fields = model._meta.private_fields
        for field, parent_model in model_fields:
            if field not in private_fields:
                if parent_model:
                    continue

                try:
                    internal_type = field.get_internal_type()
                except AttributeError:
                    continue

                if internal_type in COMBINED_DATA_TYPES and hasattr(field, "column"):
                    typ = COMBINED_DATA_TYPES[internal_type](field)
                    if not isinstance(typ, (list, tuple)):
                        typ = [typ]
                    default_value = _maybe_add_default_value(model, field)
                    if default_value is not None:
                        column = Column(
                            field.column,
                            *typ,
                            primary_key=field.primary_key,
                            default=default_value
                        )
                    else:
                        column = Column(
                            field.column,
                            *typ,
                            primary_key=field.primary_key
                        )

                    columns.append(column)
        Table(name, metadata, *columns)


def _maybe_add_default_value(model, field):
    # Handle default values
    internal_type = field.get_internal_type()
    default_value = None

    # Ignore relationship fields
    if isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
        return default_value  # Skip relationship fields for default value

    # If a field is nullable, do not assign default value.
    if field.null:
        return default_value

    if hasattr(field, 'default') and field.default is not django_models.NOT_PROVIDED:
        default = field.default
        if not callable(default) or is_simple_callable(default):
            default_value = default
        else:
            raise Exception(f"Callable function not handled for model: {model._meta.model_name} field: {field.name}")
    elif internal_type == "DateTimeField":
        # Handle auto_now and auto_now_add for DateTimeField
        if getattr(field, 'auto_now', False):
            from sqlalchemy.sql import func
            default_value = func.now()
        elif getattr(field, 'auto_now_add', False):
            from sqlalchemy.sql import func
            default_value = func.now()
        else:
            raise Exception(
                f"DateTimeField default function not handled for model: {model._meta.model_name} field: {field.name}")
    elif internal_type in ("CharField", "TextField", "ImageField") and getattr(field, 'blank', False):
        default_value = ""
    return default_value


def is_simple_callable(value):
    """Check if a callable can be called without arguments."""
    if callable(value):
        try:
            value()  # Try to call the callable without arguments
            return True
        except Exception:
            return False
    return False
