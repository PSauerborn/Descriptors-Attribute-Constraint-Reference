
from functools import wraps
import time
import numpy as np


def timer(*args, **kwargs):
    """Decorator that evaluates the average runtime of a given function over a set number of iterations

    Parameters
    ----------
    n: int
        number of times the function will be run. Note that an average run time is then computed

    """

    accepted_args = ['n']

    for argument in kwargs.keys():
        if argument not in accepted_args:
            raise AttributeError(
                '{} not accepted argument: please see documentation for allowed arguments'.format(argument))

    def make_wrapper(func):

        @wraps(func)
        def wrapper(*fargs, **fkwargs):

            times = []

            for n in range(kwargs['n']):

                start = time.time()

                func(*fargs, **fkwargs)

                end = time.time()

                times.append(end-start)

            print('{} runtime {}'.format(func.__name__, np.mean(times)))

        return wrapper
    return make_wrapper


@timer(n=10)
def loop():

    for i in range(1000000):
        pass


loop()
