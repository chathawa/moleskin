from abc import ABC, ABCMeta
from typing import Protocol, Generic, TypeVar


class StateModelMeta(ABCMeta):
    pass


class StateModel(ABC, metaclass=StateModelMeta):
    pass


State = TypeVar('State', bound=StateModel)


class Selector(Protocol[State]):
    def __call__(self, state: State):
        pass


__all__ = ['StateModelMeta', 'StateModel', 'Selector']
