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

    """Simple adaptive Exponentially Weighted Mean Filter.

    It adapts the alpha parameter based on the number of samples read,
    making it very responsive on startup, and then smoother once we
    have lots of samples.

    """

    MIN_SAMPLES = 5
    
    rpm = pyqtSignal(int)

    def __init__(self, transmitter, alpha=0.2, **kwargs):
        QObject.__init__(self)
        self._n_samples = 0
        self._rpm = 0
        self._transmitter = transmitter
        self._alpha = alpha
        self._transmitter.rpm.connect(self._listen)

    def _listen(self, rpm):
        if rpm > 0 and self._n_samples < self.MIN_SAMPLES:
            self._n_samples += 1
            alpha = 1
        else:
            alpha = self._alpha
        
        if rpm == 0:
            self._rpm = 0
        else:
            # For a fixed sample rate the exponentially weighted mean
            # can be calculated with a simple cumulative sum.
            self._rpm = (rpm * alpha) + ((1 - alpha) * self._rpm)
        self.rpm.emit(self._rpm)


class Simple(QObject):

    rpm = pyqtSignal(int)

    def __init__(self, transmitter, n_samples=10, **kwargs):
        QObject.__init__(self)
        self._rpms = [0]
        self._transmitter = transmitter
        self._n = n_samples
        self._transmitter.rpm.connect(self._listen)

    def _emit_rpm(self):
        rpm = float(sum(self._rpms))/len(self._rpms)
        self.rpm.emit(round(rpm, 0))
        
    def _listen(self, rpm):
        if rpm == 0:
            self._rpms = [0]
        else:
            if len(self._rpms) == self._n:
                self._rpms = self._rpms[1:]
            self._rpms.append(rpm)
        self._emit_rpm()
