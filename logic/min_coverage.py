from collections import defaultdict


def get_min_coverage(matrix):
    matrix = restructure_matrix(matrix)
    used_rows = []

    while not is_empty(matrix):
        max_i = find_row_with_max_one_count(matrix)

        columns_to_delete = get_columns_to_delete(matrix, max_i)
        delete_row(matrix, max_i)
        for j in columns_to_delete:
            delete_column(matrix, j)
        used_rows.append(max_i)

    return used_rows


def restructure_matrix(matrix):
    """
    restructure 'list' matrix (row of rows)
    to 'dict' matrix (dict of dict) 
    by {row:{column:value}} template
    """
    r_matrix = defaultdict(dict)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            r_matrix[i][j] = value

    return r_matrix


def find_row_with_max_one_count(matrix):
    """
    find row in matrix where count of one is max
    """
    max_i = -1
    max_i_count = -1
    for i, row in matrix.items():
        current_count = len([value for value in row.values() if value])
        if current_count > max_i_count:
            max_i = i
            max_i_count = current_count
    return max_i


def get_columns_to_delete(matrix, i):
    """
    get column numbers from specified row, where cell value is 1
    """
    return [
        j
        for j, value in matrix[i].items()
        if value
    ]


def is_empty(matrix):
    """
    check if matrix is empty
    """
    return not any(matrix.values())


def delete_row(matrix, i):
    """
    delete row from matrix by row index
    """
    del matrix[i]


def delete_column(matrix, j):
    """
    delete column from matrix by column index
    """
    for i, row in matrix.items():
        del row[j]
