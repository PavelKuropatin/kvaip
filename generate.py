from constants import ONE, ZERO, DC


def generate_data(number: int):
    return [
        {"x": [0, 0, 0], "f": ZERO, "m": [0]},
        {"x": [0, 0, 1], "f": ONE, "m": [1]},
        {"x": [0, 1, 0], "f": DC, "m": [2]},
        {"x": [0, 1, 1], "f": ZERO, "m": [3]},
        {"x": [1, 0, 0], "f": ONE, "m": [4]},
        {"x": [1, 0, 1], "f": DC, "m": [5]},
        {"x": [1, 1, 0], "f": ONE, "m": [6]},
        {"x": [1, 1, 1], "f": DC, "m": [7]}
    ]
