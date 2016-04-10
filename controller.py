
import os
import sys

import minimalmodbus

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt

from view.main_window import get_main_window
from model.rpm_calculator import RPMCalculator, FakeRPMCalculator


GATEWAY_ID = 1
D1_NODE_ID = 11
D2_NODE_ID = 12


def _get_register_number(device_id):

    def _get_register_offset(register_name):
        _REGISTER_OFFSETS = {"rpm_sensor": 2,}
        return _REGISTER_OFFSETS[register_name]

    def _get_device_offset(device_id):
        return 16 * device_id

    return _get_device_offset(device_id) + _get_register_offset("rpm_sensor")

        
class Application(qt.QApplication):

    def __init__(self, rpm_calculator, *args):
        qt.QApplication.__init__(self, list(args))
        self.setStyle("Plastique")
        self._rpm_calculator = rpm_calculator
        self._timer = None
        self._setup()

    def _setup_timer(self):
        self._timer = qtc.QTimer()
        self._timer.timeout.connect(self._rpm_calculator.calculate_rpm)
        self._timer.start(100)
        
    def _setup(self):
        self._setup_timer()

    def listen(self, slot):
        self._rpm_calculator.rpm.connect(slot)


def main():

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        calculator = FakeRPMCalculator(None, None)
    else:
        gateway = minimalmodbus.Instrument("/dev/ttyUSB0", GATEWAY_ID)
        calculator = RPMCalculator(gateway, _get_register_number(D1_NODE_ID))

    application = Application(calculator)
    main_window = get_main_window(application)
    main_window.show()
    rc = application.exec_()
    return rc


if __name__ == "__main__":
    main()
