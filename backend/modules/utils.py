from flask_restful_swagger import registry
from flask_restful_swagger.swagger import _parse_doc


def model(c=None, *args, **kwargs):
    add_model(c)
    return c


def add_model(model_class):
    models = registry["models"]
    name = model_class.__name__
    model = models[name] = {"id": name}
    model["description"], model["notes"] = _parse_doc(model_class)
    properties = model["properties"] = {}

    if "swagger_metadata" in dir(model_class):
        for field_name, field_metadata in model_class.swagger_metadata.items():
            properties[field_name] = field_metadata


def snake_to_camel(snake: str):
    temp = snake.split("_")
    camel = ""

    for i in range(len(temp)):
        if i == 0:
            camel.join(temp[i])
            continue

        # Convert to camel case
        camel.join(temp[i][0].upper() + temp[i][1:])

    return camel


# TODO better function name
def custom_get(body: dict, snake_key: str):
    camel_key = snake_to_camel(snake_key)

    # Search from body
    if snake_key in body:
        return body[snake_key]

    if camel_key in body:
        return body[camel_key]

    # If not found
    return None


# TODO better function name
def custom_check(body: dict, snake_key: str):
    camel_key = snake_to_camel(snake_key)
    return camel_key in body or snake_key in body


def base_serialize(obj):
    try:
        return obj.base_serialize()
    except AttributeError:
        return obj
