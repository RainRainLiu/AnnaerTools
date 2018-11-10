import sys
from src.gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    # Create main app
    myApp = QApplication(sys.argv)
    myApp.setQuitOnLastWindowClosed(True)
    try:
        sys.argv.index("--debug")
    except ValueError:
        pass
    ex2 = MainWindow()
    ex2.show()
    # Execute the Application and Exit
    sys.exit(myApp.exec_())