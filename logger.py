from functools import wraps, partial
import logging


def attach_wrapper(obj, func=None):
    """Utility Decorator to attach a function as to an object"""

    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    """
    Decorator used to add Logging to a function. Note that if the message and name arent specified, they default to the functions module and name

    Parameters
    ----------
    level:
        logging level
    name: str
        name of logger
    message: str
        log message

    """

    def decorate(func):

        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate


# the above can then be used as follows


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')


logging.basicConfig(level=logging.DEBUG)

print(add(2, 3))

# because the attach_wrapper function sets the functions as attributes

add.set_message('Add Called')

print(add(2, 3))

add.set_level(logging.WARNING)

print(add(2, 3))
