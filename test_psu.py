from unittest.mock import patch, MagicMock
import pytest
from psu import PSU

FAKE_MODEL_NUMBER = 'HDP1160V4S'

@pytest.fixture
def mocked_serial():
    class MockSerial:
        def __init__(self, *args, **kwargs):
            self.__written = b''
            self.write = MagicMock(side_effect=self._write)
            self.readline = MagicMock(side_effect=self._readline)
        def _write(self, *args, **kwargs):
            self.__written = args[0]
        def _readline(self, *args, **kwargs):
            if self.__written == bytes.fromhex('ff ff 02 20'):
                return FAKE_MODEL_NUMBER.encode()
            if self.__written == bytes.fromhex('ff ff 02 09'):
                return b'330'
            if self.__written == bytes.fromhex('ff ff 02 0a'):
                return b'250'
            if self.__written == bytes.fromhex('ff ff 02 12'):
                return b'500'
            if self.__written == bytes.fromhex('ff ff 02 13'):
                return b'1000'
            if self.__written == bytes.fromhex('ff ff 02 14'):
                return b'1'
            return b''
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    return MockSerial()

@pytest.fixture
def psu(mocked_serial):

    with patch('psu.Serial', return_value=mocked_serial):
        yield PSU()

def test_get_model_number(psu):
    assert psu.get_model() == FAKE_MODEL_NUMBER.encode()

def test_get_active_voltage(psu):
    assert psu.get_active_voltage() == b'330'

def test_get_active_current(psu):
    assert psu.get_active_current() == b'250'

def test_get_voltage_limit(psu):
    assert psu.get_voltage_limit() == b'500'

def test_get_current_limit(psu):
    assert psu.get_current_limit() == b'1000'

def test_get_on_off_status(psu):
    assert psu.get_on_off_status() == b'1'

def test_turn_on(psu, mocked_serial):
    psu.turn_on()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 06 01'))

def test_turn_off(psu, mocked_serial):
    psu.turn_off()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 06 00'))

def test_ocp_on(psu, mocked_serial):
    psu.ocp_on()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 1a 01'))

def test_ocp_off(psu, mocked_serial):
    psu.ocp_off()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 1a 00'))

def test_ovp_on(psu, mocked_serial):
    psu.ovp_on()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 19 01'))

def test_ovp_off(psu, mocked_serial):
    psu.ovp_off()
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 03 19 00'))

def test_set_voltage(psu, mocked_serial):
    psu.set_output_voltage(3.3)
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 04 07 4a 01'))

def test_set_current(psu, mocked_serial):
    psu.set_output_current(100)
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 04 08 64 00'))

def test_set_ovp(psu, mocked_serial):
    psu.set_ovp_limit(15.5)
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 04 17 0e 06'))

def test_set_ocp(psu, mocked_serial):
    psu.set_ocp_limit(250)
    mocked_serial.write.assert_called_with(bytes.fromhex('ff ff 04 18 fa 00'))
