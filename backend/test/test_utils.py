from core.utils import *
from test.test_main import client


def test_snake_to_camel():
    snake_text = "this_is_very_nice_snake"
    camel_text = snake_to_camel(snake_text)
    assert camel_text == "thisIsVeryNiceSnake"


def test_camel_to_snake():
    camel_text = "thisIsVeryNiceCamel"
    snake_text = camel_to_snake(camel_text)
    assert snake_text == "this_is_very_nice_camel"


def test_snake_dict_to_camel():
    snake_dict = {
        "very_nice": {
            "much_deep": {
                "whoah": "asd",
                "very_nicu": "hei",
                "kappa_mui": "hui"
            }
        }
    }

    right_camel = {
        "veryNice": {
            "muchDeep": {
                "whoah": "asd",
                "veryNicu": "hei",
                "kappaMui": "hui"
            }
        }
    }

    camel_dict = snake_dict_to_camel(snake_dict)
    assert camel_dict == right_camel


def test_camel_dict_to_snake():
    right_snake = {
        "very_nice": {
            "much_deep": {
                "whoah": "asd",
                "very_nicu": "hei",
                "kappa_mui": "hui"
            }
        }
    }

    camel_dict = {
        "veryNice": {
            "muchDeep": {
                "whoah": "asd",
                "veryNicu": "hei",
                "kappaMui": "hui"
            }
        }
    }

    snake_dict = camel_dict_to_snake(camel_dict)
    assert snake_dict == right_snake


def test_snake_to_snake():
    snake_text = "this_is_very_nice_snake"
    new_snake_text = camel_to_snake(snake_to_camel(snake_text))
    assert new_snake_text == snake_text


def test_camel_to_camel():
    camel_text = "thisIsVeryNiceCamel"
    new_camel_text = snake_to_camel(camel_to_snake(camel_text))
    assert camel_text == new_camel_text


def test_snake_dict_to_snake():
    snake_dict = {
        "very_nice": {
            "much_deep": {
                "whoah": "asd",
                "very_nicu": "hei",
                "kappa_mui": "hui"
            }
        }
    }

    new_snake_dict = camel_dict_to_snake(snake_dict_to_camel(snake_dict))
    assert snake_dict == new_snake_dict


def test_camel_dict_to_camel():
    camel_dict = {
        "veryNice": {
            "muchDeep": {
                "whoah": "asd",
                "veryNicu": "hei",
                "kappaMui": "hui"
            }
        }
    }

    new_camel_dict = snake_dict_to_camel(camel_dict_to_snake(camel_dict))
    assert camel_dict == new_camel_dict


def test_no_change():
    snake_text = "this_is_very_nice_snake"
    new_snake_text = camel_to_snake(snake_text)
    assert snake_text == new_snake_text

    camel_text = "thisIsVeryNiceCamel"
    new_camel_text = snake_to_camel(camel_text)
    assert camel_text == new_camel_text

    snake_dict = {
        "very_nice": {
            "much_deep": {
                "whoah": "asd",
                "very_nicu": "hei",
                "kappa_mui": "hui"
            }
        }
    }
    new_snake_dict = camel_dict_to_snake(snake_dict)
    assert snake_dict == new_snake_dict

    camel_dict = {
        "veryNice": {
            "muchDeep": {
                "whoah": "asd",
                "veryNicu": "hei",
                "kappaMui": "hui"
            }
        }
    }
    new_camel_dict = snake_dict_to_camel(camel_dict)
    assert camel_dict == new_camel_dict


def test_is_superuser():
    response = client.get('/players/superuser')
    assert response.status_code == 200, response.text

    data = response.json()

    assert data['isSuperuser']
