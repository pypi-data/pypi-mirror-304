from typing import Any, Literal, overload, Iterable
from sys import maxsize
import adaptivecard._base_types as _base_types
from adaptivecard._mixin import Mixin
from adaptivecard.card_elements import TextBlock
from adaptivecard._utils import try_get_pixel_string
from adaptivecard._typing import ListLike, DefaultNone, ElementList, ColumnList, RowList, CellList



class Container(Mixin):
    """A grouping of elements. Containers are useful for grouping a number of related elements
    into one structure. All elements inside a container will inherit its styling attributes
    upon rendering of the card."""
    type = "Container"
    __slots__ = ('items', 'style', 'vertical_content_alignment', 'bleed', 'min_height',
                 'rtl', 'height', 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 items: _base_types.Element | ListLike[_base_types.Element] = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning", "accent"] = DefaultNone,
                 vertical_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.style = style
        self.vertical_content_alignment = vertical_content_alignment
        self.bleed = bleed
        self.min_height = min_height
        self.rtl = rtl
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    @property
    def empty(self):
        return len(self.items) == 0

    def append(self, element: _base_types.Element):
        if not isinstance(element, _base_types.Element):
            element = TextBlock(element)
        self.items.append(element)

    def extend(self, elements: Iterable[_base_types.Element]):
        for element in elements:
            self.append(element)

    def __len__(self):
        return self.items.__len__()

    def __iter__(self):
        return self.items.__iter__()

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, k):
        return self.items.__getitem__(k)
    
    def __setitem__(self, __key, __value):
        if isinstance(__value, str):
            __value = TextBlock(__value)
        return self.items.__setitem__(__key, __value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.items})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'items':
            if isinstance(__value, ListLike):
                __value = ElementList(__value)
            elif isinstance(__value, _base_types.Element):
                __value = ElementList([__value])
        elif __name == "min_height":
            __value = try_get_pixel_string(__value, __name)
        return super().__setattr__(__name, __value)

    def set_attributes_for_children(self, **kwargs):
        for child in self:
            child.set_attributes(**kwargs)


class Column(Mixin):
    """A column container. Columns must be grouped inside a ColumnSet."""
    type = "Column"
    __slots__ = ('items', 'background_image', 'bleed', 'fallback', 'min_height',
                 'rtl', 'separator', 'spacing', 'style', 'vertical_content_alignment', 'rtl',
                 'width', 'id', 'is_visible')
    def __init__(self,
                 items: _base_types.Element | ListLike[_base_types.Element | Any] | Any = DefaultNone,
                 background_image = DefaultNone,
                 bleed: bool = DefaultNone,
                 fallback: _base_types.Column = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                   | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 vertical_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 width: str | int | Literal["auto", "stretch"] = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.background_image = background_image
        self.bleed = bleed
        self.fallback = fallback
        self.min_height = min_height
        self.rtl = rtl
        self.separator = separator
        self.spacing = spacing
        self.select_action = select_action
        self.style = style
        self.vertical_content_alignment = vertical_content_alignment
        self.width = width
        self.id = id
        self.is_visible = is_visible

    def append(self, element: _base_types.Element):
        if not isinstance(element, _base_types.Element):
            element = TextBlock(element)
        self.items.append(element)

    def extend(self, elements: Iterable[_base_types.Element]):
        for element in elements:
            self.append(element)

    def __iter__(self):
        return self.items.__iter__()
    
    def __getitem__(self, __i, /):
        return self.items.__getitem__(__i)
    
    def __setitem__(self, __key, __value, /):
        return self.items.__setitem__(__key, __value)
    
    def __str__(self):
        return str([str(item) for item in self.items])
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "items":
            items = ElementList()
            if isinstance(__value, ListLike):
                for item in __value:
                    if not isinstance(item, _base_types.Element):
                        item = TextBlock(item)
                    items.append(item)

            elif not isinstance(__value, _base_types.Element):
                items.append(TextBlock(__value))

            else:
                items.append(__value)
            __value = items

        elif __name in ("min_height", "width"):
            if isinstance(__value, str):
                __value = __value.lower()
                if __value.isdigit():
                    __value += "px"
        return super().__setattr__(__name, __value)

    def set_attributes_for_children(self, **kwargs):
        for child in self:
            child.set_attributes(**kwargs)


class ColumnSet(Mixin):
    """A container for columns."""
    type = 'ColumnSet'
    __slots__ = ('columns', 'style', 'bleed', 'min_height', 'horizontal_alignment', 'height',
                 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 columns: ListLike[Column | ListLike[Any]] = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                   | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 min_height: str | int = DefaultNone,
                 horizontal_alignment: Literal["left", "center", "right"] | None = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] | None = DefaultNone,
                 separator: bool | None = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        if columns is DefaultNone:
            columns = ColumnList()
        self.columns: ColumnList = columns
        self.style = style
        self.bleed = bleed
        self.min_height = min_height
        self.horizontal_alignment = horizontal_alignment
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    def append(self, column: Column | ListLike):
        if isinstance(column, ListLike):
            column = Column(column)
        if not isinstance(column, (Column, ListLike)):
            raise TypeError(f"Expected Column or list-like object, got {type(column).__name__} instead")
        self.columns.append(column)

    def extend(self, columns: Iterable[_base_types.Column]):
        for column in columns:
            self.append(column)

    def __len__(self):
        return self.columns.__len__()

    def __iter__(self):
        return self.columns.__iter__()

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.columns.__getitem__(__k)
    
    def __setitem__(self, __key: int, __value: object, /):
        if not isinstance(__value, Column):
            raise TypeError()
        return self.columns.__setitem__(__key, __value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.columns})"
    
    def __str__(self):
        return "[" + ", ".join([str(col) for col in self.columns]) + "]"

    def __setattr__(self, __name: str, __value) -> None:
        if __name == "columns":
            if not isinstance(__value, ListLike):
                raise TypeError(f"expected a list-like value")
            columns = ColumnList()
            for item in __value:
                if not isinstance(item, Column):
                    item = Column(item)
                columns.append(item)
            __value = columns
        elif __name == "min_height":
            __value = try_get_pixel_string(__value, __name)
        return super().__setattr__(__name, __value)

    def set_attributes_for_children(self, **kwargs):
        for child in self:
            child.set_attributes(**kwargs)

class TableCell(Mixin):
    type = "TableCell"
    __slots__ = ('items', 'select_action', 'style', 'vertical_alignment', 'bleed',
                 'background_image', 'min_height', 'rtl')
    def __init__(self,
                 items: Any | ListLike[Any] = DefaultNone,
                 select_action: _base_types.Execute | _base_types.OpenUrl | _base_types.Submit
                 | _base_types.ToggleVisibility = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone,
                 vertical_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 bleed: bool = DefaultNone,
                 background_image: str = DefaultNone,
                 min_height: str | int = DefaultNone,
                 rtl: bool = DefaultNone):

        if items is DefaultNone:
            items = ElementList()
        self.items: ElementList = items
        self.select_action = select_action
        self.items = items
        self.style = style
        self.vertical_alignment = vertical_alignment
        self.bleed = bleed
        self.background_image = background_image
        self.min_height = min_height
        self.rtl = rtl

    def append(self, item: _base_types.Element | Any):
        if not isinstance(item, _base_types.Element):
            item = TextBlock(item)
        self.items.append(item)

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.items.__getitem__(__k)
    
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, _base_types.Element):
            __value = TextBlock(__value)
        return self.items.__setitem__(__key, __value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.items})"

    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.items]) + "]"

    def __iter__(self):
        return self.items.__iter__()
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "items":
            items = ElementList()
            if isinstance(__value, ListLike):
                for item in __value:
                    if not isinstance(item, _base_types.Element):
                        item = TextBlock(item)
                    items.append(item)
            elif not isinstance(__value, _base_types.Element):
                items.append(TextBlock(__value))
            __value = items
        elif __name == "min_height":
            __value = try_get_pixel_string(__value, __name)
        return super().__setattr__(__name, __value)


class TableRow(Mixin):
    type = "TableRow"
    __slots__ = ("cells", "style")
    def __init__(self,
                 cells: ListLike[Any] = DefaultNone,
                 style: Literal["default", "emphasis", "good", "attention", "warning",
                                "accent"] = DefaultNone):
        if cells is DefaultNone:
            cells = ElementList()
        self.cells = cells
        self.style = style
    
    def append(self, __object: _base_types.Element | Any, /):
        if not isinstance(__object, TableCell):
            __object = TableCell(__object)
        self.cells.append(__object)

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k):
        if isinstance(__k, slice):
            return self.__class__(cells=self.cells[__k])
        return self.cells.__getitem__(__k)
    
    def __setitem__(self, __key, __value):
        if not isinstance(__value, TableCell): __value = TableCell(__value)
        self.cells.__setitem__(__key, __value)

    def __contains__(self, value):
        return value in self.cells
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "cells":
            if not isinstance(__value, ListLike):
                raise TypeError("expected a list-like value")
            cells = CellList()
            for cell in __value:
                if not isinstance(cell, TableCell):
                    cell = TableCell(cell)
                cells.append(cell)
            __value = cells
        return super().__setattr__(__name, __value)

    def __len__(self):
        return self.cells.__len__()

    def __iter__(self):
        return self.cells.__iter__()
    
    def index(self, value=1, start: int = 0, stop: int = maxsize, /):
        return self.cells.index(value, start, stop)

    def count(self, value, /):
        return self.cells.count(value)
    
    def __reversed__(self):
        attrs = {attr_name: getattr(self, attr_name)
                 if attr_name != "cells"
                 else reversed(getattr(self, attr_name))
                 for attr_name in self.__slots__
                 if hasattr(self, attr_name)}
        return self.__class__(**attrs)

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.cells)})"

    def __str__(self):
        return "[" + ", ".join([str(cell) for cell in self.cells]) + "]"


class Table(Mixin):
    type = "Table"
    __slots__ = ('columns', 'rows', 'first_row_as_header', 'show_grid_lines', 'grid_style',
                 'horizontal_cell_content_alignment', 'vertical_cell_content_alignment', 'fallback', 'height',
                 'separator', 'spacing', 'id', 'is_visible')
    def __init__(self,
                 rows: ListLike[ListLike] = DefaultNone,
                 first_row_as_header: bool = DefaultNone,
                 columns: ListLike[int] = DefaultNone,
                 show_grid_lines: bool = DefaultNone,
                 grid_style: Literal["default", "emphasis", "good", "attention", "warning",
                                     "accent"] = DefaultNone,
                 horizontal_cell_content_alignment: Literal["left", "center", "right"] = DefaultNone,
                 vertical_cell_content_alignment: Literal["top", "center", "bottom"] = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone):

        if rows is DefaultNone:
            rows = RowList()
        self.rows: RowList = rows
        self.columns = columns if columns is not None else []
        self.first_row_as_header = first_row_as_header
        self.show_grid_lines = show_grid_lines
        self.grid_style = grid_style
        self.horizontal_cell_content_alignment = horizontal_cell_content_alignment
        self.vertical_cell_content_alignment = vertical_cell_content_alignment
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k, /):
        return self.rows.__getitem__(__k)
    
    def __setitem__(self, __key, __value, /):
        if not isinstance(__value, TableRow):
            raise TypeError
        return self.rows.__setitem__(__key, __value)
    
    def append(self, row: ListLike):
        if not isinstance(row, ListLike):
            raise TypeError
        if not isinstance(row, TableRow):
            row = TableRow(row)
        self.rows.append(row)
    
    # custom to_dict para lidar com o formato atípico do atributo columns dentro do json
    def to_dict(self):
        dic = super().to_dict()
        default_width = 1
        if hasattr(self, "columns") and self.columns:
            json_columns = [{"width": width} for width in self.columns]
        elif self.rows:
            json_columns = [{"width": default_width} for _ in self.rows[0]]
        else:
            json_columns = dic["columns"]
        dic["columns"] = json_columns
        return dic
    
    def __len__(self):
        return self.rows.__len__()
    
    def __repr__(self):
        s = " " * 6
        lstring = f",\n{s}".join([row.__repr__() for row in self.rows])
        lstring = f"{self.__class__.__name__}({lstring})"
        return lstring

    def __str__(self):
        lstring = ',\n'.join([str(row) for row in self.rows])
        lstring = f"[{lstring}]"
        return lstring

    def __iter__(self):
        return iter(self.rows)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "rows":
            rows = RowList()
            if not (isinstance(rows, ListLike) or \
            not all([isinstance(item, ListLike) for item in rows])):
                raise TypeError("argument 'rows' must be a collection of collections")
            for row in __value:
                if not isinstance(row, TableRow):
                    row = TableRow(row)
                rows.append(row)
            __value = rows
        return super().__setattr__(__name, __value)


class ActionSet(Mixin):
    type = "ActionSet"
    __slots__ = ("actions", "fallback", "height", "separator", "spacing", "id", "is_visible")
    def __init__(self,
                 actions: _base_types.Action | ListLike[_base_types.Action] = DefaultNone,
                 fallback: _base_types.Element = DefaultNone,
                 height: Literal["auto", "stretch"] = DefaultNone,
                 separator: bool = DefaultNone,
                 spacing: Literal["default", "none", "small", "medium", "large", "extraLarge",
                                  "padding"] | None = DefaultNone,
                 id: str = DefaultNone,
                 is_visible: bool = DefaultNone
                 ):
        if actions is DefaultNone:
            actions = ElementList()
        self.actions: ElementList = actions
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.is_visible = is_visible

    def __len__(self):
        return self.actions.__len__()

    @overload
    def __getitem__(self, __i: int):
        ...

    @overload
    def __getitem__(self, __s: slice):
        ...

    def __getitem__(self, __k):
        r = self.actions.__getitem__(__k)  
        if isinstance(__k, slice):
            r = self.__class__(r)
        return r

    def append(self, action: _base_types.Action) -> None:
        if not isinstance(action, _base_types.Action):
            raise TypeError("Can only append objetcs of type Action")
        self.actions.append(action)

    def extend(self, actions: Iterable[_base_types.Element]):
        for action in actions:
            self.append(action)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "actions":
            if isinstance(__value, _base_types.Action):
                __value = ElementList([__value])
            elif isinstance(__value, ListLike):
                __value = ElementList(__value)
        return super().__setattr__(__name, __value)
        

_base_types.Container.register(Container)
_base_types.Column.register(Column)
_base_types.ColumnSet.register(ColumnSet)
_base_types.Table.register(Table)
_base_types.TableRow.register(TableRow)
_base_types.TableCell.register(TableCell)
_base_types.ActionSet.register(ActionSet)