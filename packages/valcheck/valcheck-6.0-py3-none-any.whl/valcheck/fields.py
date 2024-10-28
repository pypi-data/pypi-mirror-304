from __future__ import annotations

from datetime import date, datetime, timezone
import random
from typing import Any, Callable, Iterable, List, Literal, Optional, Type, Union
import uuid

from valcheck.models import Error
from valcheck import utils


class ValidatedField:
    """Class that represents a validated field"""

    def __init__(
            self,
            *,
            field: Field,
            errors: List[Error],
        ) -> None:
        assert isinstance(field, Field), "Param `field` must be of type `valcheck.fields.Field`"
        assert utils.is_list_of_instances_of_type(errors, type_=Error, allow_empty=True), (
            "Param `errors` must be a list where each item is of type `valcheck.models.Error`"
        )
        self._field = field
        self._errors = errors

    def __str__(self) -> str:
        kwargs_list = [
            f"is_valid={not bool(self.errors)}",
            f"field_identifier={utils.wrap_in_quotes_if_string(self.field.field_identifier)}",
            f"field={self.field}",
        ]
        kwargs_string = "(" + ", ".join(kwargs_list) + ")"
        return f"{self.__class__.__name__}{kwargs_string}"

    @property
    def field(self) -> Field:
        return self._field

    @field.setter
    def field(self, value: Field) -> None:
        assert isinstance(value, Field), "Param `field` must be of type `valcheck.fields.Field`"
        self._field = value

    @property
    def errors(self) -> List[Error]:
        return self._errors

    @errors.setter
    def errors(self, value: List[Error]) -> None:
        assert utils.is_list_of_instances_of_type(value, type_=Error, allow_empty=True), (
            "Param `errors` must be a list where each item is of type `valcheck.models.Error`"
        )
        self._errors = value


class Field:
    """Class that represents a field (that needs to be validated)"""

    def __init__(
            self,
            *,
            source: Optional[str] = None,
            target: Optional[str] = None,
            required: Optional[bool] = True,
            nullable: Optional[bool] = False,
            default_factory: Optional[Callable] = None,
            converter_factory: Optional[Callable] = None,
            sample_value_factory: Optional[Callable] = None,
            validators: Optional[List[Callable]] = None,
            error: Optional[Error] = None,
            type_alias: Optional[str] = None,
        ) -> None:
        """
        Parameters:
            - source (str): Field name used in the input data (optional)
            - target (str): Field name used in the validated data (optional)
            - required (bool): True if the field is required, else False. Default: True
            - nullable (bool): True if the field is nullable, else False. Default: False
            - default_factory (callable): Callable that returns the default value to set for the field
            if `required=False` and the field is missing.
            - converter_factory (callable): Callable that takes in the validated value (of the field), and returns
            the converted value (for the field).
            - sample_value_factory (callable): Callable that returns the sample value for the field.
            - validators (list of callables): List of callables that each return a boolean (takes the field value as a param).
            The callable returns True if validation is successful, else False.
            - error (Error instance): Instance of type `valcheck.models.Error`.
            - type_alias (str): Alias of the field type (optional).
        """
        assert source is None or utils.is_valid_object_of_type(source, type_=str, allow_empty=False), (
            "Param `source` must be of type 'str' and must be non-empty"
        )
        assert target is None or utils.is_valid_object_of_type(target, type_=str, allow_empty=False), (
            "Param `target` must be of type 'str' and must be non-empty"
        )
        assert isinstance(required, bool), "Param `required` must be of type 'bool'"
        assert isinstance(nullable, bool), "Param `nullable` must be of type 'bool'"
        assert default_factory is None or callable(default_factory), (
            "Param `default_factory` must be a callable that returns the default value if the field is missing when `required=False`"
        )
        assert converter_factory is None or callable(converter_factory), (
            "Param `converter_factory` must be a callable that takes in the validated value (of the field), and returns"
            " the converted value (for the field)."
        )
        assert sample_value_factory is None or callable(sample_value_factory), (
            "Param `sample_value_factory` must be a callable that returns the sample value"
        )
        assert validators is None or isinstance(validators, list), "Param `validators` must be of type 'list'"
        if isinstance(validators, list):
            for validator in validators:
                assert callable(validator), "Param `validators` must be a list of callables"
        assert error is None or isinstance(error, Error), "Param `error` must be of type `valcheck.models.Error`"
        assert type_alias is None or utils.is_valid_object_of_type(type_alias, type_=str, allow_empty=False), (
            "Param `type_alias` must be of type 'str' and must be non-empty"
        )

        self._field_identifier = utils.set_as_empty()
        self._field_value = utils.set_as_empty()
        self.source = source
        self.target = target
        self.required = required
        self.nullable = nullable
        self.default_factory = default_factory
        self.converter_factory = converter_factory
        self.sample_value_factory = sample_value_factory
        self.validators = validators or []
        self.error = error or Error()
        self.type_alias = type_alias or self.__class__.__name__

    def copy(self) -> Field:
        """Returns deep-copy of current `Field` object"""
        return utils.make_deep_copy(self)

    def __str__(self) -> str:
        kwargs_list = [
            f"field_identifier={utils.wrap_in_quotes_if_string(self.field_identifier)}",
            f"field_value={utils.wrap_in_quotes_if_string(self.field_value)}",
            f"source={utils.wrap_in_quotes_if_string(self.source)}",
            f"target={utils.wrap_in_quotes_if_string(self.target)}",
            f"required={self.required}",
            f"nullable={self.nullable}",
            f"type_alias={utils.wrap_in_quotes_if_string(self.type_alias)}",
        ]
        kwargs_string = "(" + ", ".join(kwargs_list) + ")"
        return f"{self.__class__.__name__}{kwargs_string}"

    @property
    def field_identifier(self) -> str:
        return self._field_identifier

    @field_identifier.setter
    def field_identifier(self, value: str) -> None:
        assert isinstance(value, str), "Param `field_identifier` must be of type 'str'"
        self._field_identifier = value

    @property
    def field_value(self) -> Union[Any, utils.Empty]:
        return self._field_value

    @field_value.setter
    def field_value(self, value: Union[Any, utils.Empty]) -> None:
        self._field_value = value

    def _can_be_set_to_null(self) -> bool:
        return self.nullable and self.field_value is None

    def _cannot_be_set_to_null(self) -> bool:
        return not self.nullable and self.field_value is None

    def _has_valid_custom_validators(self) -> bool:
        if not self.validators:
            return True
        validator_return_values = [validator(self.field_value) for validator in self.validators]
        for return_value in validator_return_values:
            assert isinstance(return_value, bool), (
                f"Expected the return type of `validators` to be 'bool', but got '{type(return_value).__name__}'"
            )
        return all(validator_return_values)

    def _convert_field_value_if_needed(self) -> Any:
        """Returns the converted field value if a `converter_factory` is present; otherwise returns the same field value"""
        return self.converter_factory(self.field_value) if self.converter_factory else self.field_value

    def validate(self) -> List[Error]:
        """Returns list of errors (each of type `valcheck.models.Error`)"""
        raise NotImplementedError()

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        """Returns a sample value for the field"""
        return None

    def validate_entire_field(self) -> ValidatedField:
        if utils.is_empty(self.field_value) and not self.required and self.default_factory:
            self.field_value = self.default_factory()
        validated_field = ValidatedField(field=self, errors=[])
        if utils.is_empty(self.field_value) and not self.required and not self.default_factory:
            return validated_field
        if self._can_be_set_to_null():
            validated_field.field.field_value = self._convert_field_value_if_needed()
            return validated_field
        if utils.is_empty(self.field_value) and self.required:
            validated_field.errors += [self.create_missing_field_error()]
            return validated_field
        if self._cannot_be_set_to_null():
            suffix = "Cannot be null"
            validated_field.errors += [self.create_invalid_field_error(suffix=suffix)]
            return validated_field
        errors = self.validate()
        if errors:
            validated_field.errors += errors
            return validated_field
        if not self._has_valid_custom_validators():
            suffix = "Custom validations failed"
            validated_field.errors += [self.create_invalid_field_error(suffix=suffix)]
            return validated_field
        validated_field.field.field_value = self._convert_field_value_if_needed()
        return validated_field

    def invalid_field_error_message(
            self,
            *,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
        ) -> str:
        return utils.make_message(
            f"Invalid {self.type_alias} '{self.source}'",
            prefix=prefix,
            suffix=suffix,
            sep=" || ",
        )

    def missing_field_error_message(
            self,
            *,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
        ) -> str:
        return utils.make_message(
            f"Missing {self.type_alias} '{self.source}'",
            prefix=prefix,
            suffix=suffix,
            sep=" || ",
        )

    def create_error_instance(self, *, validator_message: str) -> Error:
        """Creates and returns a new `valcheck.models.Error` instance for the field"""
        error_copy = self.error.copy()
        error_copy.validator_message = validator_message
        error_copy.append_to_field_path(self.source)
        return error_copy

    def create_invalid_field_error(
            self,
            *,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
        ) -> Error:
        validator_message = self.invalid_field_error_message(prefix=prefix, suffix=suffix)
        return self.create_error_instance(validator_message=validator_message)

    def create_missing_field_error(
            self,
            *,
            prefix: Optional[str] = None,
            suffix: Optional[str] = None,
        ) -> Error:
        validator_message = self.missing_field_error_message(prefix=prefix, suffix=suffix)
        return self.create_error_instance(validator_message=validator_message)


class AnyField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(AnyField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        options = (
            {},
            [],
            "some string",
            '{"key1": "value1", "key2": "value2"}',
        )
        return random.choice(options)


class BooleanField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(BooleanField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, bool):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        options = (True, False)
        return random.choice(options)


class StringField(Field):
    def __init__(self, *, allow_empty: Optional[bool] = True, **kwargs: Any) -> None:
        assert isinstance(allow_empty, bool), "Param `allow_empty` must be of type 'bool'"
        self.allow_empty = allow_empty
        super(StringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not utils.is_valid_object_of_type(self.field_value, type_=str):
            return [self.create_invalid_field_error()]
        if not utils.is_empty_value_allowed(self.field_value, allow_empty=self.allow_empty):
            return [self.create_invalid_field_error(suffix="Must be a non-empty string")]
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return "some string"


class JsonStringField(Field):
    def __init__(
            self,
            *,
            which: Literal["ANY", "JSON_ARRAY", "JSON_OBJECT", "JSON_OBJECT_OR_ARRAY"] = "ANY",
            to_python_obj: Optional[bool] = False,
            **kwargs: Any,
        ) -> None:
        which_options = ["ANY", "JSON_ARRAY", "JSON_OBJECT", "JSON_OBJECT_OR_ARRAY"]
        assert isinstance(which, str) and which in which_options, f"Param `which` must be one of {which_options}"
        assert isinstance(to_python_obj, bool), f"Param `to_python_obj` must be of type 'bool'"
        self.which: Literal["ANY", "JSON_ARRAY", "JSON_OBJECT", "JSON_OBJECT_OR_ARRAY"] = which
        self.to_python_obj = to_python_obj
        super(JsonStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        error_message = ""
        if self.which == "JSON_ARRAY":
            parsed_obj, is_valid = utils.validate_json_array(self.field_value)
            if not is_valid:
                error_message = "Must be a valid JSON array"
        elif self.which == "JSON_OBJECT":
            parsed_obj, is_valid = utils.validate_json_object(self.field_value)
            if not is_valid:
                error_message = "Must be a valid JSON object"
        elif self.which == "JSON_OBJECT_OR_ARRAY":
            parsed_obj, is_valid = utils.validate_json_object_or_array(self.field_value)
            if not is_valid:
                error_message = "Must be a valid JSON object or JSON array"
        else:
            parsed_obj, is_valid = utils.validate_json_string(self.field_value)
            if not is_valid:
                error_message = "Must be a valid JSON string"

        if error_message:
            return [self.create_invalid_field_error(suffix=error_message)]
        if self.to_python_obj:
            self.field_value = parsed_obj
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        if self.which == "JSON_ARRAY":
            return '[1, 2, 3, null, "hello"]'
        return '{"key1": "value1", "key2": "value2"}'


class EmailIdStringField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(EmailIdStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if utils.is_valid_email_id_string(self.field_value):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return "hello@example.com"


class UuidStringField(Field):
    def __init__(self, *, to_uuid_obj: Optional[bool] = False, **kwargs: Any) -> None:
        assert isinstance(to_uuid_obj, bool), "Param `to_uuid_obj` must be of type 'bool'"
        self.to_uuid_obj = to_uuid_obj
        super(UuidStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        uuid_obj, is_valid = utils.validate_uuid_string(self.field_value)
        if not is_valid:
            suffix = "Must be a valid UUID string"
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_uuid_obj and uuid_obj is not None:
            self.field_value = uuid_obj
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return str(uuid.uuid4())


class UuidField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(UuidField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, uuid.UUID):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return uuid.uuid4()


class DateStringField(Field):
    def __init__(self, *, format_: Optional[str] = "%Y-%m-%d", to_date_obj: Optional[bool] = False, **kwargs: Any) -> None:
        assert isinstance(format_, str), "Param `format_` must be of type 'str'"
        assert isinstance(to_date_obj, bool), "Param `to_date_obj` must be of type 'bool'"
        self.format_ = format_
        self.to_date_obj = to_date_obj
        super(DateStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        date_obj, is_valid = utils.validate_date_string(self.field_value, self.format_)
        if not is_valid:
            suffix = f"Must be a valid date-string of format '{self.format_}'. Eg: '{self.sample_value()}'"
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_date_obj and date_obj is not None:
            self.field_value = date_obj
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return date(year=2020, month=4, day=20).strftime(self.format_)


class DateField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(DateField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, date) and self.field_value.__class__ is date:
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return date(year=2020, month=4, day=20)


class DatetimeStringField(Field):
    def __init__(
            self,
            *,
            format_: Optional[str] = "%Y-%m-%d %H:%M:%S.%f%z",
            to_datetime_obj: Optional[bool] = False,
            allowed_tz_names: Optional[List[str]] = None,
            **kwargs: Any,
        ) -> None:
        assert isinstance(format_, str), "Param `format_` must be of type 'str'"
        assert isinstance(to_datetime_obj, bool), "Param `to_datetime_obj` must be of type 'bool'"
        assert allowed_tz_names is None or isinstance(allowed_tz_names, list), "Param `allowed_tz_names` must be of type 'list'"
        self.format_ = format_
        self.to_datetime_obj = to_datetime_obj
        self.allowed_tz_names = allowed_tz_names
        super(DatetimeStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        datetime_obj, is_valid = utils.validate_datetime_string(self.field_value, self.format_)
        if not is_valid or datetime_obj is None:
            suffix = (
                f"Must be a valid datetime-string of format '{self.format_}'."
                f" Eg: '{self.sample_value()}'."
            )
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.allowed_tz_names:
            assert utils.is_timezone_aware(datetime_obj), (
                f"'{self.__class__.__name__}' has param `format_` set to '{self.format_}' which is not timezone-aware."
                " Therefore the param `allowed_tz_names` must not be passed."
            )
            if not utils.is_datetime_of_timezone(datetime_obj, allowed_tz_names=self.allowed_tz_names):
                suffix = (
                    f"Must be a valid datetime-string of format '{self.format_}'."
                    f" Must be of one of the following timezones [{' | '.join(self.allowed_tz_names)}]."
                    f" Eg: '{self.sample_value()}'."
                )
                return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_datetime_obj and datetime_obj is not None:
            self.field_value = datetime_obj
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        dt_obj = datetime(
            year=2020,
            month=4,
            day=20,
            hour=17,
            minute=30,
            second=45,
            microsecond=585675,
            tzinfo=timezone.utc,
        )
        dt_obj = datetime.strptime(dt_obj.strftime(self.format_), self.format_)
        if self.allowed_tz_names and utils.is_timezone_aware(dt_obj):
            tz_name = random.choice(self.allowed_tz_names)
            dt_obj = utils.convert_datetime_timezone(dt_obj, tz_name=tz_name)
        return dt_obj.strftime(self.format_)


class DatetimeField(Field):
    def __init__(
            self,
            *,
            timezone_aware: Optional[bool] = True,
            allowed_tz_names: Optional[List[str]] = None,
            **kwargs: Any,
        ) -> None:
        assert isinstance(timezone_aware, bool), "Param `timezone_aware` must be of type 'bool'"
        assert allowed_tz_names is None or isinstance(allowed_tz_names, list), "Param `allowed_tz_names` must be of type 'list'"
        if not timezone_aware:
            assert allowed_tz_names is None, "Param `allowed_tz_names` must not be passed when `timezone_aware=False`"
        self.timezone_aware = timezone_aware
        self.allowed_tz_names = allowed_tz_names
        super(DatetimeField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not (
            isinstance(self.field_value, datetime)
            and self.field_value.__class__ is datetime
        ):
            suffix = "Invalid data-type"
            return [self.create_invalid_field_error(suffix=suffix)]
        if not (self.field_value.tzinfo is not None if self.timezone_aware else self.field_value.tzinfo is None):
            suffix = (
                "Invalid timezone awareness/naivety."
                f" Expected a {'timezone-aware' if self.timezone_aware else 'timezone-naive'} datetime object."
            )
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.allowed_tz_names and not utils.is_datetime_of_timezone(self.field_value, allowed_tz_names=self.allowed_tz_names):
            suffix = (
                "Invalid timezone."
                f" Must be of one of the following timezones [{' | '.join(self.allowed_tz_names)}]."
            )
            return [self.create_invalid_field_error(suffix=suffix)]
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        dt_obj = datetime(
            year=2020,
            month=4,
            day=20,
            hour=17,
            minute=30,
            second=45,
            microsecond=585675,
            tzinfo=timezone.utc if self.timezone_aware else None,
        )
        if self.allowed_tz_names:
            tz_name = random.choice(self.allowed_tz_names)
            dt_obj = utils.convert_datetime_timezone(dt_obj, tz_name=tz_name)
        return dt_obj


class ChoiceField(Field):
    def __init__(self, *, choices: Iterable[Any], **kwargs: Any) -> None:
        assert utils.is_collection_of_items(choices) and bool(choices), "Param `choices` must be a non-empty iterable"
        self.choices = choices
        super(ChoiceField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if self.field_value in self.choices:
            return []
        suffix = f"Must be a valid choice i.e; one of {list(self.choices)}"
        return [self.create_invalid_field_error(suffix=suffix)]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return random.choice(self.choices)


class MultiChoiceField(Field):
    def __init__(self, *, choices: Iterable[Any], **kwargs: Any) -> None:
        assert utils.is_collection_of_items(choices) and bool(choices), "Param `choices` must be a non-empty iterable"
        self.choices = choices
        super(MultiChoiceField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if (
            utils.is_collection_of_items(self.field_value)
            and bool(self.field_value)
            and all([item in self.choices for item in self.field_value])
        ):
            return []
        suffix = f"Must be a valid list of choices i.e; one or more of {list(self.choices)}"
        return [self.create_invalid_field_error(suffix=suffix)]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return (
            random.sample(self.choices, k=2) if len(self.choices) > 1 else random.sample(self.choices, k=1)
        )


class BytesField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(BytesField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, bytes):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return b''


class NumberField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(NumberField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, (int, float)):
            return []
        suffix = "Must be a valid number (either integer or float)"
        return [self.create_invalid_field_error(suffix=suffix)]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return 3.14


class IntegerField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(IntegerField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, int):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return 314


class FloatField(Field):
    def __init__(self, **kwargs: Any) -> None:
        super(FloatField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if isinstance(self.field_value, float):
            return []
        return [self.create_invalid_field_error()]

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return 3.14


class NumberStringField(Field):
    def __init__(self, *, to_number: Optional[bool] = False, **kwargs: Any) -> None:
        assert isinstance(to_number, bool), "Param `to_number` must be of type 'bool'"
        self.to_number = to_number
        super(NumberStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        number, is_valid = utils.validate_number_string(self.field_value)
        if not is_valid:
            suffix = "Must be a valid number (either integer or float) cast as a string"
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_number and number is not None:
            self.field_value = number
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return "3.14"


class IntegerStringField(Field):
    def __init__(self, *, to_integer: Optional[bool] = False, **kwargs: Any) -> None:
        assert isinstance(to_integer, bool), "Param `to_integer` must be of type 'bool'"
        self.to_integer = to_integer
        super(IntegerStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        number_as_int, is_valid = utils.validate_integer_string(self.field_value)
        if not is_valid:
            suffix = "Must be a valid integer cast as a string"
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_integer and number_as_int is not None:
            self.field_value = number_as_int
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return "314"


class FloatStringField(Field):
    def __init__(self, *, to_float: Optional[bool] = False, **kwargs: Any) -> None:
        assert isinstance(to_float, bool), "Param `to_float` must be of type 'bool'"
        self.to_float = to_float
        super(FloatStringField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        number_as_float, is_valid = utils.validate_float_string(self.field_value)
        if not is_valid:
            suffix = "Must be a valid float cast as a string"
            return [self.create_invalid_field_error(suffix=suffix)]
        if self.to_float and number_as_float is not None:
            self.field_value = number_as_float
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return "3.14"


class DictionaryField(Field):
    def __init__(self, *, allow_empty: Optional[bool] = True, **kwargs: Any) -> None:
        assert isinstance(allow_empty, bool), "Param `allow_empty` must be of type 'bool'"
        self.allow_empty = allow_empty
        super(DictionaryField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not utils.is_valid_object_of_type(self.field_value, type_=dict):
            return [self.create_invalid_field_error()]
        if not utils.is_empty_value_allowed(self.field_value, allow_empty=self.allow_empty):
            return [self.create_invalid_field_error(suffix="Must be a non-empty dictionary")]
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return {
            "a": 1,
            "b": 2,
            "c": 3,
        }


class ListField(Field):
    def __init__(self, *, allow_empty: Optional[bool] = True, **kwargs: Any) -> None:
        assert isinstance(allow_empty, bool), "Param `allow_empty` must be of type 'bool'"
        self.allow_empty = allow_empty
        super(ListField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not utils.is_valid_object_of_type(self.field_value, type_=list):
            return [self.create_invalid_field_error()]
        if not utils.is_empty_value_allowed(self.field_value, allow_empty=self.allow_empty):
            return [self.create_invalid_field_error(suffix="Must be a non-empty list")]
        return []

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return [1, 2, 3]


class ModelDictionaryField(Field):
    def __init__(self, *, validator_model: Type, **kwargs: Any) -> None:
        from valcheck.validators import Validator
        assert validator_model is not Validator and issubclass(validator_model, Validator), (
            "Param `validator_model` must be a sub-class of `valcheck.validators.Validator`"
        )
        kwargs_to_disallow = ['validators', 'error']
        if utils.dict_has_any_keys(kwargs, keys=kwargs_to_disallow):
            msg = (
                f"This field does not accept the following params: {kwargs_to_disallow}, since"
                " the `validator_model` handles these parameters"
            )
            raise ValueError(msg)
        self.validator_model = validator_model
        super(ModelDictionaryField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not isinstance(self.field_value, dict):
            suffix = "Field must be a dictionary"
            error = self.create_invalid_field_error(suffix=suffix)
            return [error]
        validator = self.validator_model(data=self.field_value)
        validator.run_validations()
        error_objs = validator.errors
        for error_obj in error_objs:
            suffix = error_obj.validator_message
            error_obj.validator_message = self.invalid_field_error_message(suffix=suffix)
            error_obj.append_to_field_path(self.source)
        if not error_objs:
            self.field_value = validator.validated_data
        return error_objs

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return {
            **self.validator_model().get_representation(**kwargs),
        }


class ModelListField(Field):
    def __init__(self, *, validator_model: Type, allow_empty: Optional[bool] = True, **kwargs: Any) -> None:
        from valcheck.validators import Validator
        assert validator_model is not Validator and issubclass(validator_model, Validator), (
            "Param `validator_model` must be a sub-class of `valcheck.validators.Validator`"
        )
        kwargs_to_disallow = ['validators', 'error']
        if utils.dict_has_any_keys(kwargs, keys=kwargs_to_disallow):
            msg = (
                f"This field does not accept the following params: {kwargs_to_disallow}, since"
                " the `validator_model` handles these parameters"
            )
            raise ValueError(msg)
        assert isinstance(allow_empty, bool), "Param `allow_empty` must be of type 'bool'"
        self.validator_model = validator_model
        self.allow_empty = allow_empty
        super(ModelListField, self).__init__(**kwargs)

    def validate(self) -> List[Error]:
        if not isinstance(self.field_value, list):
            suffix = "Field must be a list"
            error = self.create_invalid_field_error(suffix=suffix)
            return [error]
        if not self.allow_empty and not self.field_value:
            suffix = "Field must be a non-empty list"
            error = self.create_invalid_field_error(suffix=suffix)
            return [error]
        errors: List[Error] = []
        validated_field_value = []
        for idx, item in enumerate(self.field_value):
            row_number = idx + 1
            row_number_string = f"<Row number: {row_number}>"
            if not isinstance(item, dict):
                suffix = f"Row must be a dictionary {row_number_string}"
                error = self.create_invalid_field_error(suffix=suffix)
                errors.append(error)
                continue
            validator = self.validator_model(data=item)
            validator.run_validations()
            error_objs = validator.errors
            validated_field_value.append(validator.validated_data)
            for error_obj in error_objs:
                suffix = f"{error_obj.validator_message} {row_number_string}"
                error_obj.validator_message = self.invalid_field_error_message(suffix=suffix)
                error_obj.append_to_field_path(self.source)
            errors.extend(error_objs)
        if not errors:
            self.field_value = validated_field_value
        return errors

    def sample_value(self, **kwargs: Any) -> Union[Any, None]:
        if self.sample_value_factory:
            return self.sample_value_factory()
        return [
            self.validator_model().get_representation(**kwargs),
        ]


