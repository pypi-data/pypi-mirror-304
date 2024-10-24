from typing import Protocol, Sequence, Iterator, Iterable, TypeVar, Any, SupportsIndex, overload, runtime_checkable
from adaptivecard._base_types import Element, Choice, TableRow, Column, TableCell


_T_co = TypeVar("_T_co", covariant=True)

@runtime_checkable
class SequenceNotStr(Protocol[_T_co]):
    @overload
    def __getitem__(self, index: SupportsIndex, /) -> _T_co:
        ...

    @overload
    def __getitem__(self, index: slice, /) -> Sequence[_T_co]:
        ...

    def __contains__(self, value: object, /) -> bool:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[_T_co]:
        ...

    def index(self, value: Any, start: int = ..., stop: int = ..., /) -> int:
        ...

    def count(self, value: Any, /) -> int:
        ...

    def __reversed__(self) -> Iterator[_T_co]:
        ...

ListLike = SequenceNotStr

class DefaultNoneMeta(type):
    def __init__(self, name, bases, dict) -> None:
        super().__init__(name, bases, dict)
    def __repr__(self) -> str:
        return self.__name__

class DefaultNone(metaclass=DefaultNoneMeta):
    pass


def _check_type(value, types: tuple[type, ...]):
    if not isinstance(value, types):
        msg = f"{value} is not an instance of either of {[tp.__name__ for tp in types]}"
        raise TypeError(msg)


class TypedList(list):
    def __init__(self, data = None):
        if data is None:
            data = []
        if hasattr(data, "__iter__"):
            for value in data:
                _check_type(value, self._types)
        super().__init__(data)
    def append(self, __object) -> None:
        _check_type(__object, self._types)
        return super().append(__object)
    def insert(self, __index: SupportsIndex, __object: Any) -> None:
        _check_type(__object, self._types)
        return super().insert(__index, __object)
    def extend(self, elements: Iterable[Element]) -> None:
        for element in elements:    
            self.append(element)
    def __setitem__(self, __key, __value, /):
        _check_type(__value, self._types)
        return super().__setitem__(__key, __value)
    @overload
    def __getitem__(self, __i: int):
        ...
    @overload
    def __getitem__(self, __s: slice):
        ...
    def __getitem__(self, k):
        r = super().__getitem__(k)
        if isinstance(r, list):
            r = self.__class__(r)
        return r


def create_typed_list(name: str, types: tuple[type, ...]):
    """Returns a custom TypedList class which will raise for all types not defined in `types`"""
    return type(name, (TypedList,), {"_types": types})


ElementList = create_typed_list("ElementList", (Element,))
ColumnList = create_typed_list("ColumnList", (Column,))
RowList = create_typed_list("RowList", (TableRow,))
ChoiceList = create_typed_list("ChoiceList", (Choice,))
CellList = create_typed_list("CellList", (TableCell,))