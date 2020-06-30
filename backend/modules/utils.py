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


# TODO better function name
def custom_get(body: dict, snake_key: str):
    temp_key = snake_key.split("_")
    camel_key = ""

    for i in range(len(temp_key)):
        if i == 0:
            camel_key.join(temp_key[i])
            continue

        # Convert to camel case
        camel_key.join(temp_key[i][0].upper() + temp_key[i][1:])

    # Search from body
    if snake_key in body:
        return body[snake_key]

    if camel_key in body:
        return body[camel_key]

    # If not found
    return None
