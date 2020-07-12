import string
import random


def generate_identity():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(64))


def get_branch(ref):
    ref_list = ref.split("/")
    return ref_list[len(ref_list)-1]


def action_imperfect(action):
    if action.endswith('e'):
        return action + "d"
    else:
        return action + "ed"
