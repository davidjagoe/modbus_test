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
    N_DEC_PLACES = 0
    
    ZERO_AFTER = 4 # seconds

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
        period = 2 * delta # in seconds
        freq = 1.0 / period # in Hz
        rpm = freq * 60.0
        if rpm > 30:
            self._rpm = self._rpm
        else:
            self._rpm = rpm

    def _emit_rpm(self):
        print self._rpm
        self.rpm.emit(round(self._rpm, 0))

    def transmitter_tick(self):
        self._emit_rpm()
        
    def sensor_tick(self):
        switch_state = self._read_sensor()
        if switch_state is not SWITCHING:
            # Do nothing if the sensor is busy switching
            if self._state is None:
                # Initialization - only happens once
                self._t = time.time()
                self._state = switch_state
            elif switch_state != self._state:
                # Change in state
                self._state = switch_state
                self._calculate_rpm()
                # self._emit_rpm()
                # if switch_state is ON:
                #     print "Rising Edge"
                #     print
                #     # On a rising edge, calculate the RPM
                #     self._calculate_rpm()
                #     self._emit_rpm()
                # else:
                #     print "Falling Edge"
            else:
                # No change in state; check for timeout
                t = time.time()
                delta = t - self._t
                if delta > self.ZERO_AFTER:
                    print "ZEROING"
                    self._t = t
                    self._rpm = 0
                    self._emit_rpm()


class FakeTransmitter(QObject):

    rpm = pyqtSignal(int)
    
    def __init__(self):
        QObject.__init__(self)
        self._t = time.time()

    def tick(self):
        t = time.time()
        if t - self._t >= 1:
            self._t = t
            # rpm = random.randint(0, 30)
            rpm = random.normalvariate(15, 5)
            print "RPM: {0}".format(rpm)
            self.rpm.emit(rpm)
