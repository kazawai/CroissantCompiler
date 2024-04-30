from enum import Enum

from modules.exceptions.exception import SPFIndexError
from modules.utils.variable import Variable
from modules.utils.wrapper import Wrapper


def list_bc(_): 
    """
    return the basis case of a list -> empty list
    """
    return []


def list_gc(args):
    """
    return the general case -> a list of arbitrary sequence of elements
    """
    if type(args[0]) == list:
        return list(args[0])
    return args


def index_list(args):
    """
    return element of a list by a given index
    """
    index = args[1] 
    print(index)
    print(args)
    if index < 1 or index > len(args[0]):
        raise SPFIndexError(index, len(args[0]))
    return args[0][index - 1]


def size_list(args):
    """
    give the length of a list
    """
    return len(args[0])


def range_list(args):
    """
    by using range mechanism, return a list
    """
    return list(range(args[0], args[1] + 1))


def add(args):
    """
    append an element to the end of list
    """
    current_value = Variable.call(args[1])
    new_value = current_value + [args[0]]
    Variable.modification([args[1], new_value])


def list_add(args):
    """
    concatenate 2 lists
    """
    return args[0] + args[1]


class ListExpression(Enum):
    """
    All semantic rules of list objects
    """
    LIST_BC = Wrapper(lambda _ : [])
    LIST_GC = Wrapper(list_gc)

    INDEX_LIST = Wrapper(
        index_list, authorized_types={str: [int], list: [int]}, label_op="[] (indexer)"
    )
    SIZE_LIST = Wrapper(
        size_list, authorized_types={str: [], list: []}, label_op="taille"
    )
    RANGE_LIST = Wrapper(range_list, authorized_types={int: [int]}, label_op="[..:..]")
    SEQUENCE = Wrapper(lambda args: list(args))
    ADD = Wrapper(
        add,
        authorized_types={
            str: [str, list],
            list: [str, list],
            int: [str, list],
            bool: [str, list],
        },
        label_op="ajouter .. dans ..",
    )
    LIST_ADD = Wrapper(
        list_add, authorized_types={list: [list]}, label_op="[..] + [..]"
    )
