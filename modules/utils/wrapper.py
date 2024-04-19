from modules.exceptions.exception import SPFSyntaxError


class Wrapper:

    def __init__(self, f, authorized_types={}, label_op="none"):
        self.f = f
        self.authorized_types = authorized_types
        self.label_op = label_op

    def __call__(self, *args, **kwargs):
        if len(self.authorized_types.keys()) == 0 or self.authorized_type(*args):
            return self.f(*args, **kwargs)
        raise SPFSyntaxError(
            f"Le type {list(map(type, *args))} ne peut pas être utilisé pour cette opération {self.label_op} : {list(*args)}"
        )

    def authorized_type(self, args):
        key = type(args[0])
        if key not in self.authorized_types.keys():
            return False
        for i in range(1, len(args)):
            arg = args[i]
            if (
                len(self.authorized_types[key]) != 0
                and type(arg) not in self.authorized_types[key]
            ):
                return False
        return True
