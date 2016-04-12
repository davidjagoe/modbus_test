import time

from PyQt4.QtCore import QObject, pyqtSignal


class NoFilter(QObject):

    rpm = pyqtSignal(int)
    
    def __init__(self, transmitter, **kwargs):
        QObject.__init__(self)
        self._transmitter = transmitter
        self._transmitter.rpm.connect(self._listen)

    def _listen(self, rpm):
        self.rpm.emit(rpm)


class EMAFilter(QObject):

    rpm = pyqtSignal(int)

    def __init__(self, transmitter, alpha=0.8):
        QObject.__init__(self)
        self._rpm = 0
        self._transmitter = transmitter
        self._alpha = alpha
        self._transmitter.rpm.connect(self._listen)

    def _listen(self, rpm):
        self._rpm = (rpm * self._alpha) + ((1 - self._alpha) * self._rpm)
        self.rpm.emit(self._rpm)
