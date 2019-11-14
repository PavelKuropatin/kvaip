__author__ = "student"

from collections import defaultdict
from itertools import groupby
from pprint import pprint
from constants import ONE, ZERO, DC

def get_kvaip_info(data):

    groups = get_groups(data)
    pairs = get_pairs(groups)

    
    two_cubes = get_two_cubes(pairs, data)
    # pprint(two_cubes)

    four_cubes = get_four_cubes(two_cubes)
    # pprint(four_cubes)

    result_cubes = merge_cubes(two_cubes, four_cubes)

    m = get_m_with_f_one(data)

    matrix = build_matrix_for_coverage(result_cubes, m)

    return two_cubes, four_cubes, result_cubes, m, matrix

def build_matrix_for_coverage(result_cubes, m_with_f_one):
    column_indexes = {i: m for i, m in enumerate(m_with_f_one)}
    row_indexes = {i: x for i, x in enumerate(result_cubes)}

    matrix = []
    for i, x in row_indexes.items():
        row = []
        for j, m in column_indexes.items():
            row.append(1 if m in x["m"] else 0)
        matrix.append(row)
    return matrix

def get_m_with_f_one(data):
    return [
        row["m"][0] 
        for row in data 
        if row["f"] == ONE
    ]

def merge_cubes(two_cubes, four_cubes):
    unused_two_cubes = []
    for two_cube in two_cubes:
        for four_cube in four_cubes:
            if two_cube["m"].difference(four_cube["m"]):
                unused_two_cubes.append(two_cube)
    return unused_two_cubes + four_cubes
    
def get_two_cubes(pairs, data):
    two_cubes_indexes = []
    for left, right in pairs:
        for l in left:
            for r in right:
                if is_match(data[l]["x"], data[r]["x"]):
                    two_cubes_indexes.append((l, r))

    return [      {
            "m": {i, j},
            "x": merge_arrays(data[i]["x"], data[j]["x"])
        }
        for i, j in two_cubes_indexes
        ]

def get_groups(data, f_values = [ONE, DC]):
    """
    group data by count of one in "x" array
    skip row if its "f" is not in f_values
    return one_count:row_numbers(from "m") dictionary
    """
    data = [row for row in data if row["f"] in f_values]
    grouped_data = groupby(data, lambda row: sum(row["x"]))

    return {
        one_count : [
            row["m"][0]
            for row in rows
        ]
        for one_count, rows in grouped_data
    }


def get_pairs(groups):
    return [
        (groups[list(groups.keys())[i]], groups[list(groups.keys())[i + 1]])
        for i in range(len(groups.keys()) - 1)
        ]


def is_match(arr1, arr2):
    """
    compare array by value sequentially
    return false if count of mistached values is more then 1
    """
    diff = 0
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            diff += 1
        if diff == 2:
            return False
    return True

def merge_arrays(arr1, arr2):
    """
    merge arrays by values sequentially
    if values don't match the DC valus will be set.
    """
    return [
        DC if arr1[i] != arr2[i] else arr1[i]
        for i in range(len(arr1))
    ]

def get_four_cubes(two_cubes):
    four_cubes = []
    for i in range(len(two_cubes)):
        for j in range(i + 1, len(two_cubes)):
            arr1 = two_cubes[i]["x"]
            arr2 = two_cubes[j]["x"]
            if is_match(arr1, arr2):
                item = {
                    "x": merge_arrays(arr1, arr2),
                    "m": set(list(two_cubes[i]["m"]) + list(two_cubes[j]["m"]))
                }
                if item not in four_cubes:
                    four_cubes.append(item)
    return four_cubes
