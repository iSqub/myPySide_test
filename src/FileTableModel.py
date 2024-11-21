from PySide2.QtCore import QAbstractTableModel, Qt


class FileTableModel(QAbstractTableModel):
    byte_in_row = 16

    def __init__(self, filename, bytes_is_row):
        super().__init__()
        file = open(filename, "rb")
        self.byte_in_row = bytes_is_row
        self.text_column_idx = bytes_is_row
        self._data = bytearray(file.read())
        self.row_count = int(len(self._data) / self.byte_in_row)

    def rowCount(self, index):
        return self.row_count

    def columnCount(self, index):
        return self.byte_in_row + 1

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == self.text_column_idx:
                # последняя колонка с текстом
                start = index.row() * self.byte_in_row
                finish = start + self.byte_in_row
                text_byte = self._data[start:finish]
                return self.bytesToText(text_byte)

            # получаем номер байта в файле
            byte_in_file = index.row() * self.byte_in_row + index.column()
            return '{:02x}'.format(self._data[byte_in_file]).upper()

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal and section == self.text_column_idx:
            return "Текст"
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return self.hex(section).zfill(len(self.hex(self.row_count)))
        elif role == Qt.DisplayRole:
            return self.hex(section)

    def bytesToText(self, text_byte):
        text = ''
        for byte in text_byte:
            if byte > 31:
                text += chr(byte)
            else:
                text += '.'
        return text

    def hex(self, value):
        return '{:02x}'.format(value).upper()