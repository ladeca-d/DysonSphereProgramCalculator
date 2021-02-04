from PySide2.QtWidgets import QApplication
import window


def main():
    app = QApplication([])
    screen = app.primaryScreen()
    size = screen.size()
    main_window = window.MainWindow(size.width(), size.height())
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()

