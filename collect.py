"""Walk the distance grid and record one ADC reading per step to adc.csv.

It asks for 10, 20, ... 150 cm in turn. Put the book there, press enter,
it takes N samples over about a second and saves the median. After 150 it
starts the next pass. Type q and enter to quit.

Run on the Pi:  ~/cpsy-display-ip/cpsy/bin/python collect.py
"""

import csv
import os
import statistics
import time

import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008

N = 20
VREF = 3.3
FILE = "adc.csv"
GRID = range(10, 160, 10)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
adc = MCP3008(spi, digitalio.DigitalInOut(board.D8))


def sample():
    samples = []
    for _ in range(N):
        samples.append(adc.read(0))
        time.sleep(0.05)
    return statistics.median(samples)


# continue the pass count from what is already in the file
done = 0
if os.path.exists(FILE):
    with open(FILE, newline="") as f:
        done = sum(1 for _ in csv.DictReader(f))
pass_no = done // len(GRID) + 1

new = not os.path.exists(FILE)
with open(FILE, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["cm", "pass", "raw", "volts"])
    while True:
        for cm in GRID:
            if input(f"pass {pass_no}, book at {cm} cm, enter: ").strip() == "q":
                raise SystemExit
            raw = sample()
            volts = raw * VREF / 1023
            w.writerow([cm, pass_no, round(raw), round(volts, 3)])
            f.flush()
            print(f"  {raw:5.0f} raw  {volts:5.3f} V")
        pass_no += 1
