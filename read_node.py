#!/usr/bin/env python

import time
import minimalmodbus

GATEWAY_ID = 1
D1_NODE_ID = 11
D2_NODE_ID = 12


def _get_register_offset(register_name):
    _REGISTER_OFFSETS = {"rpm_sensor": 2,}
    return _REGISTER_OFFSETS[register_name]


def _get_device_offset(device_id):
    return 16 * device_id


def read_rpm_sensor(gateway, node_id):
    register_number = _get_device_offset(node_id) + _get_register_offset("rpm_sensor")
    return gateway.read_register(register_number, 0)


def main_loop():
    gateway = minimalmodbus.Instrument("/dev/ttyUSB0", GATEWAY_ID)
    while True:
        time.sleep(0.1)
        print read_rpm_sensor(gateway, D1_NODE_ID)


if __name__ == "__main__":
    main_loop()

