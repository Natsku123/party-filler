import datetime
import pytz
import requests
import os
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
            camel += temp[i]
            continue

        # Convert to camel case
        camel += temp[i][0].upper() + temp[i][1:]

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


def snake_dict_to_camel(snake_obj):
    """
    Convert dictionary or list recursively to use
    camelCase keys instead of snake_case
    :param snake_obj: dictionary or list to be converted
    :return: camelCase version of snake_obj
    """
    camel_obj = {}
    if isinstance(snake_obj, list):
        for i in range(len(snake_obj)):
            if isinstance(snake_obj[i], dict) or \
                    isinstance(snake_obj[i], list):
                snake_obj[i] = snake_dict_to_camel(snake_obj[i])
    if isinstance(snake_obj, dict):
        for key, value in snake_obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = snake_dict_to_camel(value)
            camel_obj[snake_to_camel(key)] = value
        return camel_obj
    return snake_obj


def base_serialize(obj):
    try:
        return obj.base_serialize()
    except AttributeError:
        return obj


def datetime_to_string(date: datetime):
    return date.replace(tzinfo=pytz.UTC).isoformat("T").split("+")[0] + "Z"


def get_channel_info(discord_id: str):
    """
    Use bot user to get channel info
    :param discord_id: discord id of channel
    :return: channel object
    """
    r = requests.get(
        'https://discord.com/api/v6/channels/' + discord_id,
        headers={'Authorization': 'Bot ' + str(os.environ.get(
            'BOT_TOKEN', 'NO TOKEN'
        ))}
    )
    return r.json()


def send_webhook(content):
    if os.environ.get('WEBHOOK_ID') and content:
        requests.post(
            'http://bot:9080//webhook/' + os.environ.get('WEBHOOK_ID'),
            data=content
        )
