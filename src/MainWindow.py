import sys

from PySide2.QtCore import QModelIndex
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QMainWindow, QTableView, QApplication

from src.FileTableModel import FileTableModel


class MainWindow(QMainWindow):

    def __init__(self, filename):
        super().__init__()
        self.setWindowTitle("Тест таблицы")
        table = QTableView(self)
        font = QFont()
        font.setFamily("Liberation Mono")
        font.setPointSize(8)
        table.setFont(font)
        table.horizontalHeader().setFont(font)
        table.verticalHeader().setFont(font)
        model = FileTableModel(filename)
        table.setModel(model)

        for column in range(model.columnCount(QModelIndex())):
            table.setColumnWidth(column, 20)

        self.setCentralWidget(table)

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QMainWindow using QWidget as central widget
    filename = r".\32M_RND.bin"
    window = MainWindow(filename)
    window.setMinimumSize(900, 600)
    window.show()
    sys.exit(app.exec_())