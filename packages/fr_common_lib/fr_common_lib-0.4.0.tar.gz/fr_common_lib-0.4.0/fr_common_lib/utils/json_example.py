from copy import deepcopy
from typing import Type


class JsonExample(dict):

    def __init__(self, cls: Type):
        super().__init__()
        self['content'] = {
            'application/json': {
                'examples': {
                    cls.__name__: {
                        'value':{
                            'type': cls.__name__,
                            **{
                                key: value  for key, value in cls.__dict__.items()
                                if not (key.startswith('__') and key.endswith('__'))
                            }
                        }
                    }
                }
            }
        }


    @property
    def _examples(self):
        return self['content']['application/json']['examples']

    @_examples.setter
    def _examples(self, value):
        self['content']['application/json']['examples'] = value

    def __or__(self, other):
        if isinstance(other, self.__class__):
            new = deepcopy(self)
            new._examples = (
                    self._examples | other._examples
            )
            return new
        return super().__or__(other)
