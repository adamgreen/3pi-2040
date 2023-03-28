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
#   Code to allow the 3π+ 2040 to roam around a room autonomously using
#   behavior based programming like the RugRover in "Mobile Robots".
#
#   Is only able to support the Cruise and Escape behaviors from the RugRover
#   code since the 3π+ robot doesn't have photocell light intensity sensor
#   or IR based obstacle detectors.
#
###############################################################################
import time
from pololu_3pi_2040_robot import robot
from micropython import const

class WheelPID:
    def __init__(self, Kp=0.5, Ki=0.05):
        self._Kp = Kp
        self._Ki = Ki
        self._desired_tick_velocity = 0.0
        self._desired_tick_bias = 0.0
        self._motorPWM = [0, 0]
        self._integral = 0.0
        self._motors = robot.Motors()
        self._encoders = robot.Encoders()
        self._last_ticks = self._encoders.get_counts()
        self._last_time = time.ticks_us()
        # This is the maximum number of encoder ticks per second for full-speed motion of my 3π+ robot.
        self._max_ticks_per_second = 5000.0
        self._percent_to_ticks_per_second = self._max_ticks_per_second / 100.0

    def set_velocities(self, velocity, steering_bias):
        self._desired_tick_velocity = velocity * self._percent_to_ticks_per_second
        self._desired_tick_bias = steering_bias * self._percent_to_ticks_per_second

    def update(self):
        ticks_delta = [0.0, 0.0]
        curr_time = time.ticks_us()
        curr_ticks = self._encoders.get_counts()
        elapsed_time = curr_time - self._last_time
        ticks_delta[0] = (curr_ticks[0] - self._last_ticks[0]) / (elapsed_time / 1000000.0)
        ticks_delta[1] = (curr_ticks[1] - self._last_ticks[1]) / (elapsed_time / 1000000.0)

        errors = [0.0, 0.0]
        integral_error = self._Ki * self._integrate(ticks_delta)
        errors[0] = self._Kp * (self._desired_tick_velocity - ticks_delta[0] - integral_error)
        errors[1] = self._Kp * (self._desired_tick_velocity - ticks_delta[1] + integral_error)
        self._alter_motor_pwm(errors)

        self._last_time = curr_time
        self._last_ticks = curr_ticks


    def _integrate(self, tick_counts):
        self._integral = self._integral + tick_counts[0] - tick_counts[1] + self._desired_tick_bias
        return self._integral

    def _alter_motor_pwm(self, motor_pwm_deltas):
        self._motorPWM[0] = self._clip(self._motorPWM[0] + motor_pwm_deltas[0], -robot.Motors.MAX_SPEED, robot.Motors.MAX_SPEED)
        self._motorPWM[1] = self._clip(self._motorPWM[1] + motor_pwm_deltas[1], -robot.Motors.MAX_SPEED, robot.Motors.MAX_SPEED)
        self._motors.set_speeds(self._motorPWM[0], self._motorPWM[1])

    def _clip(self, val, min, max):
        if val < min:
            val = min
        if val > max:
            val = max
        return val



class BehaviorBase:
    def __init__(self):
        self.outputActive = False
        self.outputVelocity = 0.0
        self.outputSteering = 0.0

class Cruise(BehaviorBase):
    CRUISE_SPEED = const(20.0)

    def __init__(self):
        super().__init__()

    def update(self):
        self.outputActive = True
        self.outputVelocity = CRUISE_SPEED
        self.outputSteering = 0.0

class Escape(BehaviorBase):
    STATE_IDLE = const(0)
    STATE_BACKUP = const(1)
    STATE_TURNING = const(2)
    BACKUP_SPEED = const(25.0)
    BACKUP_TIME = const(500000)
    TURN_SPEED = const(25.0)
    TURN_TIME = const(350000)

    def __init__(self):
        self._state = STATE_IDLE
        self._start_time = 0
        self._turn_bias = 0
        super().__init__()

    def update(self, left_bumper_is_pressed, right_bumper_is_pressed):
        curr_time = time.ticks_us()
        elapsed_time = curr_time - self._start_time

        if self._state == STATE_IDLE:
            if left_bumper_is_pressed:
                self._backup_and_turn(-TURN_SPEED)
            elif right_bumper_is_pressed:
                self._backup_and_turn(TURN_SPEED)
        elif self._state == STATE_BACKUP:
            if elapsed_time >= BACKUP_TIME:
                self._start_time = time.ticks_us()
                self._state = STATE_TURNING
                self.outputActive = True
                self.outputVelocity = 0.0
                self.outputSteering = self._turn_bias
        elif self._state == STATE_TURNING:
            if elapsed_time >= TURN_TIME:
                self._state = STATE_IDLE
                self.outputActive = False
                self.outputVelocity = 0.0
                self.outputSteering = 0.0

    def _backup_and_turn(self, turn_bias):
        self._turn_bias = turn_bias
        self._start_time = time.ticks_us()
        self._state = STATE_BACKUP
        self.outputActive = True
        self.outputVelocity = -BACKUP_SPEED
        self.outputSteering = 0.0



display = robot.Display()
bump_sensors = robot.BumpSensors()
wheels = WheelPID()
cruise = Cruise()
escape = Escape()

# How often should the main PID and behaviors update (frequency in Hz)?
sample_frequency = 50
sample_time = 1000000 / sample_frequency

# Speed to run the motors at in percentage (-100 to 100).
test_speed = 25.0
test_steering_bias = 0.0

# Delay for this number of seconds before starting up the motors.
startup_delay = 5

# Calibrate the analog light sensors used for the bumpers.
bump_sensors.calibrate()

# Delay specified amount of time before starting robot.
last_time_update = 0
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

next_update = time.ticks_us() + sample_time
while True:
    # Wait to run next sample at specified frequency.
    while time.ticks_us() < next_update:
        pass
    next_update += sample_time

    # Let each of the behavior state machines run and update their internal state.
    bump_sensors.read()
    cruise.update()
    escape.update(bump_sensors.left_is_pressed(), bump_sensors.right_is_pressed())

    # Arbitrate between the behaviors which want to control the wheels.
    display.fill_rect(0, 0, 128, 10, 0)
    if escape.outputActive:
        display.text("Escape Active!", 0, 0)
        wheels.set_velocities(escape.outputVelocity, escape.outputSteering)
    elif cruise.outputActive:
        display.text("Cruise Active!", 0, 0)
        wheels.set_velocities(cruise.outputVelocity, cruise.outputSteering)
    else:
        wheels.set_velocities(0, 0)
    display.show()

    wheels.update()
