from typing import Type

from pydantic import ConfigDict
from pydantic._internal._model_construction import ModelMetaclass
from sqlalchemy import orm
from sqlalchemy.orm import DeclarativeBase


class LoadOptsMixin:

    _model: Type[DeclarativeBase]

    @classmethod
    def load_opts(cls):
        return LoadOptions(cls)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )



class LoadOptions:

    def __init__(self, model) -> None:
        self._model = model
        self._override = {}

    def __call__(self):

        visited = set()

        def get_opts(from_pd, exec = None):

            options = ()

            from_sa = from_pd._model.default
            if from_sa is None:
                raise ValueError(f'Не заполнена модель sqlalchemy: _model {from_pd}')

            for fname, finfo in from_pd.model_fields.items():

                to_pd = finfo.annotation
                if not isinstance(to_pd, ModelMetaclass):
                    continue

                to_sa = to_pd._model.default
                if to_sa is None:
                    raise ValueError(f'Не заполнена модель sqlalchemy: _model {to_pd}')

                rel = getattr(from_sa, fname)
                if rel in visited:
                    continue
                visited.add(rel)

                load_opt = self._override.get(rel) or orm.selectinload(rel)
                options += (get_opts(to_pd, load_opt),)

            return exec.options(*options) if exec else options

        return get_opts(self._model)

    def __setitem__(self, rel, opt):
        self._override[rel] = opt


