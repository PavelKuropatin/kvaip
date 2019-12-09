from utils.constants import ONE, ZERO, DC


def as_str(x):
    if x == ONE:
        return "1"
    if x == ZERO:
        return "0"
    if x == DC:
        return "dc"
    return str(x)
