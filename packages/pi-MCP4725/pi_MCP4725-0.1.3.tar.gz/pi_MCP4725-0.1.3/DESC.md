A Python module for the Raspberry Pi to interface with the [MCP4725](https://ww1.microchip.com/downloads/en/devicedoc/22039d.pdf) I²C Digital-to-Analogue Converter.

## Compatibility

Tested on Python 3.9 on a Raspberry Pi Zero W v1.1, but should be compatible with most Raspberry Pi models running the latest version of Python.

Module works with Microchip's MCP4725 DAC.

## Pre-requisites

- `smbus2` library

	The MCP4725 module uses the Raspberry Pi's built-in I²C driver to communicate with the chip. This is done on Python using the SMBus protocol. However, due to SMBus incorporating only a subset of I²C features, it is not fully compatible with I²C commands. This is fixed by using `smbus2`, a drop-in replacement of the `smbus` module with extra functionality permitting the extra I²C features. It can be imported as `smbus` to be backward compatible. See below for more details.

	The module must be imported within the main code (it is not imported within the module).
