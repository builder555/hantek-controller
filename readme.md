![test-and-lint](https://github.com/builder555/hantek-controller/actions/workflows/ci.yml/badge.svg)

# Hantek Power Supply Controller

<img src="https://github.com/builder555/hantek-controller/blob/master/psu.jpg?raw=true" align="right" style="float:right; height: 200px">

This is an interface to the serial port on [Hantek HDP1160V4S](http://www.hantek.com/products/detail/18193) power supply. It should work with other HDP10000-series power supplies. [buy](https://s.click.aliexpress.com/e/_DCkHtB1)


### ❗**ATTENTION**❗
<mark>
USING THIS CODE MAY DAMAGE YOUR POWER SUPPLY OR CONNECTED DEVICES. USE AT YOUR OWN RISK.
</mark>

###

To communicate with the PSU I am using [USB-to-RS232](https://s.click.aliexpress.com/e/_DCOVD2J) adapter - does not require any drivers on debian linux.

<br clear="both"/>

## Installation

`pip install hantekpsu`

## Usage

```python
from hantekpsu import PSU
p = PSU(port='/dev/ttyUSB0', baudrate=2400)
```

## Methods
| Method | Description | Return Type |
| ------ | ----------- | ----------- |
| `turn_on()` | Turns on the power supply unit. | None |
| `turn_off()` | Turns off the power supply unit. | None |
| `ocp_on()` | Enables Over Current Protection (OCP). | None |
| `ocp_off()` | Disables Over Current Protection (OCP). | None |
| `ovp_on()` | Enables Over Voltage Protection (OVP). | None |
| `ovp_off()` | Disables Over Voltage Protection (OVP). | None |
| `get_model()` | Gets the model of the PSU. | `str` |
| `get_active_voltage()` | Gets the active output voltage of the PSU in volts. | `float` |
| `get_active_current()` | Gets the active output current of the PSU in milliamps. | `int` |
| `get_voltage_limit()` | Gets the voltage limit setting of the PSU in volts. | `float` |
| `get_current_limit()` | Gets the current limit setting of the PSU in milliamps. | `int` |
| `get_on_off_status()` | Returns the on/off status of the PSU. | `bool` |
| `set_output_voltage(v: float)` | Sets the output voltage of the PSU in volts. | None |
| `set_output_current(mA: int)` | Sets the output current of the PSU in milliamps. | None |
| `set_ovp_limit(v: float)` | Sets the Over Voltage Protection (OVP) limit in volts. | None |
| `set_ocp_limit(mA: int)` | Sets the Over Current Protection (OCP) limit in milliamps. | None |

## Examples

Set voltage to 12V and turn on the power supply:

```python
>>> from hantekpsu import PSU
>>> p = PSU()
>>> p.set_output_voltage(12.0)
>>> p.turn_on()
```

## Development

### Requirements

* python 3.10+
* poetry

Ensure the device is connected. If using usb-to-rs232 adapter, run `lsusb`:

```bash
$ lsusb
Bus 001 Device 012: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
```

You should also see something similar to `/dev/ttyUSB0` in the `/dev` folder.

To figure out which device it is, you can run  `ls /dev` before plugging in the adapter and after and compare the differences.

### Installation

```bash
git clone https://github.com/builder555/hantek-controller
cd hantek-controller
poetry config virtualenvs.in-project true --local
poetry install
```

### Unit Tests

When adding new features or modifying existing ones, make sure you add unit tests and run them:

```bash
$ poetry run pytest -v

test_psu.py::test_get_model_number PASSED                       [  6%]
test_psu.py::test_get_active_voltage PASSED                     [ 12%]
test_psu.py::test_get_active_current_in_milliamps PASSED        [ 18%]
test_psu.py::test_get_voltage_limit PASSED                      [ 25%]
test_psu.py::test_get_current_limit_in_milliamps PASSED         [ 31%]
test_psu.py::test_get_on_off_status PASSED                      [ 37%]
test_psu.py::test_turn_on PASSED                                [ 43%]
test_psu.py::test_turn_off PASSED                               [ 50%]
test_psu.py::test_ocp_on PASSED                                 [ 56%]
test_psu.py::test_ocp_off PASSED                                [ 62%]
test_psu.py::test_ovp_on PASSED                                 [ 68%]
test_psu.py::test_ovp_off PASSED                                [ 75%]
test_psu.py::test_set_voltage PASSED                            [ 81%]
test_psu.py::test_set_current PASSED                            [ 87%]
test_psu.py::test_set_ovp PASSED                                [ 93%]
test_psu.py::test_set_ocp PASSED                                [100%]

========================= 16 passed in 0.03s =========================
```

You can also run pytest-watch while developing to run tests automatically on save:

```bash
poetry run ptw --runner 'pytest -v'
```
