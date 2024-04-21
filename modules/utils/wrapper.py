from modules.exceptions.exception import SPFSyntaxError


class Wrapper:
    """
    Wrapp all semantic rules to check if the types of argument are respected according to the developpers (i.e. us :)
    """
    def __init__(self, f, authorized_types={}, label_op="none"):
        """
        Instanciate wrapper with given parameters 

        PARAMS
        ------

            - f : function to call after type verification, thus a semantic rule (see enum)
            - authorized_types : the types allowed to make a given semantic rule
            - label_op : the name of the semantic rule, mainly used for debug if type not respected
        """
        self.f = f
        self.authorized_types = authorized_types
        self.label_op = label_op

    def __call__(self, *args, **kwargs):
        """
        Call the function attribute f after type verification.
        If type verification shows us that the operation is not valid, then a error is raised
        """
        if len(self.authorized_types.keys()) == 0 or self.authorized_type(*args):
            return self.f(*args, **kwargs)
        raise SPFSyntaxError(
            f"Le type {list(map(type, *args))} ne peut pas être utilisé pour cette opération {self.label_op} : {list(*args)}",
            label=self.label_op,
        )

    def authorized_type(self, args):
        """
        Check the types specified at the creation object moment and return
            - true if types respected
            - false otherwise
        """
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
