import sys
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView

from logic.cube import Cube
from logic.kvaip import get_kvaip_info
from logic.min_coverage import get_min_coverage
from utils.generate import generate_data
from utils.utils import _


class MainWindow(QMainWindow):

    def __init__(self, file):
        super().__init__()
        uic.loadUi(file, self)
        self.show()
        self.generate_data()

    def generate_data(self):
        self.__x_count = int(self.number_edit.text())
        self.__cubes = generate_data(self.__x_count)
        # self.__x_count = self.__cubes[0].x.__len__()
        self.render_data_table()

    def render_data_table(self):
        if not self.__cubes:
            return

        self.__init_table_headers()

        for index, item in enumerate(self.__cubes):
            for j, value in enumerate(item.values()):
                MainWindow.__set_table_item(self.data_table, index, j, str(value))

    @staticmethod
    def __set_table_item(table, i, j, value):
        item = QTableWidgetItem(value, QTableWidgetItem.Type.real)
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(i, j, item)

    def __init_table_headers(self):
        column_count = self.__x_count + 2
        row_count = len(self.__cubes)
        self.data_table.setRowCount(row_count)
        self.data_table.setColumnCount(column_count)
        self.data_table.setHorizontalHeaderLabels(['x%d' % (i + 1) for i in range(self.__x_count)] + ['f', 'm'])
        for i in range(column_count):
            self.data_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def __render_cubes(self, cubes: List[Cube]):
        column_count = self.__x_count + 1

        self.result_cubes_table.setRowCount(len(cubes))
        self.result_cubes_table.setColumnCount(column_count)
        self.result_cubes_table.setHorizontalHeaderLabels(['x%d' % (i + 1) for i in range(self.__x_count)] + ['m'])
        for i in range(column_count):
            self.result_cubes_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i, cube in enumerate(cubes):
            for j, value in enumerate(cube.values(f=False)):
                MainWindow.__set_table_item(self.result_cubes_table, i, j, _(value))

    @staticmethod
    def __show_matrix(table, m_with_f_one, matrix):
        column_count = len(m_with_f_one)
        row_count = len(matrix)

        table.setRowCount(row_count)
        table.setColumnCount(column_count)
        table.setHorizontalHeaderLabels(['m%d' % m for m in m_with_f_one])
        for i in range(column_count):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                MainWindow.__set_table_item(table, i, j, _(value))

    def run_algorithm(self):
        result_cubes, m_with_f_one, matrix = get_kvaip_info(self.__cubes)
        self.__render_cubes(result_cubes)
        self.__show_matrix(self.matrix_table, m_with_f_one, matrix)
        required_rows = get_min_coverage(matrix)

        f = 3
        f = 3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow("window.ui")
    sys.exit(app.exec_())
