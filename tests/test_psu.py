from unittest.mock import MagicMock
from serial import Serial
from typing import cast
import pytest
from hantekpsu import PSU

FAKE_MODEL_NUMBER = "HDP1160V4S"
FAKE_VOLTAGE = 3.3
FAKE_VOLTAGE_LIMIT = 5.0
FAKE_CURRENT = 250
FAKE_CURRENT_LIMIT = 1200
FAKE_ON_STATUS = True


@pytest.fixture
def fake_serial():
    class FakeSerial:
        def __init__(self, *args, **kwargs):
            self.__written = b""
            self.write = MagicMock(side_effect=self._write)
            self.readline = MagicMock(side_effect=self._readline)

        def _write(self, *args, **kwargs):
            self.__written = args[0]

        def _readline(self, *args, **kwargs):
            if self.__written == bytes.fromhex("ff ff 02 20"):
                return FAKE_MODEL_NUMBER.encode()
            if self.__written == bytes.fromhex("ff ff 02 09"):
                return str(int(FAKE_VOLTAGE * 100)).encode()
            if self.__written == bytes.fromhex("ff ff 02 0a"):
                return str(int(FAKE_CURRENT)).encode()
            if self.__written == bytes.fromhex("ff ff 02 12"):
                return str(int(FAKE_VOLTAGE_LIMIT * 100)).encode()
            if self.__written == bytes.fromhex("ff ff 02 13"):
                return str(int(FAKE_CURRENT_LIMIT)).encode()
            if self.__written == bytes.fromhex("ff ff 02 14"):
                return str(int(FAKE_ON_STATUS)).encode()
            return b""

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    return FakeSerial()


@pytest.fixture
def psu(fake_serial):
    class FakeSerialClass:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return fake_serial

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    yield PSU(serial_class=FakeSerialClass)  # type: ignore


def test_get_model_number(psu):
    assert psu.get_model() == FAKE_MODEL_NUMBER


def test_get_active_voltage(psu):
    assert psu.get_active_voltage() == FAKE_VOLTAGE


def test_get_active_current_in_milliamps(psu):
    assert psu.get_active_current() == FAKE_CURRENT


def test_get_voltage_limit(psu):
    assert psu.get_voltage_limit() == FAKE_VOLTAGE_LIMIT


def test_get_current_limit_in_milliamps(psu):
    assert psu.get_current_limit() == FAKE_CURRENT_LIMIT


def test_get_on_off_status(psu):
    assert psu.get_on_off_status() == FAKE_ON_STATUS


def test_turn_on(psu, fake_serial):
    psu.turn_on()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 06 01"))


def test_turn_off(psu, fake_serial):
    psu.turn_off()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 06 00"))


def test_ocp_on(psu, fake_serial):
    psu.ocp_on()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 1a 01"))


def test_ocp_off(psu, fake_serial):
    psu.ocp_off()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 1a 00"))


def test_ovp_on(psu, fake_serial):
    psu.ovp_on()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 19 01"))


def test_ovp_off(psu, fake_serial):
    psu.ovp_off()
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 03 19 00"))


def test_set_voltage(psu, fake_serial):
    psu.set_output_voltage(3.3)
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 04 07 4a 01"))


def test_set_current(psu, fake_serial):
    psu.set_output_current(100)
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 04 08 64 00"))


def test_set_ovp(psu, fake_serial):
    psu.set_ovp_limit(15.5)
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 04 17 0e 06"))


def test_set_ocp(psu, fake_serial):
    psu.set_ocp_limit(250)
    fake_serial.write.assert_called_with(bytes.fromhex("ff ff 04 18 fa 00"))


@pytest.fixture
def mocked_serial_class():
    mocked_serial = MagicMock(spec=Serial)
    mocked_class = cast(type[Serial], mocked_serial)
    return mocked_class


def test_custom_baudrate_is_set_correctly_on_serial(mocked_serial_class):
    psu = PSU(serial_class=mocked_serial_class, baudrate=115200)
    psu.turn_on()
    assert mocked_serial_class.call_args_list[0].kwargs["baudrate"] == 115200


def test_custom_timeout_is_set_correctly_on_serial(mocked_serial_class):
    psu = PSU(serial_class=mocked_serial_class, timeout=0.9191)
    psu.turn_on()
    assert mocked_serial_class.call_args_list[0].kwargs["timeout"] == 0.9191


def test_custom_port_is_set_correctly_on_serial(mocked_serial_class):
    psu = PSU(serial_class=mocked_serial_class, port="/dev/ttyUSB123")
    psu.turn_on()
    assert mocked_serial_class.call_args_list[0].kwargs["port"] == "/dev/ttyUSB123"
