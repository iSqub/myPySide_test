from PySide2.QtCore import QAbstractTableModel, Qt


class ContactTableModel(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self.column_header = ['Обозначение','Вывод корпуса','Статус']
        self.column_count = len(self.column_header)
        self._data = data
        self.row_count = len(self._data)

    def rowCount(self, index):
        return self.row_count

    def columnCount(self, index):
        return self.column_count

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

    def headerData(self, section, orientation, role):
        if (role == Qt.DisplayRole and orientation == Qt.Horizontal):
            return self.column_header[section]
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return section+1