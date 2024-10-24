from typing import Any
from adaptivecard._typing import DefaultNone
from adaptivecard._base_types import Element, Choice
from adaptivecard._utils import snake_to_camel, save_json
from adaptivecard._type_checker import check_type, get_validation_schema_for_property
from adaptivecard.schemas import schema


class Mixin:
    __slots__ = ()

    def to_dict(self):
        dic = {}
        if hasattr(self, "type"):
            dic["type"] = self.type
        for attr_name, attr_value in {attr_name: getattr(self, attr_name) for attr_name in self.__slots__ if hasattr(self, attr_name)}.items():
            camel_formated_attr_name = snake_to_camel(attr_name)
            if isinstance(attr_value, Element):
                dic[camel_formated_attr_name] = attr_value.to_dict()
            elif isinstance(attr_value, list):
                dic[camel_formated_attr_name] = [inner_value.to_dict() for inner_value in attr_value if hasattr(inner_value, "__slots__")]
            else:
                attr_value = attr_value if attr_value is not None else "none"
                dic[camel_formated_attr_name] = attr_value
        return dic

    def to_json(self, path_name: str, indent: int = 4):
        save_json(path=path_name, obj=self.to_dict(), indent=indent)
    
    def set_attributes(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "type":
            raise AttributeError("cannot set 'type' attribute")
        # do not create attributes that are set to DefaultNone, i.e., if the user did not input any value
        if __value is DefaultNone:
            return
        if isinstance(self, Choice):
            element_type = "Input.Choice"
        else:
            element_type = self.type

        validation_schema = get_validation_schema_for_property(schema, element_type, __name)
        if validation_schema is not None:
            check_type(validation_schema, __name, __value)
        super().__setattr__(__name, __value)
