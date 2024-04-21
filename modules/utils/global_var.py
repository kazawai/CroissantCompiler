def init():
    """
    All the needed variables needed "system-wide"
    """
    global context #variables
    global nested_counter #block
    global line_counter #number of lines passed
    global debug #flag for debug see -h
    global input #the user input TODO i guess ?
    context = {}
    nested_counter = 0
    line_counter = 1
    debug = False
    input = None
