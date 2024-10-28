# cachegrab

<div>

[![Package version](https://img.shields.io/pypi/v/cachegrab?color=%2334D058&label=pypi)](https://pypi.org/project/cachegrab/)
[![License](https://img.shields.io/github/license/zteinck/cachegrab)](https://github.com/zteinck/cachegrab/blob/master/LICENSE)

</div>


`cachegrab` is a Python package that provides decorators for caching instance methods.


## Installation
```sh
pip install cachegrab
```


## Main Features

### Property Caching
- `deep_cached_property` ➔ Inspired by functools.cached_property, this decorator provides a deep copy of cached return values, ensuring they remain immutable after their initial access. The original return values are preserved in a dictionary named `self._deep_cache`.

### Attribute Caching
- `cached_attribute` ➔ Decorator that returns an instance attribute with the same name as the decorated function, prefixed with an underscore.
- `lazy_attribute` ➔ Identical to `cached_attribute`, except cached values are stored in a dictionary named `self._lazy_cache`.


## Example Usage

### Imports
```python
from cachegrab import deep_cached_property, cached_attribute
from functools import cached_property
```

### Decorate Instance Methods
Consider the example class `Dog` below:
- `toys` ➔ decorated with `cached_property` because toys can be buried and are therefore mutable.
- `is_good_boy` ➔ decorated with `deep_cached_property` because his good boy status is never in question.
- `tricks` ➔ decorated with `cached_attribute` to prevent direct overwrites.

```python
class Dog(object):

    @cached_property
    def toys(self):
        return {'ball','bone'}

    @deep_cached_property
    def is_good_boy(self):
        return True

    @cached_attribute
    def tricks(self):
        return {'sit','shake'}

    def bury_toys(self):
        while self.toys:
            self.toys.pop()
```

We will attempt to modify both cached properties:
```python
dog = Dog()
dog.bury_toys()
dog.good_boy = False
```

Let's look at the results:
```python
print('dog toys ➜', ', '.join(dog.toys) if dog.toys else '?')
print('good boy? ➜', dog.is_good_boy)
print('_deep_cache ➜', dog._deep_cache)

dog.tricks # access tricks property
print('_tricks ➜', dog._tricks)
```

<pre>
dog toys ➜ ?
good boy? ➜ True
_deep_cache ➜ {'is_good_boy': True}
_tricks ➜ {'sit','shake'}
</pre>
