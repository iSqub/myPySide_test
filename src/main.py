import logging
import sys

from PySide2.QtWidgets import QApplication

from src.MainWindow import MainWindow
from src.StartWindow import StartWindow

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