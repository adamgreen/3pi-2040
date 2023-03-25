###############################################################################
#  Copyright (C) 2023  Adam Green (https://github.com/adamgreen)
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
###############################################################################
#   Continuously show the analog readings from front bumpers.
#
#   Can be used to see ambient lighting effects on light sensors used as part
#   of the bumper setup on the 3pi+ 2040 robot.
#
###############################################################################
import time
from pololu_3pi_2040_robot import robot

display = robot.Display()
bump_sensors = robot.BumpSensors()
button_c = robot.ButtonC()

# Can press the C button on the robot to re-run this calibration at any time.
bump_sensors.calibrate()

while True:
    bump = bump_sensors.read()
    left = bump[0]
    right = bump[1]
    delta = left - right

    display.fill(0)
    display.text(" Left: {}".format(left), 0, 0)
    display.text("Right: {}".format(right), 0, 10)
    display.text(" Diff: {}".format(delta), 0, 20)

    # Draw bar graph depicting state of analog bumper switches.
    scale = (64-40)/1023
    if bump_sensors.left_is_pressed():
        display.fill_rect(0, 64-int(left*scale), 8, int(left*scale), 1)
    else:
        display.rect(0, 64-int(left*scale), 8, int(left*scale), 1)
    if bump_sensors.right_is_pressed():
        display.fill_rect(120, 64-int(right*scale), 8, int(right*scale), 1)
    else:
        display.rect(120, 64-int(right*scale), 8, int(right*scale), 1)

    display.show()

    if button_c.check():
        bump_sensors.calibrate()

    time.sleep_ms(2)
