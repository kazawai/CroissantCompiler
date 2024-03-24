from variable import VariableExpression
from entier import ArithmeticExpression
from booléen import BooleanExpr
from texte import StringExpression

class Statement:

    def __init__(self):
        self.enum_classes = [VariableExpression, ArithmeticExpression, BooleanExpr, StringExpression]

    def __getitem__(self, key):
        for enum_class in self.enum_classes:
            for member in enum_class:
                if key == member.name:
                    return member.value
        raise Exception(f"unknown identifier {key}")
