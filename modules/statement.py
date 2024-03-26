from modules.booléen import BooleanExpression
from modules.entier import ArithmeticExpression
from modules.liste import ListExpression
from modules.print import Print
from modules.texte import StringExpression
from modules.variable import VariableExpression as Variable


class Statement:

    def __init__(self):
        self.enum_classes = [
            Print,
            Variable,
            ArithmeticExpression,
            BooleanExpression,
            StringExpression,
            ListExpression
        ]

    def __getitem__(self, key):
        for enum_class in self.enum_classes:
            for member in enum_class:
                if key == member.name:
                    return member.value
        raise Exception(f"unknown identifier {key}")
