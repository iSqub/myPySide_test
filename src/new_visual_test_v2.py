# -*- coding: utf-8 -*-
import time
import os
import copy
import sys

from PySide2.QtCore import (Qt,QAbstractTableModel,Slot)
from PySide2.QtGui import (QFont, QColor)
from PySide2.QtWidgets import (QApplication,QMainWindow,QTableView,QAbstractItemView,QHBoxLayout,QGridLayout,QScrollBar,QPushButton,QWidget)


filename = r".\32M_RND.bin"

def convert_to(number, base, length=2,  upper=True):
    digits = '0123456789abcdef'
    if base > len(digits): return None
    result = ''
    while number > 0:
        result = digits[number % base] + result
        number //= base
    if(len(result) < length):
        while len(result) != length:
            result = '0' + result
    return result.upper() if upper else result

#----------------------------------------------------------------------------
#Создаем заголовок для столбцов, он создается один раз
def CreateColumnHeader(charactersPerCell=2,cellBaseLength=2,cellsPerRow=32,cellBase=16,showString=True,textCoding = 'cp1251'):
    columnHeader = []
    reqColLenhth = len(convert_to(number=int(charactersPerCell/cellBaseLength)*cellsPerRow,base=cellBase, length=cellBaseLength))#Вычисляем максимальное значение, чтобы узнать необходимое количество символов
    outputString = ""
    for i in range(cellsPerRow):
        colName = int(charactersPerCell/cellBaseLength)*i
        columnName = convert_to(number=colName,base=cellBase, length=reqColLenhth)
        columnHeader.append(columnName)
        outputString += columnName + ' '
    if(showString):
        columnName = "Текс("+textCoding+")"
        columnHeader.append(columnName)
        outputString += columnName
    outputString += '\n'
    return columnHeader
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#Создаем заголовок для строк, он создается каждый раз
def CreateRowHeader(charactersPerCell=2,cellBaseLength=2,length=1024,charactersPerRow=64,rowOffset=0):
    rowHeader = []
    maxRowCount =  int(length / (charactersPerRow/cellBaseLength))
    if(maxRowCount == 0):
        maxRowCount = 1
    rowLength = int(charactersPerRow/cellBaseLength)
    reqRowLenhth = len(convert_to(number=maxRowCount*rowLength,base=16, length=2))
    for i in range(maxRowCount):
        rowName = int(charactersPerCell/cellBaseLength)*rowLength*(i+rowOffset)
        rowHeader.append(convert_to(number=rowName,base=16, length=reqRowLenhth))
    return rowHeader
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
def CreateDataTable(databytes,cellBase=16,cellBaseLength=2,charactersPerCell=2,cellsPerRow=32,showString=True,textCoding='cp1251'):
    charactersPerRow = charactersPerCell*cellsPerRow
    temporaryCellString = ""
    temporaryRowString = ""
    temporaryRow = []
    finalTextData = []
    for i, data_byte in enumerate(databytes):
        temporaryRowString += convert_to(number=data_byte,base=cellBase, length=cellBaseLength)#Переводим байты в строку нужной системы счисления
        if(len(temporaryRowString) >= charactersPerRow):#мы набрали необходимое количество символов для строки
            temporaryRow.clear()
            temporaryTextString = ""
            stringRowConvertToText = ""
            for j in range(cellsPerRow):#Заполняем ячейки строки
                start_index = j*charactersPerCell
                stop_index = start_index + charactersPerCell
                temporaryCellString = temporaryRowString[start_index:stop_index:]
                temporaryRow.append(copy.deepcopy(temporaryCellString))
                stringRowConvertToText += temporaryCellString#Cобираем строку из символов
            if(showString):#Если нужно то добавляем отображение текста строки
                charCount = len(stringRowConvertToText)
                j = 0
                k = 0
                #print(stringRowConvertToText)
                while(k<charCount):
                    start_index = j*cellBaseLength
                    stop_index = start_index + cellBaseLength
                    textChar = stringRowConvertToText[start_index:stop_index:]
                    j += 1
                    k += cellBaseLength
                    #print(textChar, j, charCount)
                    char = int(textChar,base=cellBase)
                    try:
                        if(char > 31):
                            temporaryCellString = char.to_bytes(1,'big').decode(textCoding)
                        else:
                            temporaryCellString = '.'
                    except:
                        temporaryCellString = '.'
                    temporaryTextString += temporaryCellString
                temporaryRow.append(temporaryTextString)
            finalTextData.append(copy.deepcopy(temporaryRow))
            temporaryRowString = temporaryRowString[charactersPerRow::]#Отбросили сиволы ушедшие в предыдущю строку
    return finalTextData
#----------------------------------------------------------------------------

class TableModel(QAbstractTableModel):
    def __init__(self, data, hheaders, vheaders, reference_data):
        super().__init__()
        self._data = data
        self.reference_data = reference_data
        self.hheaders = hheaders
        self.vheaders = vheaders

    def set_data(self,data):
        self._data = data

    def set_vheaders(self,vheaders):
        self.vheaders = vheaders

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            try:
                reference_value = self.reference_data[index.row()][index.column()]
                if (value != reference_value):
                    return QColor('red')
            except:
                pass

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.hheaders[section])

            if orientation == Qt.Vertical:
                return str(self.vheaders[section])

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        open_file = open(filename, "rb")
        self.opened_file = open_file.read()
        open_file.close()
        self.length = len(self.opened_file)
        self.textCoding = 'cp1251'
        self.cellBase = 16
        self.cellBaseLength = 2
        self.showString = True #Нужно добавить отображение текста, возможно только в том случае если в одну строку помещается целое количество байт
        self.charactersPerCell = 2 #Количество символов в выбраной системе счисления в одной ячейке
        self.cellsPerRow = 16 #Количество ячеек в одной строке
        self.charactersPerRow = self.charactersPerCell*self.cellsPerRow
        
        #----------------------------------------------------------------------------
        #Проверяем длину файла, если нужно добавляем до одной строки 
        if(self.length >= (self.charactersPerRow/self.cellBaseLength)):
            pass
        else:
            add_zero_count = int(self.charactersPerRow/self.cellBaseLength) - self.length
            self.opened_file += bytes([0 for j in range(add_zero_count)])
            self.length += add_zero_count
        #----------------------------------------------------------------------------

        finalTextData = CreateDataTable(databytes=self.opened_file[0:512],cellBase=self.cellBase,cellBaseLength=self.cellBaseLength,charactersPerCell=self.charactersPerCell,cellsPerRow=self.cellsPerRow,showString=self.showString,textCoding=self.textCoding)
        referenceTextData = copy.deepcopy(finalTextData)
        self.columnHeader = CreateColumnHeader(charactersPerCell=self.charactersPerCell,cellBaseLength=self.cellBaseLength,cellsPerRow=self.cellsPerRow,cellBase=self.cellBase,showString=self.showString,textCoding=self.textCoding)
        rowHeader = CreateRowHeader(charactersPerCell=self.charactersPerCell,cellBaseLength=self.cellBaseLength,length=self.length,charactersPerRow=self.charactersPerRow,rowOffset=0)
        
        open_file.close()

        self.table = QTableView()
        self.model = TableModel(finalTextData,self.columnHeader,rowHeader,referenceTextData)
        self.table.setModel(self.model)
        font = QFont()
        font.setFamily("Liberation Mono")
        font.setPointSize(8)
        self.table.setFont(font)
        #font.setBold(True)
        self.table.horizontalHeader().setFont(font)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        #self.table.setSizeAdjustPolicy(QAbstractItemView.AdjustToContents)
        self.table.setFixedSize(self.table.size().width()+25,self.table.size().height()+220)
        
        self.scrollbar = QScrollBar()
        self.scrollbar.setOrientation(Qt.Vertical)
        self.scrollbar.setMinimum(0)
        self.scrollbar.setValue(0)
        self.scrollbar.setMaximum((self.length//512)-1)
        #self.scrollbar.setEnabled(False)
        self.scrollbar.valueChanged.connect(self.wheelEvent)

        self.pushbutton = QPushButton("Обновить!") 
        self.table_layout = QHBoxLayout()
        self.table_layout.addWidget(self.table)
        self.table_layout.addWidget(self.scrollbar)
        self.layout = QGridLayout(self)
        self.layout.addLayout(self.table_layout, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.pushbutton, 1, 0, Qt.AlignmentFlag.AlignCenter)
    
    def printDataGrid(self):
        start_time = time.time()
        startVisiblePageNumber = self.scrollbar.value()
        start_index = startVisiblePageNumber*512
        stop_index = start_index+512
        row_index_offset = startVisiblePageNumber*32
        printed_data = self.opened_file[start_index:stop_index]
        end_time = time.time()
        elapsed_time_1 = end_time - start_time
        start_time = time.time()
        #Очень медленные функции...
        finalTextData = CreateDataTable(databytes=printed_data,cellBase=self.cellBase,cellBaseLength=self.cellBaseLength,charactersPerCell=self.charactersPerCell,cellsPerRow=self.cellsPerRow,showString=self.showString,textCoding=self.textCoding)
        rowHeader = CreateRowHeader(charactersPerCell=self.charactersPerCell,cellBaseLength=self.cellBaseLength,length=self.length,charactersPerRow=self.charactersPerRow,rowOffset=row_index_offset)
        end_time = time.time()
        elapsed_time_2 = end_time - start_time
        start_time = time.time()
        self.model.set_data(finalTextData)
        self.model.set_vheaders(rowHeader)
        self.table.reset()
        self.table.verticalHeader().reset()
        end_time = time.time()
        elapsed_time_3 = end_time - start_time
        print(elapsed_time_1,elapsed_time_2,elapsed_time_3)
        


    @Slot()
    def wheelEvent(self, WheelEvent):
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        value = self.scrollbar.value()
        direction = 0
        try:
            direction = int(WheelEvent.angleDelta().y())
        except Exception:
            pass #Не колесо мыши
        if(self.scrollbar.isEnabled()):  
            if(direction<0):
                value += 1
            elif(direction>0):
                value -= 1
            self.scrollbar.valueChanged.disconnect(self.wheelEvent)
            if((value>=0) and (value<= self.scrollbar.maximum())):
                if(direction !=0):
                    self.scrollbar.setValue(value)
            self.scrollbar.valueChanged.connect(self.wheelEvent)
        self.printDataGrid()

class MainWindow(QMainWindow):
    def __init__(self, main_widget):
        super().__init__()
        self.setWindowTitle("Тест таблицы")
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    main_widget = StartWindow()
    # QMainWindow using QWidget as central widget
    window = MainWindow(main_widget)
    window.show()
    sys.exit(app.exec_())

