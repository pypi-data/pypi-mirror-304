from abc import ABC



class Element(ABC):
    pass


class AdaptiveCard(ABC):
    pass


class ActionSet(Element):
    pass


class Action(ABC):
    pass


class ShowCard(Action):
    pass


class Execute(Action):
    pass


class OpenUrl(Action):
    pass


class Submit(Action):
    pass


class ToggleVisibility(Action):
    pass

class Table(ABC):
    pass


class TableRow(Table):
    pass


class TableCell(Table):
    pass


class Content(ABC):
    pass


class Message(ABC):
    pass


class Container(Element):
    pass


class ColumnSet(Element):
    pass


class Column(ABC):
    pass


class TextBlock(Element):
    pass


class Image(Element):
    pass


class ImageSet(Element):
    pass


class Text(Element):
    pass


class Number(Element):
    pass


class Date(Element):
    pass


class Time(Element):
    pass


class DataQuery(ABC):
    pass


class Toggle(Element):
    pass


class Choice(ABC):
    pass


class ChoiceSet(Element):
    pass


Element.register(AdaptiveCard)
Element.register(Table)
Element.register(TableRow)
Element.register(TableCell)
Element.register(ColumnSet)
Element.register(Column)
Element.register(Container)
Element.register(TextBlock)
Element.register(Image)
Element.register(ImageSet)
Element.register(Message)
Element.register(Content)
Element.register(Action)
Element.register(ActionSet)
Element.register(Text)
Element.register(Number)
Element.register(Date)
Element.register(Time)
Element.register(DataQuery)
Element.register(Toggle)
Element.register(Choice)
Element.register(ChoiceSet)
Action.register(ShowCard)
Action.register(Execute)
Action.register(OpenUrl)
Action.register(Submit)
Action.register(ToggleVisibility)
