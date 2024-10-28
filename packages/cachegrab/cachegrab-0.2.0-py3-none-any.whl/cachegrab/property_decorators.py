from .utils import deep_copy



def deep_copy_property(func):
    ''' property that returns a deep copy of the return value '''

    @property
    def wrapper(self):
        return deep_copy(func(self))

    return wrapper



def deep_cached_property(func):
    ''' Inspired by functools.cached_property, this decorator provides a deep copy
        of cached return values, ensuring they remain immutable after their initial
        access. The original return values are preserved in a dictionary named
        _deep_cache. '''

    @property
    def wrapper(self):

        if '_deep_cache' not in self.__dict__:
            self._deep_cache = {}

        key = func.__name__

        if key not in self._deep_cache:
            self._deep_cache[key] = func(self)

        return deep_copy(self._deep_cache[key])

    return wrapper