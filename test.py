from pprint import pprint
from min_coverage import get_min_coverage
from kvaip import get_kvaip_info
from generate import generate_data

data = generate_data(0)

two_cubes, four_cubes, result_cubes, m_with_f_one, matrix = get_kvaip_info(data)
print("2cubes")
pprint(two_cubes)

print("4cubes")
pprint(four_cubes)

print("cubes")
pprint(result_cubes)

print("m")
pprint(m_with_f_one)

print("matrix")
pprint(matrix)

required_rows = get_min_coverage(matrix)

print("selected_rows")
pprint(required_rows)