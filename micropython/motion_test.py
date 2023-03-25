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
#   Run both motors at 100% power in the forward direction to see what the
#   encoder ticks per second are like. The motors will stop running when either
#   bump sensor is activated.
#
###############################################################################
import time
from pololu_3pi_2040_robot import robot

display = robot.Display()
bump_sensors = robot.BumpSensors()
motors = robot.Motors()
encoders = robot.Encoders()

# How often should the main PID and other update loop execute.
sample_frequency = 50
sample_time = 1000000 / sample_frequency

# Speed to run the motors at.
test_speed = motors.MAX_SPEED

# Delay for this number of seconds before starting up the motors.
startup_delay = 10
last_time_update = 0

# Calibrate the analog light sensors used for the bumpers.
bump_sensors.calibrate()

# Delay specified amount of time before starting motors.
curr_time = time.ticks_us()
start_time = curr_time + startup_delay * 1000000
while start_time > curr_time:
    curr_time = time.ticks_us()
    time_remaining = (start_time - curr_time + 999999) // 1000000
    if time_remaining != last_time_update:
        last_time_update = time_remaining
        display.fill_rect(0, 0, 128, 10, 0)
        display.text("Secs left: {}".format(time_remaining), 0, 0)
        display.show()

# Turn the motors on fully in the forward direction.
motors.set_speeds(test_speed, test_speed)

next_update = time.ticks_us() + sample_time
prev_counts = encoders.get_counts()
max_left_rate = 0
max_right_rate = 0
while True:
    # Wait to run next sample at specified frequency.
    # Stop the motors immediately if either bumper detects contact with an obstacle.
    while time.ticks_us() < next_update:
        bump_sensors.read()
        if bump_sensors.left_is_pressed() or bump_sensors.right_is_pressed():
            motors.off()
    next_update += sample_time

    counts = encoders.get_counts()
    left_count = counts[0] - prev_counts[0]
    right_count = counts[1] - prev_counts[1]
    prev_counts = counts
    left_rate = left_count * sample_frequency
    right_rate = right_count * sample_frequency
    max_left_rate = max(max_left_rate, left_rate)
    max_right_rate = max(max_right_rate, right_rate)

    display.fill_rect(0, 0, 128, 20, 0)
    display.text(" Left: {}".format(max_left_rate), 0, 0)
    display.text("Right: {}".format(max_right_rate), 0, 10)
    display.show()
