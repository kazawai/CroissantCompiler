from modules.types.booléen import BooleanExpression
from modules.types.comparison import ComparisonExpression
from modules.types.entier import ArithmeticExpression
from modules.types.liste import ListExpression
from modules.types.system import System
from modules.types.texte import StringExpression
from modules.utils.variable import VariableExpression as Variable


class Statement:
    """
    Statement class group all the enums (semantic rules) inside a list for clean code (Instead of importing all the rules inside the interpreter)
    in addition to unknown semantic rules. (used for dev debug)
    """
    def __init__(self):
        self.enum_classes = [
            System,
            Variable,
            ArithmeticExpression,
            BooleanExpression,
            StringExpression,
            ListExpression,
            ComparisonExpression        
        ]

    def __getitem__(self, key):
        """
        Will look for a given semantic rule 
        Raise an exception of the rule is unknown
        """
        for enum_class in self.enum_classes:
            for member in enum_class:
                if key == member.name:
                    return member.value
        raise Exception(f"unknown identifier {key}")
