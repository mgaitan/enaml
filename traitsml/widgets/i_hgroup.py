from traits.api import Enum

from .i_group import IGroup

from ..enums import Direction


class IHGroup(IGroup):
    """ A horizontally grouping container.

    This is a convienence subclass of IGroup which restricts the 
    layout direction to horizontal.

    Attributes
    ----------
    direction : Enum(Direction.LEFT_TO_RIGHT, Direction.RIGHT_TO_LEFT)
    	The layout direction restricted to horizontal directions.
    
    """	
    direction = Enum(Direction.LEFT_TO_RIGHT, Direction.RIGHT_TO_LEFT)

