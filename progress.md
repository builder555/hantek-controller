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

It appears that whether the RS232 port is connected to the psu or not the lsusb and /dev/ items are still present.
