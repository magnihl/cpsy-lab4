"""Record one ADC reading and one multimeter reading per distance to adc.csv.

Put the book at a distance, type the distance in cm, press enter. Takes N
samples over about a second and keeps the median, then asks for the
multimeter volts. Appends one row with the pass number for that distance.
Blank distance quits.

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

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
adc = MCP3008(spi, digitalio.DigitalInOut(board.D8))


def sample():
    samples = []
    for _ in range(N):
        samples.append(adc.read(0))
        time.sleep(0.05)
    return statistics.median(samples)


# how many rows each distance already has, so passes keep counting
passes = {}
if os.path.exists(FILE):
    with open(FILE, newline="") as f:
        for row in csv.DictReader(f):
            passes[row["cm"]] = passes.get(row["cm"], 0) + 1

new = not os.path.exists(FILE)
with open(FILE, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["cm", "pass", "raw", "volts", "meter"])
    while True:
        cm = input("distance cm (blank to quit): ").strip()
        if not cm:
            break
        raw = sample()
        volts = raw * VREF / 1023
        print(f"  adc {raw:5.0f} raw  {volts:5.3f} V")
        meter = input("  multimeter V: ").strip()
        passes[cm] = passes.get(cm, 0) + 1
        w.writerow([cm, passes[cm], round(raw), round(volts, 3), meter])
        f.flush()
        print(f"  saved pass {passes[cm]} at {cm} cm")
