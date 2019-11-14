import sys
from pprint import pprint

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView

from generate import generate_data
from kvaip import get_kvaip_info
from min_coverage import get_min_coverage
from utils import _


class MainWindow(QMainWindow):

    def __init__(self, file):
        super().__init__()
        uic.loadUi(file, self)
        self.show()
        self.generate_data()
        self.__data = None

    def generate_data(self):
        number = self.number_edit.text()
        self.__data = generate_data(number)
        self.render_data_table()
        self.run_algorithm()

    def render_data_table(self):
        if not self.__data:
            return
        data_table: QTableWidget = self.data_table
        self.__init_table_headers(self.__data)

        for i, row in enumerate(self.__data):
            j = 0
            for x in row["x"]:
                MainWindow.__set_table_item(data_table, i, j, str(x))
                j += 1
            MainWindow.__set_table_item(data_table, i, j, _(row["f"]))
            MainWindow.__set_table_item(data_table, i, j + 1, ", ".join([str(m) for m in row["m"]]))


    @staticmethod
    def __set_table_item(table, i, j, value):
        item = QTableWidgetItem(value, QTableWidgetItem.Type.real)
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(i, j, item)

    def __init_table_headers(self, data):
        x_count = len(data[0]["x"])
        column_count = x_count + 2
        row_count = len(data)

        self.data_table.setRowCount(row_count)
        self.data_table.setColumnCount(column_count)
        self.data_table.setHorizontalHeaderLabels(['x%d' % (i + 1) for i in range(x_count)] + ['f', 'm'])
        for i in range(column_count):
            self.data_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    @staticmethod
    def __render_cubes(table, cubes):
        x_count = len(cubes[0]["x"])
        column_count = x_count + 1

        table.setRowCount(len(cubes))
        table.setColumnCount(column_count)
        table.setHorizontalHeaderLabels(['x%d' % (i + 1) for i in range(x_count)] + ['m'])
        for i in range(column_count):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i, row in enumerate(cubes):
            j = 0
            for x in row["x"]:
                MainWindow.__set_table_item(table, i, j, _(x))
                j += 1
            MainWindow.__set_table_item(table, i, j, ", ".join([str(m) for m in row["m"]]))

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
        two_cubes, four_cubes, result_cubes, m_with_f_one, matrix = get_kvaip_info(self.__data)
        self.__render_cubes(self.two_cubes_table, two_cubes)
        self.__render_cubes(self.four_cubes_table, four_cubes)
        self.__render_cubes(self.result_cubes_table, result_cubes)
        self.__show_matrix(self.matrix_table, m_with_f_one, matrix)
        required_rows = get_min_coverage(matrix)

        print("selected_rows")
        pprint(required_rows)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow("window.ui")
    sys.exit(app.exec_())
