from jsonschema import validators
from jsonschema.exceptions import ErrorTree
import adaptivecard._base_types as _base_types
from adaptivecard._typing import DefaultNone
from adaptivecard._utils import snake_to_camel, camel_to_snake, get_schema_path
from collections import namedtuple



def is_type(tp):
    def helper(_, instance):
        return isinstance(instance, tp)
    return helper


type_checker = (
    validators.Draft6Validator.TYPE_CHECKER.redefine_many(
        {"Element": is_type(_base_types.Element),
         "AdaptiveCard": is_type(_base_types.AdaptiveCard),
         "TextBlock": is_type(_base_types.TextBlock),
         "ActionSet": is_type(_base_types.ActionSet),
         "Action": is_type(_base_types.Action),
         "ShowCard": is_type(_base_types.ShowCard),
         "Execute": is_type(_base_types.Execute),
         "OpenUrl": is_type(_base_types.OpenUrl),
         "Submit": is_type(_base_types.Submit),
         "ToggleVisibility": is_type(_base_types.ToggleVisibility),
         "Table": is_type(_base_types.Table),
         "TableRow": is_type(_base_types.TableRow),
         "TableCell": is_type(_base_types.TableCell),
         "Container": is_type(_base_types.Container),
         "ColumnSet": is_type(_base_types.ColumnSet),
         "Column": is_type(_base_types.Column),
         "Image": is_type(_base_types.Image),
         "ImageSet": is_type(_base_types.ImageSet),
         "Input.Text": is_type(_base_types.Text),
         "Input.Number": is_type(_base_types.Number),
         "Input.Date": is_type(_base_types.Date),
         "Input.Time": is_type(_base_types.Time),
         "Input.Toggle": is_type(_base_types.Toggle),
         "Input.Choice": is_type(_base_types.Choice),
         "Input.ChoiceSet": is_type(_base_types.ChoiceSet),
        }
         )
         )

CardValidator = validators.extend(validators.Draft6Validator, type_checker=type_checker)



def get_deepest_error(errors):
    """Traverses the errors looking for the first non-empty tree. If found, searches left in every
    left child's context until context is null. Returns a namedtuple with the offending elements's
    name and the error object itself."""
    for error in errors:
        error_tree = ErrorTree([error])
        if error_tree._contents:
            offending_element = next(iter(error_tree))
            child_tree = error_tree[offending_element]
            errors = child_tree.errors
            while not errors:
                sub = next(iter(child_tree._contents))
                child_tree = child_tree._contents[sub]
                errors = child_tree.errors
            child_error = next(iter(errors.values()))
            while (child_errors := child_error.context):
                child_error = next(iter(child_errors))
            Error = namedtuple("Error", ("element", "error"))
            return Error(offending_element, child_error)
        elif error.context:
            return get_deepest_error(error.context)



def get_validation_schema_for_property(schema: dict, type: str, property: str):
    property = snake_to_camel(property)
    validation_schema = {"definitions": schema["definitions"].copy(), "properties": {}}
    properties = get_schema_path(validation_schema["definitions"][type])
    if properties is not None and property in properties:
        validation_schema["properties"][property] = properties[property].copy()
        return validation_schema


def check_types(schema: dict, obj: dict):
    """Checks types by running a json schema validation on the `obj` object.
    Assumes the first deepest error to be the most relevant and raises it."""
    obj_no_default_values = {
        snake_to_camel(key): value for key, value in obj.items() if value is not DefaultNone}
    validator = CardValidator(schema)
    error = get_deepest_error(validator.iter_errors(obj_no_default_values))
    if error is None:
        return
    element = camel_to_snake(error.element)
    error_msg = f"invalid value for '{element}': {error.error.message}"
    if error.error.validator == "enum":
        raise ValueError(error_msg)
    elif error.error.validator == "type":
        raise TypeError(error_msg)
    else:
        raise Exception(f"unknown error. Validator: {error.error.validator}, Message: {error.error.message} ")
    

def check_type(schema: dict, attr_name: str, attr_value):
    validator = CardValidator(schema)
    obj = {snake_to_camel(attr_name): attr_value}
    error = get_deepest_error(validator.iter_errors(obj))
    if error is None:
        return
    element = camel_to_snake(error.element)
    error_msg = f"invalid value for '{element}': {error.error.message}"
    if error.error.validator == "enum":
        raise ValueError(error_msg)
    elif error.error.validator == "type":
        raise TypeError(error_msg)
    else:
        raise Exception(f"unknown error. Validator: {error.error.validator}, Message: {error.error.message} ")

