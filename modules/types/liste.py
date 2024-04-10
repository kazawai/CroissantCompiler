from enum import Enum

from modules.utils.wrapper import Wrapper
from modules.exceptions.exception import SPFIndexError


def list_bc(args):
    return []


def list_gc(args):
    if type(args[0]) == list:
        return list(args[0])
    return args

def index_list(args):
    if args[1] < 0 or args[1] >= len(args[0]):
        raise SPFIndexError(args[1], len(args[0]))
    return args[0][args[1]]

def size_list(args):
    return len(args[0])

def range_list(args):
    return list(range(args[0], args[1]))

def add(args):
    if type(args[1]) != list:
        args[1] = [args[1]]
    print(args)
    print("je passe")
    return args[1] + [args[0]]

class ListExpression(Enum):
    LIST_BC = Wrapper(list_bc)
    LIST_GC = Wrapper(list_gc)

    INDEX_LIST = Wrapper(index_list, authorized_types={str: [int], list : [int]}, label_op="[] (indexer)")
    SIZE_LIST = Wrapper(size_list, authorized_types={str : [], list : []}, label_op="taille")
    RANGE_LIST = Wrapper(range_list, authorized_types={int : [int]}, label_op="[..:..]")
    SEQUENCE = Wrapper(lambda args: list(args))
    ADD = Wrapper(add, authorized_types={str : [list], list : [list], int : [list], bool : [list]}, label_op="ajouter .. dans ..")
