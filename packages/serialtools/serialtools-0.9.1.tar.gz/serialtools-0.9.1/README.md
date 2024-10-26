Tools to work with a serial bus.

This project aims to become for the serial bus what [cantools](https://cantools.readthedocs.io/en/latest/) is for the CAN bus.

In contrast to other tools for a serial bus like
[hterm](https://www.der-hammer.info/pages/terminal.html) or
[pyserial-miniterm](https://pythonhosted.org/pyserial/tools.html#module-serial.tools.miniterm)
this project aims to also decode and encode messages and also provide an API.



# Debugging

## Inappropriate ioctl for device
Do you have the correct permissions to access the serial bus?
If you are not part of the tty group run
```bash
# usermod -aG tty <username>
# reboot
```
