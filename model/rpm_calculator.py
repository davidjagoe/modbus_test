#!/usr/bin/env python

import time

from PyQt4.QtCore import QObject, pyqtSignal


class _OFF(object):
    "OFF STATE"
    def __repr__(self):
        return "OFF"
        
class _ON(object):
    "ON STATE"
    def __repr__(self):
        return "ON"

    
class _SWITCHING(object):
    "SWITCHING STATE"
    def __repr__(self):
        return "SWITCHING"
    

ON = _ON()
OFF = _OFF()
SWITCHING = _SWITCHING()


class RPMCalculator(QObject):

    N_DEC_PLACES = 0
    LIMIT_OFF = 3000 # Approx 4.73 mA
    LIMIT_ON = 30000 # Approx 11.36 mA
    ZERO_CONSTANT = 6 # seconds
    FILTER_LENGTH = 10

    rpm = pyqtSignal(int)
    
    def __init__(self, gateway_device, register_number):
        QObject.__init__(self)
        self._gateway = gateway_device
        self._register = register_number
        self._rpms = [0]
        self._state = None
        self._t = 0

    def _read_sensor(self):
        value = self._gateway.read_register(
            self._register, self.N_DEC_PLACES)
        if value < self.LIMIT_OFF:
            return OFF
        elif value > self.LIMIT_ON:
            return ON
        else:
            return SWITCHING

    def _set_rpm(self):
        t = time.time()
        delta = t - self._t
        self._t = t
        period = delta # in seconds
        freq = 1.0 / period # in Hz
        rpm = freq * 60.0
        if rpm > 30:
            return
        if len(self._rpms) == self.FILTER_LENGTH:
            self._rpms = self._rpms[1:]
        self._rpms.append(rpm)

    def _emit_rpm(self):
        mean = float(sum(self._rpms)) / len(self._rpms)
        self.rpm.emit(round(mean, 0))

    def calculate_rpm(self):
        switch_state = self._read_sensor()
        if switch_state is not SWITCHING:
            if self._state is None:
                self._t = time.time()
                self._state = switch_state
            elif switch_state != self._state:
                if switch_state is ON:
                    self._set_rpm()
                self._state = switch_state
            else:
                t = time.time()
                delta = t - self._t
                if delta > self.ZERO_CONSTANT:
                    self._t = t
                    self._rpms = [0]
        self._emit_rpm()
