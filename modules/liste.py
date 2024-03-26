from enum import Enum

from modules.wrapper import Wrapper


def list_bc(args):
    return []


def list_gc(args):
    return list(args[0])


def concat_list(args):
    return args[0] + args[1]


def index_list(args):
    return args[0][args[1]]


def size_list(args):
    return len(args[0])


def range_list(args):
    return list(range(args[0], args[1]))


class ListExpression(Enum):
    LIST_BC = Wrapper(list_bc)
    LIST_GC = Wrapper(list_gc)
    CONCAT_LIST = Wrapper(concat_list)
    INDEX_LIST = Wrapper(index_list)
    SIZE_LIST = Wrapper(size_list)
    RANGE_LIST = Wrapper(range_list)
    SEQUENCE = Wrapper(lambda args: list(args))
