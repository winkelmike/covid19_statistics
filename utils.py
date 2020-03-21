
def etl_chain(arg, *funcs):
    """
    Runs a chain of variable functions in its input recursively
    :param arg: information on which the functions is ran
    :param funcs: variable function
    :return: function (chain) output
    """
    result = arg
    for f in funcs:
        result = f(result)
    return result
