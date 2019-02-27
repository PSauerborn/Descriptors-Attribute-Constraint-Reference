class Descriptor():
    """Base class Descriptor used to set a value"""

    def __init__(self, name=None, **opts):

        self.name = name

        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    """Descriptor used for enforcing types"""

    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected Argument of type {}'.format(str(self.expected_type)))

        super().__set__(instance, value)


class Unsigned(Descriptor):
    """Descriptor used for enforcing values"""

    def __set__(self, instance, value):

        if value < 0:
            raise ValueError('Expected Unsigned Value')

        super().__set__(instance, value)


class MaxSized(Descriptor):
    """Descriptor used for enforcing size"""

    def __init__(self, name=None, **opts):

        if 'size' not in opts:
            raise TypeError('Missing size option')

        super().__init__(name, **opts)

    def __set__(self, instance, value):

        if len(value) >= self.size:
            raise ValueError('size must be < {}'.format(self.size))

        super().__set__(instance, value)

# the above classes can then be used as building blocks for more complex structures


class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    pass


# Decorators can then be used as a standard approach to specify the constraints

def constrained_attributes(**kwargs):
    """Decorator used to enforce constraints on custom classes"""

    def wrapper(cls):

        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))

        return cls

    return wrapper

# the above can then be used as follows


@constrained_attributes(name=SizedString(size=8), shares=UnsignedInteger, price=UnsignedFloat)
class Stock():

    def __init__(self, name, shares, price):

        self.name = name
        self.shares = shares
        self.price = price

    def __str__(self):
        return 'Name: {0.name} Shares: {0.shares} Price: {0.price}'.format(self)


a = Stock(name='GOOG', shares=12445, price=0.87)

print(a)
