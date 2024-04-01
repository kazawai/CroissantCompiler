from modules.types.booléen import BooleanExpression
from modules.types.comparison import ComparisonExpression
from modules.types.entier import ArithmeticExpression
from modules.types.liste import ListExpression
from modules.types.print import Print
from modules.types.texte import StringExpression
from modules.utils.variable import VariableExpression as Variable


class Statement:

    def __init__(self):
        self.enum_classes = [
            Print,
            Variable,
            ArithmeticExpression,
            BooleanExpression,
            StringExpression,
            ListExpression,
            ComparisonExpression
        ]

    def __getitem__(self, key):
        for enum_class in self.enum_classes:
            for member in enum_class:
                if key == member.name:
                    return member.value
        raise Exception(f"unknown identifier {key}")
