#!/usr/bin/env python

import time
import minimalmodbus

GATEWAY_ID = 1
D1_NODE_ID = 11
D2_NODE_ID = 12


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


class RPMCalculator(object):

    N_DEC_PLACES = 0
    LIMIT_OFF = 3000 # Approx 4.73 mA
    LIMIT_ON = 30000 # Approx 11.36 mA
    DAMPING_CONSTANT = 2 # seconds
    
    def __init__(self, gateway_device, register_number):
        self._gateway = gateway_device
        self._register = register_number
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
            
    def calculate_rpm(self):
        switch_state = self._read_sensor()
        print switch_state


def _get_register_number(device_id):

    def _get_register_offset(register_name):
        _REGISTER_OFFSETS = {"rpm_sensor": 2,}
        return _REGISTER_OFFSETS[register_name]

    def _get_device_offset(device_id):
        return 16 * device_id

    return _get_device_offset(device_id) + _get_register_offset("rpm_sensor")


def main_loop(calculator):
    while True:
        time.sleep(0.1)
        calculator.calculate_rpm()


def main():
    gateway = minimalmodbus.Instrument("/dev/ttyUSB0", GATEWAY_ID)
    calculator = RPMCalculator(gateway, _get_register_number(D1_NODE_ID))
    main_loop(calculator)
    
        
        
if __name__ == "__main__":
    main()

