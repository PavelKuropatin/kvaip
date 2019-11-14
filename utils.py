from constants import ONE, ZERO, DC


def _(x):
    if x == ONE:
        return "1"
    if x == ZERO:
        return "0"
    if x == DC:
        return "DC"
    return str(x)
