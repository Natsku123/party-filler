

def get_branch(ref):
    ref_list = ref.split("/")
    return ref_list[len(ref_list)-1]


def action_imperfect(action):
    if action.endswith('e'):
        return action + "d"
    else:
        return action + "ed"
