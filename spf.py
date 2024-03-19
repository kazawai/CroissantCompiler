from lark import Lark, Transformer
from enum import Enum


buffer = {}


class Type(Enum):
    INTEGER = 1
    BOOLEAN = 2
    STRING = 3
    LIST = 4


class Expression(Transformer):

    def declaration(self, args):
        return Value().declaration(args)
    
    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]
    
    def mul(self, args):
        return args[0] * args[1]
    
    def div(self, args):
        return args[0] / args[1]
    
    def number(self, args):
        return int(args[0])
    
    def neg(self, args):
        return - args[0]
        

class Value(Transformer):

    def declaration(self, args):
        match args[0]:
            case "entier":
                self.type = Type.INTEGER
            case "booléen":
                self.type = Type.BOOLEAN
            case "texte":
                self.type = Type.STRING
            case "liste":
                self.type = Type.LIST
        self.name = args[1]
        self.val = args[2]
        buffer[self.name] = self.val
        return self.val
    
    def call(self, args):
        print("je passe")
        if args[0] in buffer.keys:
            return buffer[args[0]]
        return(f"variable : {args[0]} does not exist")
    
"""
def ArithmeticOp(Transformater):

    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]
    
    def mul(self, args):
        return args[0] * args[1]
    
    def div(self, args):
        return args[0] / args[1]
    
    def number(self, args):
        return args[0]
    
    def neg(self, args):
        return - args[0]
"""




with open("spf.lark", "r") as file:
    grammar = file.read()
    parser = Lark(grammar, parser="lalr", transformer=(Expression()))
    statement = ""
    while(statement != "sortir"):
        statement = input(">")
        print(parser.parse(statement))


