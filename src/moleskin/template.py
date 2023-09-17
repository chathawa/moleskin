from __future__ import annotations
from abc import ABC, abstractmethod, ABCMeta
from typing import TypeVar, Generic, Tuple, cast, Callable
from gui.bases.state import StateModel

State = TypeVar('State', bound=StateModel)
SelectedState = TypeVar('SelectedState')
Form = TypeVar('Form', bound=Tuple)


class TemplateMeta(ABCMeta):
    def __new__(cls, name, bases, class_dict, **kwargs):
        template_class = super().__new__(cls, name, bases, class_dict)

        try:
            is_singleton = kwargs['singleton']
        except KeyError:
            if cls.__init__ is not TemplateMeta.__init__:
                raise UserWarning(
                    f"__init__ is overloaded in {cls} but "
                    f"the class was not defined as explicitly singleton or non-singleton"
                )

            try:
                is_singleton = next(getattr(base, '_is_singleton') for base in bases if hasattr(base, '_is_singleton'))
            except StopIteration:
                is_singleton = True

        template_class._is_singleton = is_singleton
        return template_class


class Template(ABC, Generic[State, SelectedState, Form], metaclass=TemplateMeta):
    _singleton: Template = None

    def __new__(cls, *args, **kwargs):
        if cls._is_singleton:
            if not cls._singleton:
                cls._singleton = super().__new__(cls)
            template = cls._singleton
        else:
            template = super().__new__(cls)

        return template

    @abstractmethod
    def select_state(self, state: State) -> SelectedState:
        pass

    @abstractmethod
    def bind(self, state: SelectedState, component) -> Form:
        pass

    def __getstate__(self):
        if not self._is_singleton:
            raise NotImplementedError("template class is not a singleton and does not implement hook __getstate__")

    def __setstate__(self, state: Tuple):
        if not self._is_singleton:
            raise NotImplementedError("template class is not a singleton and does not implement hook __setstate__")

        cast(Callable[[None], None], self.__init__)(*state)


FixedForm = TypeVar('FixedForm')


class FixedFormTemplate(
    Template[StateModel, None, FixedForm],
    ABC,
    Generic[FixedForm],
    singleton=False
):
    def __init__(self, *form):
        self._form: FixedForm = form

    def __getstate__(self):
        return self._form

    def __setstate__(self, form: FixedForm):
        self.__init__(*form)

    def select_state(self, state: StateModel):
        pass

    def bind(self, _, __):
        return self._form


__all__ = ['Template', 'FixedFormTemplate']
