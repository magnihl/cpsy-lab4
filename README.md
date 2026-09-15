# cpsy-lab4

Distance sensing on a Raspberry Pi Zero: GP2Y0A02YK infrared sensor
read through an MCP3008 ADC on SPI0, channel 0, 3.3 V reference.

Runs on the Pi with the lab 2 environment plus the ADC driver:

    ~/cpsy-display-ip/cpsy/bin/pip install adafruit-circuitpython-mcp3xxx
    ~/cpsy-display-ip/cpsy/bin/python raw.py
    ~/cpsy-display-ip/cpsy/bin/python collect.py

- `raw.py` prints raw value and volts twice a second.
- `collect.py` walks 10 to 150 cm, enter per step, one median ADC reading per step to `adc.csv`.
- `distance.py` prints centimetres from the fitted formula, once a second.
