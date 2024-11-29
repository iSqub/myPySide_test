import logging
import sys

from PySide2.QtCore import QModelIndex, Qt, Slot, QSize, QTimer, QEvent
from PySide2.QtGui import QFont, QColor, QIcon
from PySide2.QtWidgets import QLabel, QPushButton, QSpinBox, QComboBox, QCheckBox, QRadioButton, QTabWidget, QScrollBar,QProgressBar, QMainWindow, QTableView, QApplication, QMenu, QMessageBox, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QStatusBar

from src.FileTableModel import FileTableModel
from src.MemoryTableModel import MemoryTableModel
from src.ErrorsTableModel import ErrorsTableModel
from src.ContactTableModel import ContactTableModel
from src.HistoryTableModel import HistoryTableModel

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_path = '/'.join(sys.executable.replace('\\', '/').split('/')[:-1])#Определяем место положение фала .exe

        self.color_ok = QColor(0,255,0,255)     #Green
        self.ccolor_fail = QColor(255,0,0,255)   #Red
        self.column_count = 16  #количество столбцов на экране отображения данных
        self.textCoding = ['cp1251','utf-8','ascii']#Варианты кодировок отображения текстовой информации
        comboBoxSizePolicy_h = QSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Minimum,QSizePolicy.ControlType.ComboBox)
        comboBoxSizePolicy_h.setHorizontalStretch(85)
        labelSizePolicy_l = QSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Minimum,QSizePolicy.ControlType.Label)
        labelSizePolicy_l.setHorizontalStretch(15)
        pushButtonSizePolicy_l = QSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Minimum,QSizePolicy.ControlType.PushButton)
        pushButtonSizePolicy_l.setHorizontalStretch(0)

        #--------------------------------COM-потр-------------------------------
        self.com_ports_lable = QLabel("Порт:")
        self.com_ports_lable.setSizePolicy(labelSizePolicy_l)
        self.com_ports_combobox = QComboBox()
        self.com_ports_combobox.setSizePolicy(comboBoxSizePolicy_h)
        #self.programmer_com_ports_combobox.addItems(self.programmer.MC_name)
        self.com_ports_combobox.setDisabled(True)
        self.com_ports_combobox.setToolTip("Выберети COM-порт для подключения к программатору")

        self.com_ports_layout = QHBoxLayout()
        self.com_ports_layout.addWidget(self.com_ports_lable)
        self.com_ports_layout.addWidget(self.com_ports_combobox)
        #--------------------------------COM-потр-------------------------------

        #--------------------------------Микросхема-----------------------------
        self.IC_lable = QLabel("ИМС:")
        self.IC_lable.setSizePolicy(labelSizePolicy_l)
        self.IC_combobox = QComboBox()
        self.IC_combobox.setSizePolicy(comboBoxSizePolicy_h)
        #self.programmer_IC_combobox.addItems(self.programmer.supported_IC_names)
        self.IC_combobox.setCurrentIndex(0)
        self.IC_combobox.setDisabled(True)
        self.IC_combobox.setToolTip("Выбор поддерживаемой программатором микросхемы")
        #self.programmer_IC_combobox.textActivated.connect(self.selectIC)

        self.IC_layout = QHBoxLayout()
        self.IC_layout.addWidget(self.IC_lable)
        self.IC_layout.addWidget(self.IC_combobox)
        #--------------------------------Микросхема-----------------------------
        
        #--------------------------------Режимы---------------------------------
        self.commands_lable = QLabel("Режим:")
        self.commands_lable.setSizePolicy(labelSizePolicy_l)
        self.commands_combobox = QComboBox()
        #self.programmer_commands_combobox.textActivated.connect(self.selectMode)
        self.commands_combobox.setSizePolicy(comboBoxSizePolicy_h)
        #self.programmer_commands_combobox.addItems(self.programmer.supported_commands_name)
        self.commands_combobox.setDisabled(True)
        self.commands_combobox.setToolTip("Выбор поддерживаемого микросхемой режама работы")
        self.commands_layout = QHBoxLayout()
        self.commands_layout.addWidget(self.commands_lable)
        self.commands_layout.addWidget(self.commands_combobox)
        #--------------------------------Режимы---------------------------------

        #--------------------------------COM-потр+Микросхема+Режимы-------------
        self.commands_vertical_layout = QVBoxLayout()
        self.commands_vertical_layout.addLayout(self.com_ports_layout)
        self.commands_vertical_layout.addLayout(self.IC_layout)
        self.commands_vertical_layout.addLayout(self.commands_layout)
        self.commands_vertical_layout.addStretch(1)
        #--------------------------------COM-потр+Микросхема+Режимы-------------
    
        #--------------------------------Подключение+запуск---------------------
        self.connect_pushbutton = QPushButton("Подключить программатор") 
        self.connect_pushbutton.setToolTip("Подключение/отключение программатора")
        #self.programmer_connect_pushbutton.clicked.connect(self.programmerConnection)
        self.action_pushbutton = QPushButton("Запуск") 
        self.action_pushbutton.setEnabled(False)
        self.action_pushbutton.setToolTip("Кнопка запуска или прерывания для выбранного режима работы")
        #self.programmer_action_pushbutton.clicked.connect(self.programmerAction)

        self.connetc_action_layout = QHBoxLayout()
        self.connetc_action_layout.addWidget(self.connect_pushbutton)
        self.connetc_action_layout.addWidget( self.action_pushbutton)
        #--------------------------------Подключение+запуск---------------------

        #--------------------------------Адрес----------------------------------
        self.adress_lable = QLabel("Адрес в микросхеме:")
        self.adress_spin_box = QSpinBox()
        self.adress_spin_box.setPrefix("0x")
        self.adress_spin_box.setDisplayIntegerBase(16)
        self.adress_spin_box.setRange(0x0,0x3FFFFF)
        self.adress_spin_box.setSingleStep(128)
        self.adress_spin_box.setValue(0)
        self.adress_spin_box.setToolTip("Смещение в адресном пространстве микросхемы памяти")

        self.adress_layout = QHBoxLayout()
        self.adress_layout.addWidget(self.adress_lable)
        self.adress_layout.addWidget(self.adress_spin_box)
        #--------------------------------Адрес----------------------------------

        #--------------------------------Страницы-------------------------------
        self.page_count_lable = QLabel("Количество страниц:")
        self.page_count_spin_box = QSpinBox()
        self.page_count_spin_box.setRange(1,32768)#Максимум на 32Мбит
        self.page_count_spin_box.setSingleStep(1)
        self.page_count_spin_box.setValue(1)
        self.page_count_spin_box.setToolTip("Количество страниц микросхемы памяти, которые будут изменены")

        self.page_count_layout = QHBoxLayout()
        self.page_count_layout.addWidget(self.page_count_lable)
        self.page_count_layout.addWidget(self.page_count_spin_box)
        #--------------------------------Страницы-------------------------------

        #--------------------------------Адрес+Страницы-------------------------
        self.action_vertical_layout = QVBoxLayout()
        self.action_vertical_layout.addLayout(self.connetc_action_layout)
        self.action_vertical_layout.addLayout(self.adress_layout)
        self.action_vertical_layout.addLayout(self.page_count_layout)
        self.action_vertical_layout.addStretch(1)
        #--------------------------------Адрес+Страницы-------------------------
        
        #--------------------------------Подключение+запуск+Адрес+Страницы------
        self.settings_layout = QHBoxLayout()
        self.settings_layout.addLayout(self.commands_vertical_layout)
        self.settings_layout.addLayout(self.action_vertical_layout)
        #--------------------------------Подключение+запуск+Адрес+Страницы------

        # Fill example data
        font = QFont()
        font.setFamily("Liberation Mono")
        font.setPointSize(8)
        #--------------------------------Данные из файла------------------------
        self.dataFromFileViewerWidget = QTableView(self)
        self.dataFromFileViewerWidget.setFont(font)
        self.dataFromFileViewerWidget.horizontalHeader().setFont(font)
        self.dataFromFileViewerWidget.verticalHeader().setFont(font)
        model = FileTableModel([], self.column_count)
        self.dataFromFileViewerWidget.setModel(model)
        self.dataFromFileViewerWidget.horizontalHeader().setStretchLastSection(True)

        for column in range(model.columnCount(QModelIndex())):
            if column != model.text_column_idx:
                self.dataFromFileViewerWidget.setColumnWidth(column, 20)

        #--------------------------------Данные из файла------------------------

        #--------------------------------Данные из микросхемы-------------------
        self.dataFromMemoryViewerWidget = QTableView(self)
        self.dataFromMemoryViewerWidget.setFont(font)
        self.dataFromMemoryViewerWidget.horizontalHeader().setFont(font)
        self.dataFromMemoryViewerWidget.verticalHeader().setFont(font)
        model = MemoryTableModel([], self.column_count)
        self.dataFromMemoryViewerWidget.setModel(model)
        self.dataFromMemoryViewerWidget.horizontalHeader().setStretchLastSection(True)

        for column in range(model.columnCount(QModelIndex())):
            if column != model.text_column_idx:
                self.dataFromMemoryViewerWidget.setColumnWidth(column, 20)
        #--------------------------------Данные из микросхемы-------------------

        #--------------------------------Список ошибок--------------------------
        self.dataFromErrorsViewerWidget = QTableView(self)
        self.dataFromErrorsViewerWidget.setFont(font)
        self.dataFromErrorsViewerWidget.horizontalHeader().setFont(font)
        self.dataFromErrorsViewerWidget.verticalHeader().setFont(font)
        example_data = [[0,1,1,0,100],[0,1,1,0,200],[0,1,1,0,500]]
        model = ErrorsTableModel(example_data)
        self.dataFromErrorsViewerWidget.setModel(model)
        self.dataFromErrorsViewerWidget.horizontalHeader().setStretchLastSection(True)
        #--------------------------------Список ошибок--------------------------
        
        #--------------------------------Статус контактирования-----------------
        self.dataFromContactViewerWidget = QTableView(self)
        self.dataFromContactViewerWidget.setFont(font)
        self.dataFromContactViewerWidget.horizontalHeader().setFont(font)
        self.dataFromContactViewerWidget.verticalHeader().setFont(font)
        example_data = [['A0','1','Годен'],['A1','2','Годен'],['A3','2','Брак']]
        model = ContactTableModel(example_data)
        self.dataFromContactViewerWidget.setModel(model)
        self.dataFromContactViewerWidget.horizontalHeader().setStretchLastSection(True)
        #--------------------------------Статус контактирования-----------------

       #--------------------------------История действий------------------------
        self.historyDataViewerWidget = QTableView(self)
        self.historyDataViewerWidget.setFont(font)
        self.historyDataViewerWidget.horizontalHeader().setFont(font)
        self.historyDataViewerWidget.verticalHeader().setFont(font)
        example_data = [['29.11.2024, 12:00:10','1661РР065','Проверка контактирования','-','-','-','29.11.2024, 12:00:16','Брак'],['29.11.2024, 12:00:10','1661РР065','Чтение в режиме SPI (0x0B)','0','1','MainWindow.py','29.11.2024, 12:15:10','Годен']]
        model = HistoryTableModel(example_data)
        self.historyDataViewerWidget.setModel(model)
        self.historyDataViewerWidget.horizontalHeader().setStretchLastSection(True)
        #--------------------------------История действий------------------------

        #--------------------------------Настройки отображения данных------------
        self.dataFromFileViewerSettingsGroupBox = QGroupBox("Настройки отображения данных из файла")
        self.dataViewerSettingsLable = QLabel("Количество столбцов:")
        #self.dataViewerSettingsLable.setSizePolicy(labelSizePolicy_l)
        self.dataViewerSettingSpinBox = QSpinBox()
        self.dataViewerSettingSpinBox.setValue(self.column_count)
        self.dataViewerSettingSpinBox.setRange(1,128)
        self.dataViewerSettingSpinBox.setSingleStep(1)
        self.dataViewerSettinHBoxLayout = QHBoxLayout()
        self.dataViewerSettinHBoxLayout.addWidget(self.dataViewerSettingsLable)
        self.dataViewerSettinHBoxLayout.addWidget(self.dataViewerSettingSpinBox)
        self.dataViewerSettinHBoxLayout.addStretch(1)
        self.dataViewerSettingCheckBox = QCheckBox("Отображать текстовое представление")
        self.dataViewerSettingCheckBox.setChecked(True)
        self.dataFromFileViewerSettingHex = QRadioButton("Отображение в hex формате")
        self.dataFromFileViewerSettingHex.setChecked(True)
        self.dataFromFileViewerSettingHex.setToolTip("Отображение данных в формате hex")
        self.dataFromFileViewerSettingBin = QRadioButton("Отображение в bin формате")
        self.dataFromFileViewerSettingBin.setToolTip("Отображение данных в формате bin")
        #self.dataFromFileViewerSettingHex.toggled.connect(self.viewerSettingsEvent)

        self.dataFromFileViewerSettingsVerticalalLayout = QVBoxLayout(self.dataFromFileViewerSettingsGroupBox)
        self.dataFromFileViewerSettingsVerticalalLayout.addLayout(self.dataViewerSettinHBoxLayout)
        self.dataFromFileViewerSettingsVerticalalLayout.addWidget(self.dataFromFileViewerSettingHex)
        self.dataFromFileViewerSettingsVerticalalLayout.addWidget(self.dataFromFileViewerSettingBin)
        self.dataFromFileViewerSettingsVerticalalLayout.addStretch(1)
        #--------------------------------Настройки отображения данных-------------

        #--------------------------------Настройки данных микросхемы--------------
        self.dataFromMemoryViewerSettingsGroupBox = QGroupBox("Настройки данных микросхемы")
        self.dataFromMemorySave = QPushButton("Сохранить данные в файл")
        self.dataFromMemorySave.setToolTip("Сохранить в файл данные, прочитанные из памяти")
        #self.dataFromMemorySave.clicked.connect(self.saveDumpFile)
        self.dataFromMemoryLoad = QPushButton("Загрузить дамп в буфер программы")
        self.dataFromMemoryLoad.setToolTip("Загрузить данные из файла в буфер программы, данные будут восприняты как прочитанные из памяти")
        #self.dataFromMemoryLoad.clicked.connect(self.loadDumpFile)
        
        self.dataFromMemoryViewerSettingsVerticalalLayout = QVBoxLayout(self.dataFromMemoryViewerSettingsGroupBox)
        self.dataFromMemoryViewerSettingsVerticalalLayout.addWidget(self.dataFromMemorySave)
        self.dataFromMemoryViewerSettingsVerticalalLayout.addWidget(self.dataFromMemoryLoad)
        self.dataFromMemoryViewerSettingsVerticalalLayout.addStretch(1)
        #--------------------------------Настройки данных микросхемы-------------

        #--------------------------------Настройки отображения ошибок------------
        self.dataFromErrorsViewerSettingsGroupBox = QGroupBox("Настройки поиска ошибок")
        self.dataFromErrorsViewerSettingFirst = QRadioButton("Проверка до первой ошибки")
        self.dataFromErrorsViewerSettingFirst.setToolTip("Остановка выполнения операции при достижении первой ошибки")
        self.dataFromErrorsViewerSettingFirst.setDisabled(True)
        #self.dataFromErrorsViewerSettingFirst.setChecked(True)
        #self.dataFromErrorsViewerSettingFirst.toggled.connect(self.errorDataRefresh)
        self.dataFromErrorsViewerSettingAll = QRadioButton("Найти все ошибки")
        self.dataFromErrorsViewerSettingAll.setToolTip("После окончания операции, происходит подсчёт всех ошибок")
        self.dataFromErrorsViewerSettingAll.setChecked(True)
        self.dataFromErrorsSave = QPushButton("Сохранить данные в файл")
        self.dataFromErrorsSave.setToolTip("Сохранение ошибок в файл")
        #self.dataFromErrorsSave.clicked.connect(self.saveErrorFile)

        self.dataFromErrorsViewerSettingsVerticalalLayout = QVBoxLayout(self.dataFromErrorsViewerSettingsGroupBox)
        self.dataFromErrorsViewerSettingsVerticalalLayout.addWidget(self.dataFromErrorsViewerSettingFirst)
        self.dataFromErrorsViewerSettingsVerticalalLayout.addWidget(self.dataFromErrorsViewerSettingAll)
        self.dataFromErrorsViewerSettingsVerticalalLayout.addWidget(self.dataFromErrorsSave)
        #self.dataFromErrorsViewerSettingsVerticalalLayout.addStretch(1)
        #--------------------------------Настройки отображения ошибок------------

        #--------------------------------Настройки режимов работы----------------
        self.allSettingsGroupBox = QGroupBox("Настройки режимов работы")
        self.autoSettingsCheckBox = QCheckBox("Автоматические настройки режимов")
        self.autoSettingsCheckBox.setChecked(True)
        self.contactSettingsCheckBox = QCheckBox("Проверять контактирование перед запуском")
        self.contactSettingsCheckBox.setChecked(False)
        self.fileLogsCheckBox = QCheckBox("Запись журнала событий в файл")
        self.fileLogsCheckBox.setChecked(True)
        #self.fileLogsCheckBox.stateChanged.connect(self.redirectionSTD)
        self.fileLogsCheckBox.setToolTip("Вкл./Выкл. запись последовательности событий в файл Журнал.txt в папке log")
        self.textCoding_lable = QLabel("Кодировка:")
        self.textCoding_combobox = QComboBox()
        self.textCoding_combobox.addItems(self.textCoding)
        #self.textCoding_combobox.textActivated.connect(self.selectMode)
        self.textCoding_combobox.setToolTip("Кодировка символов поля текст вкладок данные из файла и микросхемы")

        self.textCoding_combobox_layout = QHBoxLayout()
        self.textCoding_combobox_layout.addWidget(self.textCoding_lable)
        self.textCoding_combobox_layout.addWidget(self.textCoding_combobox)
        self.textCoding_combobox_layout.addStretch(1)

        self.allSettingsVerticalalLayout = QVBoxLayout(self.allSettingsGroupBox)
        self.allSettingsVerticalalLayout.addWidget(self.autoSettingsCheckBox)
        self.allSettingsVerticalalLayout.addWidget(self.contactSettingsCheckBox)
        self.allSettingsVerticalalLayout.addWidget(self.fileLogsCheckBox)
        self.allSettingsVerticalalLayout.addLayout(self.textCoding_combobox_layout)
        self.allSettingsVerticalalLayout.addStretch(1)
        #--------------------------------Настройки режимов работы----------------

        #--------------------------------Все настройки отображения---------------
        self.viewerSettingsGroupBoxVerticalLayout = QVBoxLayout()
        self.viewerSettingsGroupBoxVerticalLayout.addWidget(self.dataFromFileViewerSettingsGroupBox)
        self.viewerSettingsGroupBoxVerticalLayout.addWidget(self.dataFromMemoryViewerSettingsGroupBox)
        self.viewerSettingsGroupBoxVerticalLayout.addWidget(self.dataFromErrorsViewerSettingsGroupBox)
        #--------------------------------Все настройки отображения----------------

        #--------------------------------Все возможные настройки------------------
        self.settingsWidget = QWidget()
        self.settingsLayout = QGridLayout(self.settingsWidget)
        self.settingsLayout.addLayout(self.viewerSettingsGroupBoxVerticalLayout,0,1)
        self.settingsLayout.addWidget(self.allSettingsGroupBox,0,0)
        self.dataViewerTableWidget = QTabWidget()
        self.dataViewerTableWidget.setToolTip("Выбор источника данных и настроек отображения")
        self.dataViewerTableWidget.addTab(self.dataFromFileViewerWidget,"Данные из файла")
        self.dataViewerTableWidget.addTab(self.dataFromMemoryViewerWidget,"Данные из микросхемы")
        self.dataViewerTableWidget.addTab(self.dataFromErrorsViewerWidget, "Ошибки")
        self.dataViewerTableWidget.addTab(self.dataFromContactViewerWidget, "Контактирование")
        self.dataViewerTableWidget.addTab(self.historyDataViewerWidget, "История")
        self.dataViewerTableWidget.addTab(self.settingsWidget, "Настройки")
        #self.dataViewerTableWidget.currentChanged.connect(self.printDataGrid)
        verticalSizePolicy_H = QSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Minimum,QSizePolicy.ControlType.Label)
        verticalSizePolicy_H.setVerticalStretch(15)
        self.dataViewerTableWidget.setSizePolicy(verticalSizePolicy_H)
        #--------------------------------Все возможные настройки------------------

        #--------------------------------Статус и прогресс------------------------
        self.status_bar = QStatusBar()
        self.progressBar = QProgressBar()
        #self.progressBar.setValue(50)
        self.status_bar.addPermanentWidget(self.progressBar)
        #--------------------------------Статус и прогресс------------------------
        
        #--------------------------------Финальная сборка-------------------------
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.settings_layout)
        self.layout.addWidget(self.dataViewerTableWidget)
        self.layout.addWidget(self.status_bar)
        #--------------------------------Финальная сборка-------------------------

        self.statusBarTimer = QTimer(self)



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

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    # Qt Application
    app = QApplication(sys.argv)
    main_widget = StartWindow()
    # QMainWindow using QWidget as central widget
    window = MainWindow(main_widget)
    window.setMinimumSize(800, 600)
    window.show()
    sys.exit(app.exec_())