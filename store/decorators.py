from django.contrib.auth.decorators import user_passes_test

def developer_required(function=None, login_url='player_main'):
    """
    Decorator for views that checks that the user is a developer
    """
    actual_decorator = user_passes_test(
        lambda u: len(u.groups.filter(name='dev')) > 0,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def player_required(function=None, login_url='developer_main'):
    """
    Decorator for views that checks that the user is a player
    """
    actual_decorator = user_passes_test(
        lambda u: len(u.groups.filter(name='player')) > 0,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
