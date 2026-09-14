"""Print the MCP3008 reading of the IR sensor on CH0, no calculation.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python raw.py
Ctrl+C stops it.
"""

import time

import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008

VREF = 3.3

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
adc = MCP3008(spi, digitalio.DigitalInOut(board.D8))

while True:
    raw = adc.read(0)
    print(f"raw {raw:4d}   volts {raw * VREF / 1023:5.3f}")
    time.sleep(0.5)
