"""Django compatibility utilities."""


def context_flatten(context):
    result = {}
    # https://code.djangoproject.com/ticket/24765
    for dict_ in context.dicts:
        if hasattr(dict_, 'flatten'):
            dict_ = context_flatten(dict_)
        result.update(dict_)
    return result
