from random import choice

from logic.cube import Cube
from utils.constants import F_ALL


def generate_data(number: int):
    cubes = [
        Cube(
            x=[
                int(bit)
                for bit in format(i, f'0{number}b').zfill(number)
            ],
            f=choice(F_ALL),
            m=i
        )
        for i in range(2 ** number)
    ]
    return cubes
