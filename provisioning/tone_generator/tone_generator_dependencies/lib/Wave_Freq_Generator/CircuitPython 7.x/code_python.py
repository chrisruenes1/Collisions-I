#!/usr/bin/env python3

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

OFF = 'OFF'

from display import Display
from generator import Generator
from serial_parser import SerialParser
import shapes

# these names "change_shape" and "change_frequency"
# they're a bit misleading
# but they're left over from the original implementation
# which involved calculating deltas and guard clauses
def change_frequency(frequency):
    return min(20000, max(150, frequency))

def change_shape(shape):
    return (shape + 1) % shapes.NUMBER_OF_SHAPES

if __name__ == '__main__':
    display = Display()
    generator = Generator()
    serial_parser = SerialParser()

    shape = shapes.SINE
    frequency = 440

    display.update_shape(shape)
    display.update_frequency(frequency)

    while True:
        frequency, shape = serial_parser.check_messages()
        if frequency == OFF:
            generator.turn_off()
            display.turn_off()
        else:

            shape = change_shape(shape)
            frequency = change_frequency(frequency)

            display.update_shape(shape)
            display.update_frequency(frequency)
            generator.update(shape, frequency)
