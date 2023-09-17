from abc import ABC, ABCMeta
from typing import Protocol, TypeVar


class StateModelMeta(ABCMeta):
    pass


class StateModel(ABC, metaclass=StateModelMeta):
    pass


State = TypeVar('State', bound=StateModel)
SelectedState = TypeVar('SelectedState')


class Selector(Protocol[State, SelectedState]):
    def __call__(self, state: State) -> SelectedState:
        pass


__all__ = ['StateModelMeta', 'StateModel', 'State', 'SelectedState', 'Selector']
