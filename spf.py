from lark import Lark, Transformer

class Statement(Transformer):
    
    def assigment(self, args):
        assigment = Assigment(args[0].children)
        if args[0].data == "instanciation":
            assigment.instanciation()
        assigment.declaration()
        print(assigment)
    
    def expression(self, args):
        return args
    
class Assigment(Transformer):
    
    def __init__(self, args):
        types = {"entier" : Expression.arithmetic_exp, "booléen" : Expression.boolean_exp, "texte" : Expression.string_exp, "liste" : Expression.list_exp}
        self.type = types[args[0].value]
        self.name = args[1].value
        self.args = args
        self.value = None

    def declaration(self):
        return 
    
    def instanciation(self):
        self.value = self.type(self.args[2])

    def __str__(self):
        return f"variable \nlabel : {self.name}\ntype : {self.args[0]}\nvalue : {self.value}"



class Expression(Transformer):

    def __init__(self, args):
        self.args = args

    @staticmethod
    def boolean_exp(args):
        print(f"boolean_exp {args}")
        return BooleanExpr(args).expr(args.children[0].children[0].value)
    
    @staticmethod
    def arithmetic_exp(args):
        return ArithmeticExpr(args).expr(args.children[0].children[0].value)
    
    @staticmethod
    def string_exp(args):
        return StringExpr(args).expr(args.children[0].children[0].value)
    
    @staticmethod
    def list_exp(args):
        return ListExpr(args).expr(args.children[0].children[0].value)
    
class BooleanExpr(Expression):

    def __init__(self, args):
        expr = {"atomic_value" : BooleanExpr.atomic_value, "negation" : BooleanExpr.negation, "conjonct" : BooleanExpr.conjonct, "disjonct" : BooleanExpr.disjonct}
        self.args = args
        self.expr = expr[self.args.children[0].data]
        

    @staticmethod
    def atomic_value(args):
        match args:
            case "faux":
                return False
            case "vrai":
                return True
            case _:
                Exception("bad boolean expression")
    
    @staticmethod
    def negation(args):
        return not args
    
    @staticmethod
    def conjonct(args):
        return args[0] and args[1]
    
    @staticmethod    
    def disjonct(args):
        return args[0] or args[1]


class ArithmeticExpr(Expression):

    def __init__(self, args):
        expr = {"atomic_value" : ArithmeticExpr.atomic_value}
        self.args = args
        self.expr = expr[self.args.children[0].data]

    @staticmethod
    def atomic_value(args):
        return int(args)
    
class StringExpr(Expression):

    def __init__(self, args):
        expr = {"atomic_value" : StringExpr.atomic_value}
        self.args = args
        self.expr = expr[self.args.children[0].data]
    
    @staticmethod
    def atomic_value(args):
        return args[1:len(args) - 1]
    
class ListExpr(Expression):
    """
    DOES NOT WORK FOR NOW TODO
    """
    def __init__(self, args):
        expr = {"atomic_value" : ListExpr.atomic_value}
        self.args = args
        self.expr = expr[self.args.children[0].data]
    
    @staticmethod
    def atomic_value(args):
        return [] #returned empty list


if __name__ == "__main__":
    with open("spf.lark", "r") as grammar:
        parser = Lark(grammar, parser="lalr", transformer=(Statement()))
        while True:
            parser.parse(input(">"))
