
import os
import sys

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt
import PyQt4.uic as uic

from view.main_window import get_main_window


class Application(qt.QApplication):

    def __init__(self, *args):
        qt.QApplication.__init__(self, list(args))
        self.setStyle("Plastique")


def main():
    application = Application()
    main_window = get_main_window()
    main_window.show()
    rc = application.exec_()
    return rc


if __name__ == "__main__":
    main()
