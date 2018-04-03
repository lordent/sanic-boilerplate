from oad.merge import dict_merge


def path(documentation: dict):
    def inner(func):
        if hasattr(func, '__openapi__'):
            func.__openapi__ = dict_merge(
                func.__openapi__, documentation)
        else:
            func.__openapi__ = documentation
    return inner
