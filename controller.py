
import click
import os
import sys

import minimalmodbus

import PyQt4.QtCore as qtc
import PyQt4.QtGui as qt

from view.main_window import get_main_window
from model.rpm_transmitter import RPMTransmitter, FakeTransmitter
from model.filters import EMAFilter, NoFilter


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

    def __init__(self, rpm_transmitter, rpm_emitter, *args):
        qt.QApplication.__init__(self, list(args))
        self.setStyle("Plastique")
        self._transmitter = rpm_transmitter
        self._emitter = rpm_emitter
        self._timer = None
        self._setup()

    def _setup_timer(self):
        self._timer = qtc.QTimer()
        self._timer.timeout.connect(self._transmitter.tick)
        self._timer.start(100)
        
    def _setup(self):
        self._setup_timer()

    def listen(self, slot):
        self._emitter.rpm.connect(slot)


def _get_filter_class(filter_name):
    filters = {
        "no-filter": NoFilter,
        "ema": EMAFilter,
    }
    return filters[filter_name]


@click.command()
@click.option("--test", default=False, help="Runs the code with fake transmitter instead of the Banner Wireless transmitter")
@click.option("--filter_name", default="no-filter", help="Specifies the time-domain filter to use. Options are 'no-filter' and 'ema'")
@click.option("--ema_alpha", default=0.8, help="Specifies the alpha parameter of the EMA filter")
def main(test, filter_name, ema_alpha):

    if test:
        transmitter = FakeTransmitter()
    else:
        gateway = minimalmodbus.Instrument("/dev/ttyUSB0", GATEWAY_ID)
        transmitter = RPMTransmitter(gateway, _get_register_number(D1_NODE_ID))

    Constructor = _get_filter_class(filter_name)
    
    filter_ = Constructor(transmitter, alpha=ema_alpha)
    
    application = Application(transmitter, filter_)
    main_window = get_main_window(application)
    main_window.show()
    rc = application.exec_()
    return rc


if __name__ == "__main__":
    main()
