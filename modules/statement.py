from modules.assignment import Assignment
from modules.expression import Expression
from modules.print import Print
from modules.variable import VariableExpression as Variable


class Statement:

    def __init__(self):
        self.enum_classes = [Print, Expression, Variable, Assignment]

    def __getitem__(self, key):
        for enum_class in self.enum_classes:
            for member in enum_class:
                if key == member.name:
                    return member.value
        raise Exception(f"unknown identifier {key}")
