from lark import Lark, Transformer, v_args
from lark.lexer import Lexer, Token

# class Statement(Transformer):
#
#     @v_args()
#     def assigment(self, args):
#         assigment = Assigment(args[0].children)
#         if args[0].data == "instanciation":
#             assigment.instanciation()
#         assigment.declaration()
#         print(assigment)
#
#     def expression(self, args):
#         return args


# class Assigment(Transformer):
#
#     def __init__(self, args):
#         types = {
#             "entier": Expression.arithmetic_exp,
#             "booléen": Expression.boolean_exp,
#             "texte": Expression.string_exp,
#             "liste": Expression.list_exp,
#         }
#         self.type = types[args[0].value]
#         self.name = args[1].value
#         self.args = args
#         self.value = None
#
#     def declaration(self):
#         return
#
#     def instanciation(self):
#         self.value = self.type(self.args[2])
#
#     def __str__(self):
#         return f"variable \nlabel : {self.name}\ntype : {self.args[0]}\nvalue : {self.value}"


class Evaluate(Transformer):

    variables_buffer = {}

    def __init__(self):
        print("Init")
        self.variables_buffer = {}

    def __str__(self):
        return str(self.variables_buffer)

    @v_args()
    def statement(self, args):
        return {
            "assigment": self._handle_assignment(args),
            "expression": self.expression(args[0].children),
            "loop": self.loop(args[0]),
            "condition": self.condition(args),
        }[args[0].data]

    def _handle_assignment(self, args):
        if len(args) == 2:  # Assignment
            var_name, expr = args
            self.variables_buffer[var_name] = self.expression(expr.children)
            return f"Assigned {self.expression(expr.children)} to {var_name}"
        else:  # Expression
            return self.expression(args[0].children)

    # https://lark-parser.readthedocs.io/en/latest/visitors.html#v-args
    @v_args()  # Annoted for easy decorator implementation if needed (wrapper)
    def expression(self, args):
        if isinstance(args[0], str):  # Var access
            return self.variables_buffer.get(args[0])
        elif len(args) == 1:  # Parenthesis
            return self.expression(args[0].children)
        else:  # Operation
            return self._eval_expression(args)

    @v_args()
    def loop(self, args):
        if args[0] == "tant que":
            condition = self.expression(args[1])
            while condition:
                self.block(args[2].children)
                condition = self.expression(args[1].children)
        elif args[0] == "pour chaque":
            var_name = args[1]
            list_name = args[3]
            for element in self.expression(list_name.children):
                self.variables_buffer[var_name] = element
                self.block(args[4].children)

    @v_args()
    def block(self, args):
        for arg in args:
            self.statement(arg.children)

    @v_args()
    def condition(self, args):
        condition = self.expression(args[1])
        if condition:
            self.block(args[2].children)
        elif len(args) > 3:  # else block
            self.block(args[3].children)

    def _eval_expression(self, args):
        """
        Evaluate the expression
        """
        left = self.expression(args[0])
        right = self.expression(args[2])
        op = args[1]

        if op in ("+", "-", "*", "/"):
            if not isinstance(left, (int, float)) or not isinstance(
                right, (int, float)
            ):
                raise TypeError(f"Operands must be numbers for {op} operation")
            return {
                "+": self._add(left, right),
                "-": self._sub(left, right),
                "*": self._mul(left, right),
                "/": self._div(left, right),
            }[op]
        elif op in ("<", "<=", ">", ">=", "==", "!="):
            return {
                "<": self._lt(left, right),
                "<=": self._lte(left, right),
                ">": self._gt(left, right),
                ">=": self._gte(left, right),
                "==": self._eq(left, right),
                "!=": self._neq(left, right),
            }[op]
        else:
            raise Exception(f"Unsupported operation: {op}")

    @staticmethod
    def _add(left, right):
        return left + right

    @staticmethod
    def _sub(left, right):
        return left - right

    @staticmethod
    def _mul(left, right):
        return left * right

    @staticmethod
    def _div(left, right):
        return left / right

    @staticmethod
    def _eq(left, right):
        return left == right

    @staticmethod
    def _neq(left, right):
        return left != right

    @staticmethod
    def _gt(left, right):
        return left > right

    @staticmethod
    def _lt(left, right):
        return left < right

    @staticmethod
    def _gte(left, right):
        return left >= right

    @staticmethod
    def _lte(left, right):
        return left <= right

    # @staticmethod
    # def arithmetic_exp(args):
    #     return ArithmeticExpr(args)
    #
    # @staticmethod
    # def boolean_exp(args):
    #     return BooleanExpr(args)
    #
    # @staticmethod
    # def string_exp(args):
    #     return StringExpr(args)
    #
    # @staticmethod
    # def list_exp(args):
    #     return ListExpr(args)


# class BooleanExpr(Expression):
#
#     def __init__(self, args):
#         expr = {
#             "atomic_value": BooleanExpr.atomic_value,
#             "negation": BooleanExpr.negation,
#             "conjonct": BooleanExpr.conjonct,
#             "disjonct": BooleanExpr.disjonct,
#         }
#         self.args = args
#         self.expr = expr[self.args.children[0].data]
#
#     @staticmethod
#     def atomic_value(args):
#         match args:
#             case "faux":
#                 return False
#             case "vrai":
#                 return True
#             case _:
#                 Exception("bad boolean expression")
#
#     @staticmethod
#     def negation(args):
#         return not args
#
#     @staticmethod
#     def conjonct(args):
#         return args[0] and args[1]
#
#     @staticmethod
#     def disjonct(args):
#         return args[0] or args[1]
#
#
# class ArithmeticExpr(Expression):
#
#     def __init__(self, args):
#         expr = {"atomic_value": ArithmeticExpr.atomic_value}
#         self.args = args
#         self.expr = expr[self.args.children[0].data]
#
#     @staticmethod
#     def atomic_value(args):
#         return int(args)
#
#
# class StringExpr(Expression):
#
#     def __init__(self, args):
#         expr = {"atomic_value": StringExpr.atomic_value}
#         self.args = args
#         self.expr = expr[self.args.children[0].data]
#
#     @staticmethod
#     def atomic_value(args):
#         return args[1 : len(args) - 1]
#
#
# class ListExpr(Expression):
#     """
#     DOES NOT WORK FOR NOW TODO
#     """
#
#     def __init__(self, args):
#         expr = {"atomic_value": ListExpr.atomic_value, "list_exp": ListExpr.list_exp}
#         self.args = args
#         self.expr = expr[self.args.children[0].data]
#
#     @staticmethod
#     def atomic_value(args):
#         return []  # returned empty list
#
#     @staticmethod
#     def list_exp(args):
#         """
#         "[" expression ("," expression)* "]" -> Parse this kind of list
#         """
#         return [args[0]] + args[1]


if __name__ == "__main__":
    with open("spf.lark", "r") as grammar:
        parser = Lark(grammar, start="statement", parser="lalr", transformer=Evaluate())
        while True:
            try:
                tree = parser.parse(input("> "))
                result = Evaluate().transform(tree)
                print(result)
            except Exception as e:
                print(e)
