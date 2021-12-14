# SPDX-FileCopyrightText: 2018 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Main signal generator code.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

# use for basic test of usb communication
# import board
# import digitalio

# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT
# (if bytes availablel or whatever):
# led.value = True
# time.sleep(3.0)
# led.value = False

# from display import Display
from generator import Generator
from time import sleep
import shapes
import supervisor
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def process_freq(frequency):
    return min(20000, max(10, frequency))

def process_shape(shape):
    return (shape + 1) % shapes.NUMBER_OF_SHAPES

def parse_in_text(in_text):
    str_arr = in_text.split(',')
    return [float(str) for str in str_arr]

def run():
    # display = Display()
    generator = Generator()

    shape = shapes.SINE                          # the active waveform
    frequency = 440                       # the current frequency

    # display.update_shape(shape)           # initialize the display contents
    # display.update_frequency(frequency)

    while True:
        # Check to see if there's input available (requires CP 4.0 Alpha)
        if supervisor.runtime.serial_bytes_available:
            inText = input().strip()
            # Sometimes Windows sends an extra (or missing) newline - ignore them
            if inText == "":
                continue
            elif inText == "stop":
                generator.stop()
                # display.stop() don't know how to stop it effectively lol
            else:
                next_freq, next_shape = parse_in_text(inText)
                frequency = process_freq(next_freq)
                shape = process_shape(next_shape)

                # display.update_shape(shape)
                # display.update_frequency(frequency)
                generator.update(shape, frequency)

run()
