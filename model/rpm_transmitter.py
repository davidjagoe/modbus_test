#!/usr/bin/env python

import random
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


class RPMTransmitter(QObject):

    LIMIT_OFF = 3000 # Approx 4.73 mA
    LIMIT_ON = 30000 # Approx 11.36 mA

    ZERO_AFTER = 6 # seconds

    rpm = pyqtSignal(int)
    
    def __init__(self, gateway_device, register_number):
        QObject.__init__(self)
        self._gateway = gateway_device
        self._register = register_number
        self._rpm = 0
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

    def _calculate_rpm(self):
        t = time.time()
        delta = t - self._t
        self._t = t
        period = delta # in seconds
        freq = 1.0 / period # in Hz
        rpm = freq * 60.0
        if rpm > 30:
            self._rpm = self._rpm
        else:
            self._rpm = rpm

    def tick(self):
        switch_state = self._read_sensor()
        if switch_state is not SWITCHING:
            if self._state is None:
                self._t = time.time()
                self._state = switch_state
            elif switch_state != self._state:
                self._state = switch_state
                if switch_state is ON:
                    self._calculate_rpm()
            else:
                t = time.time()
                delta = t - self._t
                if delta > self.ZERO_AFTER:
                    self._t = t
                    self._rpm = 0
        self.rpm.emit(round(self._rpm, 0))


class FakeTransmitter(QObject):

    rpm = pyqtSignal(int)
    
    def __init__(self):
        QObject.__init__(self)
        self._t = time.time()

    def tick(self):
        t = time.time()
        if t - self._t >= 1:
            self._t = t
            rpm = random.randint(0, 30)
            print "RPM: {0}".format(rpm)
            self.rpm.emit(rpm)
