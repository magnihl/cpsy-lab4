"""Print distance in cm from the IR sensor, once a second.

L = A / (V - B), fitted to adc.csv passes 1, 3, 4 from 20 to 150 cm.
Good to about 100 cm; beyond that the curve is too flat to trust.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python distance.py
Ctrl+C stops it.
"""

import statistics
import time

import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008

A = 48.7
B = 0.068
VREF = 3.3

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
adc = MCP3008(spi, digitalio.DigitalInOut(board.D8))

while True:
    samples = [adc.read(0) for _ in range(10)]
    volts = statistics.median(samples) * VREF / 1023
    if volts > 2.6:
        print(f"{volts:5.3f} V  too close")
    elif volts < 0.3:
        print(f"{volts:5.3f} V  out of range")
    else:
        print(f"{volts:5.3f} V  {A / (volts - B):5.0f} cm")
    time.sleep(1)
