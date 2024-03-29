import datetime
import pytz
import requests
import os
import re
from pydantic import BaseModel
from core.database import models
from config import settings


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


def camel_to_snake(camel: str):
    temp = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", camel)).split()
    snake = ""

    # Convert to snake case
    for i in range(len(temp)):
        if i != 0:
            snake += "_" + temp[i].lower()
        else:
            snake += temp[i].lower()

    return snake


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
            if isinstance(snake_obj[i], dict) or isinstance(snake_obj[i], list):
                snake_obj[i] = snake_dict_to_camel(snake_obj[i])
    if isinstance(snake_obj, dict):
        for key, value in snake_obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = snake_dict_to_camel(value)
            camel_obj[snake_to_camel(key)] = value
        return camel_obj
    return snake_obj


def camel_dict_to_snake(camel_obj):
    """
    Convert dictionary or list recursively to use
    snake_case keys instead of camelCase
    :param camel_obj: dictionary or list to be converted
    :return: snake_case version of camel_obj
    """
    snake_obj = {}
    if isinstance(camel_obj, list):
        for i in range(len(camel_obj)):
            if isinstance(camel_obj[i], dict) or isinstance(camel_obj[i], list):
                camel_obj[i] = camel_dict_to_snake(camel_obj[i])
    if isinstance(camel_obj, dict):
        for key, value in camel_obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = camel_dict_to_snake(value)
            snake_obj[camel_to_snake(key)] = value
        return snake_obj
    return camel_obj


def base_serialize(obj):
    try:
        return obj.base_serialize()
    except AttributeError:
        return obj


def datetime_to_string(date: datetime):
    return date.replace(tzinfo=pytz.UTC).isoformat("T").split("+")[0]


def get_channel_info(discord_id: str):
    """
    Use bot user to get channel info
    :param discord_id: discord id of channel
    :return: channel object
    """
    r = requests.get(
        "https://discord.com/api/v6/channels/" + discord_id,
        headers={
            "Authorization": "Bot " + str(os.environ.get("BOT_TOKEN", "NO TOKEN"))
        },
    )
    return r.json()


def send_webhook(content: BaseModel):
    response = requests.post("http://bot:9080/webhook", data=content.json())
    if response.status_code != 200:
        raise ValueError(response.text)


def is_superuser(user: models.Player):
    """
    Check if user/player is a super user.
    :param user:
    :return:
    """
    return user.discord_id in settings.SUPERUSERS
