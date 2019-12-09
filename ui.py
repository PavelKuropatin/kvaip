import sys
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView

from logic.cube import Cube
from logic.min_coverage import get_min_coverage
from logic.quine import run_quine_mccluskey
from utils.generate import generate_data
from utils.utils import as_str

YELLOW = QColor(Qt.yellow)
WHITE = QColor(Qt.white)


class QuineMcCluskey(QMainWindow):

    def __init__(self, file):
        super().__init__()
        uic.loadUi(file, self)

        self.__x_count: int = 0
        self.__cubes: List[Cube] = []
        self.generate_data()

        self.show()

    def generate_data(self):
        self.__x_count = int(self.number_edit.text())
        self.__cubes = generate_data(self.__x_count)
        self.render_data_table()

    def render_data_table(self):
        if not self.__cubes:
            return

        self.__init_table_headers()

        for index, item in enumerate(self.__cubes):
            for j, value in enumerate(item.values()):
                QuineMcCluskey.__set_table_item(self.data_table, index, j, str(value))

    @staticmethod
    def __set_table_item(table, i, j, value, color=WHITE):
        item = QTableWidgetItem(value, QTableWidgetItem.Type.real)
        item.setTextAlignment(Qt.AlignCenter)
        if color:
            item.setBackground(color)
        table.setItem(i, j, item)

    def __init_table_headers(self):
        column_count = self.__x_count + 2
        row_count = 2 ** self.__x_count

        self.data_table.setRowCount(row_count)
        self.data_table.setColumnCount(column_count)
        self.data_table.setHorizontalHeaderLabels([f"x{i + 1}" for i in range(self.__x_count)] + ["f", "m"])
        for i in range(column_count):
            self.data_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def __render_cubes(self, cubes: List[Cube]):
        column_count = self.__x_count + 1

        self.result_cubes_table.setRowCount(len(cubes))
        self.result_cubes_table.setColumnCount(column_count)
        self.result_cubes_table.setHorizontalHeaderLabels([f"x{i + 1}" for i in range(self.__x_count)] + ["m"])
        for i in range(column_count):
            self.result_cubes_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i, cube in enumerate(cubes):
            for j, value in enumerate(cube.values(f=False)):
                QuineMcCluskey.__set_table_item(self.result_cubes_table, i, j, as_str(value))

    def __show_matrix(self, m_with_f_one, matrix, covered_rows):
        column_count = len(m_with_f_one)
        row_count = len(matrix)

        self.matrix_table.setRowCount(row_count)
        self.matrix_table.setColumnCount(column_count)
        self.matrix_table.setHorizontalHeaderLabels([f"m{m}" for m in m_with_f_one])
        for i in range(column_count):
            self.matrix_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i, row in enumerate(matrix):
            color = YELLOW if i in covered_rows else WHITE
            for j, value in enumerate(row):
                QuineMcCluskey.__set_table_item(self.matrix_table, i, j, as_str(value), color)

    def run_algorithm(self):
        result_cubes, m_with_f_one, matrix = run_quine_mccluskey(self.__cubes)
        self.__render_cubes(result_cubes)
        required_rows = get_min_coverage(matrix)
        self.__show_matrix(m_with_f_one, matrix, required_rows)
        self.covered_rows_label.setText(str([r + 1 for r in required_rows]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = QuineMcCluskey("window.ui")
    sys.exit(app.exec_())
