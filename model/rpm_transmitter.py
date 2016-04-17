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

    LIMIT_OFF = 5000 # Approx 4.73 mA
    LIMIT_ON = 10000 # Approx XXX - with two sensors, this value is lower
    
    ZERO_AFTER = 4 # seconds

    rpm = pyqtSignal(int)
    
    def __init__(self, gateway_device, register_number, n_sensors):
        QObject.__init__(self)
        self._gateway = gateway_device
        self._register = register_number
        self._n_sensors = n_sensors
        self._rpm = 0
        self._state = [None]*self._n_sensors
        self._t = 0

    def _read_sensors(self):
        states = []
        values = self._gateway.read_registers(self._register, self._n_sensors)
        for value in values:
            if value < self.LIMIT_OFF:
                states.append(OFF)
            elif value > self.LIMIT_ON:
                states.append(ON)
            else:
                states.append(SWITCHING)

        return states

    def _calculate_rpm(self):
        t = time.time()
        delta = t - self._t
        self._t = t

        angular_delta = 180.0 / self._n_sensors
        period = (360.0/angular_delta) * delta
        freq = 1.0 / period # in Hz
        rpm = freq * 60.0
        if rpm > 30:
            # Sometimes we get a glitch from the sensor - probably due
            # to getting a low reading between magnets. This results
            # in a very high reading that we simply ignore. TODO:
            # self._t would be wrong in this case!!
            self._rpm = self._rpm
        else:
            self._rpm = rpm

    def _emit_rpm(self):
        self.rpm.emit(round(self._rpm, 0))

    def transmitter_tick(self):
        self._emit_rpm()
        
    def sensor_tick(self):
        switch_states = self._read_sensors()
        if all([switch_state is None for switch_state in self._state]):
            # Initialization - only happens once
            self._t = time.time()
            self._state = switch_states
        elif switch_states != self._state:
            # Change in state
            print "CHANGE"
            self._state = switch_states
            self._calculate_rpm()
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
