from math import ceil

from PySide2.QtCore import QAbstractTableModel, Qt


class FileTableModel(QAbstractTableModel):

    byte_in_row = 16

    def __init__(self, filename):
        super().__init__()
        file = open(filename, "rb")
        self._data = bytearray(file.read())
        self.row_count = len(self._data) / self.byte_in_row

    def rowCount(self, index):
        return self.row_count

    def columnCount(self, index):
        return self.byte_in_row

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # получаем номер байта в файле
            byte_in_file = index.row() * self.columnCount(index) + index.column()
            return '{:02x}'.format(self._data[byte_in_file]).upper()

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

