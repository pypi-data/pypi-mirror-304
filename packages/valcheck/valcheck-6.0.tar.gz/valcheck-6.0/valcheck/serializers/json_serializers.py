from datetime import date, datetime
from typing import Any, Callable, Dict, Optional, Type, Union
from uuid import UUID

from valcheck import utils
from valcheck.meta_classes import Singleton


class JsonSerializer:
    """Class that represents a JSON serializer."""

    def __init__(self, *, include_default_serializers: Optional[bool] = False) -> None:
        assert isinstance(include_default_serializers, bool), "Param `include_default_serializers` must be of type 'bool'"
        self._json_serializable_mapper: Dict[Type, Callable] = {}
        if include_default_serializers:
            self._register_default_serializers_by_type()

    def _register_default_serializers_by_type(self) -> None:
        self.register_serializers_by_type({
            bytes: lambda value: str(value),
            date: lambda value: value.strftime("%Y-%m-%d"),
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            set: lambda value: list(value),
            str: lambda value: self.from_json_string(value) if utils.is_valid_json_object_or_array(value) else value,
            tuple: lambda value: list(value),
            UUID: lambda value: str(value),
        })

    def register_serializers_by_type(self, mapper: Dict[Type, Callable], /) -> None:
        """
        To register a serializer for a given type.
        Internally uses a type-to-callable mapping to convert a Python object (of the given type) to a JSON serializable value.
        Can be used to over-write the default serializers (if any).

        Params:
            - mapper (dict): Dictionary where keys = the type to serialize, and
            values = the callable that takes in the unserializable value as a param, and returns the serializable value.
        """
        for type_, callable_ in mapper.items():
            assert isinstance(type_, type), "Keys of `mapper` must each be of type 'type'"
            assert callable(callable_), "Values of `mapper` must each be a callable"
        self._json_serializable_mapper.update(mapper)

    def from_json_string(self, s: Union[str, bytes, bytearray], /, **kwargs: Any) -> Any:
        """Converts JSON string into a Python object"""
        return utils.from_json_string(s, **kwargs)

    def to_json_string(self, obj: Any, /, **kwargs: Any) -> str:
        """Converts Python object into a JSON string after making it JSON serializable"""
        return utils.to_json_string(self.make_json_serializable(obj), **kwargs)

    def make_json_serializable(self, obj: Any, /) -> Any:
        """Returns Python object which is JSON serializable (a new copy is returned)"""
        obj_copy = utils.make_deep_copy(obj)
        obj_copy = self._make_json_serializable(obj_copy)
        return obj_copy

    def _get_serializable_function(self, value: Any, /) -> Union[Callable, None]:
        """Returns the serializable function for the given `value`. Returns `None` if the function is not registered."""
        func: Union[Callable, None] = self._json_serializable_mapper.get(type(value), None)
        return func

    def _make_json_serializable(self, obj: Any, /) -> Any:
        """Returns Python object which is JSON serializable. Modifies the given `obj` in-place."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    obj[key] = self._make_json_serializable(value)
                elif isinstance(value, list):
                    obj[key] = self._make_json_serializable(value)
                else:
                    func = self._get_serializable_function(value)
                    if not func:
                        continue
                    obj[key] = func(value)
                    if isinstance(obj[key], (dict, list)):
                        obj[key] = self._make_json_serializable(obj[key])
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                if isinstance(item, dict):
                    obj[idx] = self._make_json_serializable(item)
                elif isinstance(item, list):
                    obj[idx] = self._make_json_serializable(item)
                else:
                    func = self._get_serializable_function(item)
                    if not func:
                        continue
                    obj[idx] = func(item)
                    if isinstance(obj[idx], (dict, list)):
                        obj[idx] = self._make_json_serializable(obj[idx])
        else:
            func = self._get_serializable_function(obj)
            if func:
                obj = func(obj)
                if isinstance(obj, (dict, list)):
                    obj = self._make_json_serializable(obj)
        return obj


class JsonSerializerSingleton(JsonSerializer, metaclass=Singleton):
    """Class that represents a JSON serializer which is a singleton."""
    pass


