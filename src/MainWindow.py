import logging
import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QApplication, QMenu, QMessageBox

from src.StartWindow import StartWindow


class MainWindow(QMainWindow):

    def __init__(self,main_widget):
        super().__init__()
        self.setWindowTitle("Тест таблицы")
        self.setWindowIcon(QIcon('./img/niime.png'))

        #--------------------------------Меню главного окна-----------------------
        self.menu = self.menuBar()
        #--------------------------------Файл-------------------------------------
        self.file_menu = self.menu.addMenu("Файл")
        #--------------------------------Открыть файл-----------------------------
        select_file_dialog = self.file_menu.addAction("Открыть файл")
        #select_file_dialog.triggered.connect(main_widget.openFile)
        select_file_dialog.setShortcut("Ctrl+A")
        #--------------------------------Обновление прошивки----------------------
        update_firmware_action = self.file_menu.addAction("Обновить прошивку")
        #update_firmware_action.triggered.connect(main_widget.update_firmware)
        update_firmware_action.setShortcut("Ctrl+U")
        #--------------------------------Обновление прошивки----------------------
        #--------------------------------Выход------------------------------------
        exit_action = self.file_menu.addAction("Выход", self.close_application)
        exit_action.setShortcut("Ctrl+Q")
        #--------------------------------Обновление прошивки----------------------
        #--------------------------------Файл-------------------------------------

        #--------------------------------Справка----------------------------------
        self.help_menu = self.menu.addMenu("Справка")
        #--------------------------------О программе------------------------------
        about_action = self.help_menu.addAction("О программе")
        #about_action.triggered.connect(main_widget.aboutProgrammer)
        about_action.setShortcut("F1")
        #--------------------------------О программе------------------------------
        #--------------------------------О прошивке-------------------------------
        about_firmware_action = self.help_menu.addAction("О прошивке")
        #about_firmware_action.triggered.connect(main_widget.aboutFirmware)
        about_firmware_action.setShortcut("F2")
        #--------------------------------О прошивке-------------------------------
        #--------------------------------Обратная связь---------------------------
        callback_action = self.help_menu.addAction("Связь с разработчиком")
        #callback_action.triggered.connect(main_widget.email_callback)
        #--------------------------------Обратная связь---------------------------
        #--------------------------------Справка----------------------------------

        #--------------------------------Контекстное меню на вкладке данных из файла
        self.fileContextMenu = QMenu(self)
        self.fileContextMenu.addAction("Открыть файл")
        #--------------------------------Контекстное меню на вкладке данных из файла

        #--------------------------------Контекстное меню на вкладке данных из микросхемы
        self.memoryContextMenu = QMenu(self)
        self.memoryContextMenu.addAction("Открыть файл")
        self.memoryContextMenu.addAction("Загрузить дамп в буфер программы")
        #--------------------------------Контекстное меню на вкладке данных из микросхемы

        #--------------------------------Контекстное меню на вкладке истории действий
        self.historyContextMenu = QMenu(self)
        self.historyContextMenu.addAction("Очистить историю")
        self.historyContextMenu.addAction("Повторить действие")
        #--------------------------------Контекстное меню на вкладке истории действий

        self.setCentralWidget(main_widget)

    def close_application(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Выход")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы действительно хотите выйти?")
        buttonAceptar  = msg.addButton("Да", QMessageBox.YesRole)    
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole) 
        msg.setDefaultButton(buttonCancelar)
        msg.exec_()        
        if(msg.clickedButton() == buttonAceptar):
            self.close()
        else:
            pass
