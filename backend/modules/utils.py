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
