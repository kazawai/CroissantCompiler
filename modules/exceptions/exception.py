from lark.exceptions import UnexpectedInput

from modules.utils import global_var


class SPFException(Exception):
    """Global exception where an error occured in the program

    Attributes:
        message -> the message to print
        line_counter -> the current line where the error occured
    """

    def __init__(self, message="error occured from the spf program"):
        self.line_counter = global_var.line_counter
        self.message = message
        super().__init__("ERROR: " + self.message + f" at line {self.line_counter}")


class SPFSyntaxError(SPFException, UnexpectedInput):

    def __init__(self):
        super().__init__(message="syntax error")


class SPFUnknowVariable(SPFException):

    def __init__(self, label):
        super().__init__(message=f"unknown variable <{label}>")


class SPFUninitializedVariable(SPFException):

    def __init__(self, label):
        super().__init__(message=f"uninitialized variable <{label}>")


class SPFAlreadyDefined(SPFException):

    def __init__(self, label):
        super().__init__(message=f"redefined variable <{label}>")


class SPFIncompatibleType(SPFException):

    def __init__(self, label, type, value):
        super().__init__(
            message=f"type <{type}> incompatible with the value <{value}> for the variable <{label}>"
        )


class SPFIndexError(SPFException):

    def __init__(self, index, size):
        super().__init__(message=f"index <{index}> out of range [0, {size}]")
