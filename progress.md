Setup:

* Using [USB-to-RS232](https://s.click.aliexpress.com/e/_DCOVD2J) adapter. Connected to [HDP1160V4S](https://s.click.aliexpress.com/e/_DCkHtB1) PSU.
* Intel NUC running Proxmox 7.4.

Connecting usb-to-rs232 port to nuc, shows the following 3 devices:

```
/dev/gpiochip0
/dev/serial
/dev/ttyUSB0
```

`lsusb` returns:

```
Bus 001 Device 122: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
```

Look at https://github.com/clayton-r/Hantek-Power-Supply-Controller/blob/master/Utils.py for ideas.

It appears that whether the RS232 port is connected to the PSU or not the lsusb and /dev/ items are still present.

Found [this manual](http://www.hantek.com/uploadpic/hantek/files/20220402/HDP_SCPI_EN.pdf)

Attempting to send commands from the utils.py above or the manual does nothing. Whether the PSU connected or not, commands appear to be sending, but no response is received.

test code: (requires `pyserial` package)

```python
import serial
s = serial.Serial(port='/dev/ttyUSB0',baudrate=9600) #also tried baud rate 2400
s.write('*IDN?'.encode())
s.read(1) # stalls here
# or:
s.write('SYSTem:GET:MODEl?'.encode())
s.read(1) # stalls here
```

Tested the output of RS232 cable with oscilloscope - TX is coming through.
