


def cached_attribute(func):
    ''' Decorator that caches the return value of a function by storing it in
        an instance attribute with the same name, prefixed by an underscore.
        On subsequent calls, the cached value is returned from the instance
        attribute instead of executing the function again. '''

    @property
    def wrapper(self):

        attr = '_' + func.__name__

        if attr not in self.__dict__:
            setattr(self, attr, func(self))

        return getattr(self, attr)

    return wrapper



def lazy_attribute(func):
    ''' Identical to cached_attribute except cached values are stored in
        a dictionary named _lazy_cache to prevent namespace clutter. '''

    @property
    def wrapper(self):

        if '_lazy_cache' not in self.__dict__:
            self._lazy_cache = {}

        key = func.__name__

        if key not in self._lazy_cache:
            self._lazy_cache[key] = func(self)

        return self._lazy_cache[key]

    return wrapper