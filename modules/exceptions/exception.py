from lark.exceptions import UnexpectedInput

from modules.utils import global_var


class SPFException(Exception):
    """Global exception where an error occured in the program

    Attributes:
        message -> the message to print
        line_counter -> the current line where the error occured
    """

    def __init__(
        self, message="Une erreur est survenue dans le programme spf.", context=""
    ):
        self.line_counter = global_var.line_counter
        # TODO : Print the line where the error occured in the program
        self.context = (
            context
            if context != ""
            else global_var.input.split("\n")[self.line_counter - 1]
        )
        self.message = message

        context_message = f"{self.context}\n" if self.context else ""

        error_message = f"Erreur: {self.message} à la ligne {self.line_counter}\n"

        super().__init__(f"\033[91m{error_message}\033[1m{context_message}\033[0m")

    def _create_context(self, context, index=-1, label=""):
        return (
            context
            + "\n"
            + "~" * index
            + "^" * len(label)
            + "~" * (len(context) - (index + len(label)))
            if index != -1
            else context + "\n" + "~" * len(context)
        )


class SPFSyntaxError(SPFException, UnexpectedInput):

    def __init__(self, message="", label=""):

        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)
        super().__init__("erreur de syntaxe : " + message, context=context)


class SPFUnknowVariable(SPFException):

    def __init__(self, label):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        # Spot the variable in the input context
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)

        super().__init__(message=f"variable inconnue <{label}>", context=context)


class SPFUninitializedVariable(SPFException):

    def __init__(self, label):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        # Spot the variable in the input context
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)

        super().__init__(message=f"variable non initialisée <{label}>", context=context)


class SPFAlreadyDefined(SPFException):

    def __init__(self, label):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        # Spot the variable in the input context
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)

        super().__init__(message=f"variable redéfinie <{label}>", context=context)


class SPFIncompatibleType(SPFException):

    def __init__(self, label, type, value):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        # Spot the variable in the input context
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)

        super().__init__(
            message=f"type <{type}> incompatible avec la valeur <{value}> pour la variable <{label}>",
            context=context,
        )


class SPFIndexError(SPFException):

    def __init__(self, index, size):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        context = super()._create_context(input_context)
        super().__init__(
            message=f"indice <{index}> hors des bornes [0, {size}]", context=context
        )


class SPFUnddefinedExpression(SPFException):

    def __init__(self, label, type):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        # Spot the variable in the input context
        label_index = input_context.find(label)
        context = super()._create_context(input_context, label_index, label)

        super().__init__(
            message=f"L'expression <{label}> n'est pas définie pour le type <{type}>",
            context=context,
        )

class SPFBadIdentifier(SPFException):

    def __init__(self, label):
        input_context = global_var.input.split("\n")[global_var.line_counter - 1]
        context = super()._create_context(input_context)
        super().__init__(
            message=f"L'identifiant de la variable <{label}> est mot clés",
            context=context
        )