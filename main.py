#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait

import socket
import threading


# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_sensor = ColorSensor(Port.S2)

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(30, 1000)
elbow_motor.run(-15)
while elbow_sensor.reflection() < 32:
    wait(10)
elbow_motor.run_time(60, 1000)
elbow_motor.reset_angle(0)
elbow_motor.hold()


# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)

def robot_pick(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(60, position)
    # Lower the arm.
    elbow_motor.run_target(60, -40)
    #elbow_motor.run_until_stalled(-60, then=Stop.HOLD, duty_limit=10)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(50, 0)

    robot_release(get_color())


def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.

    # Rotate to the drop-off position.
    base_motor.run_target(60, position)
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(60, -40)
    #elbow_motor.run_until_stalled(-60, then=Stop.HOLD, duty_limit=10)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 0)
    monitor_bool = True


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    #ev3.speaker.beep()
    wait(100)

monitor_bool = False
change_angles_bool = False
emergency_stop_bool = False
change_pick_up_bool = False
start_bool = False
pause_bool = False

#def zone_config():
zone1 = 200
zone2 = 160
zone3 = 100
zone4 = 50
zone5 = 10

#zone_config()
PICK_UP_ZONE = zone3
BLUE = zone1
YELLOW = zone5
RED = zone4
GREEN = zone2

angles = [BLUE, YELLOW, RED, GREEN]
current_index = 0

def get_color():
    if elbow_sensor.color() == Color.YELLOW:
        return YELLOW
    elif elbow_sensor.color() == Color.BLUE:
        return BLUE
    elif elbow_sensor.color() == Color.RED:
        return RED
    elif elbow_sensor.color() == Color.GREEN:
        return GREEN
    else:
        return BLUE

def monitor_pick_up_zone():
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    gripper_motor.run_target(200, -90)
    # Rotate to the pick-up position.
    base_motor.run_target(60, PICK_UP_ZONE)
    # Lower the arm.
    elbow_motor.run_target(60, -40)
    #elbow_motor.run_until_stalled(-60, then=Stop.HOLD, duty_limit=10)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(60, 7)

    wait(1000)
    #anta att 0 = stängd gripper och mindre än det är öppet
    if gripper_motor.angle() < -10:   
        monitor_bool = False
        robot_release(get_color())

def set_time_schedule():
    print("t")

# This is the main part of the program. It is a loop that repeats endlessly.
# 
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.
def emergency_stop():
    while True:
        while Button.DOWN in ev3.buttons.pressed() and not change_pick_up_bool and not change_angles_bool:
            print("EMERGENCY CALLED")            
            monitor_bool = False
            base_motor.hold()
            elbow_motor.run_target(60, -40)
            ev3.screen.clear()
            ev3.screen.draw_text(0, 0, "Emergency stop", text_color=Color.BLACK, background_color=None)
            ev3.screen.draw_text(0, 30, "called", text_color=Color.BLACK, background_color=None)
            print(monitor_bool)
        if emergency_stop_bool:
            if Button.CENTER in ev3.buttons.pressed():
                emergency_bool = False
                monitor_bool = True

def pause():
    while pause_bool:
        while Button.LEFT in ev3.buttons.pressed() and not change_angles_bool and not change_pick_up_bool:
            base_motor.hold()

t1 = threading.Thread(target=emergency_stop)
t2 = threading.Thread(target=pause)

t1.start()
t2.start()
wait(300)

while True:
    # Check if any buttons are pressed
    if Button.UP in ev3.buttons.pressed() and change_pick_up_bool == False:
        monitor_bool = False
        change_angles_bool = True
    elif Button.RIGHT in ev3.buttons.pressed() and change_angles_bool == False:
        monitor_bool = False
        change_pick_up_bool = True
    elif Button.DOWN in ev3.buttons.pressed() and not change_angles_bool and not change_pick_up_bool and start_bool:
        monitor_bool = False
        emergency_stop_bool = True
    elif Button.LEFT in ev3.buttons.pressed() and not change_angles_bool and not change_pick_up_bool:
        monitor_bool = False
        pause_bool = True

    if monitor_bool:
        print(monitor_bool)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Monitoring pick-up ", text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(0, 30, "zones", text_color=Color.BLACK, background_color=None)
        monitor_pick_up_zone()

    if change_pick_up_bool:
        wait(500)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Pick-up zones:", text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(0, 30, str(PICK_UP_ZONE), text_color=Color.BLACK, background_color=None)

        if Button.UP in ev3.buttons.pressed():
            PICK_UP_ZONE += 10
            if PICK_UP_ZONE > 360:
                PICK_UP_ZONE -= 360
        elif Button.DOWN in ev3.buttons.pressed():
            PICK_UP_ZONE -= 10
            if PICK_UP_ZONE < 0:
                PICK_UP_ZONE += 360
        elif Button.CENTER in ev3.buttons.pressed():
            if not pause_bool:
                monitor_bool = True
            change_pick_up_bool = False


    if emergency_stop_bool and not change_angles_bool and not change_pick_up_bool and start_bool:
        monitor_bool = False
        base_motor.hold()
        elbow_motor.run_target(60, -40)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Emergency stop", text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(0, 30, "called", text_color=Color.BLACK, background_color=None)        
        if Button.CENTER in ev3.buttons.pressed():
            elbow_motor.run_target(60, 7)
            monitor_bool = True
            emergency_stop_bool = False

    if pause_bool and not change_angles_bool and not change_pick_up_bool:
        base_motor.hold()
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Paused", text_color=Color.BLACK, background_color=None)
        if Button.RIGHT in ev3.buttons.pressed():
            robot_release(get_color)
            monitor_bool = True
            pause_bool = False
        wait(100)

    if not start_bool:
        monitor_bool = False
        base_motor.hold()
        if not change_angles_bool and not change_pick_up_bool:
            wait(100)
            ev3.screen.clear()
            ev3.screen.draw_text(0, 0, "press down to start", text_color=Color.BLACK, background_color=None)
                
        if Button.DOWN in ev3.buttons.pressed() and not change_angles_bool and not change_pick_up_bool:
            elbow_motor.run_target(60, 7)
            monitor_bool = True
            start_bool = True
            

    
    if change_angles_bool:
        wait(500)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Drop off zones:", text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(0, 30, "B      Y      R      G", text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(0, 60, str(angles[0]) + "  " + str(angles[1]) + "  " + str(angles[2]) + "  " + str(angles[3]), text_color=Color.BLACK, background_color=None)
        ev3.screen.draw_text(current_index * 50, 90, "  ", Color.BLACK, background_color=Color.BLACK)
        
        # Toggle between columns
        if Button.RIGHT in ev3.buttons.pressed():
            if current_index != 3:
               current_index += 1
            else:
                current_index = 0
        elif Button.LEFT in ev3.buttons.pressed():
            if current_index != 0:
                current_index -= 1
            else:
                current_index = 3
        
        # Increase/Decrease angle value
        elif Button.UP in ev3.buttons.pressed():
            angles[current_index] += 10
            if angles[current_index] > 360:
                angles[current_index] -= 360
        elif Button.DOWN in ev3.buttons.pressed():
            angles[current_index] -= 10
            if angles[current_index] < 0:
                angles[current_index] += 360

        elif Button.CENTER in ev3.buttons.pressed():
            if not pause_bool:
                monitor_bool = True
            change_angles_bool = False 
        
        BLUE = angles[0]
        YELLOW = angles[1]
        RED = angles[2]
        GREEN = angles[3]

        print("index: " + str(current_index) + ", value: " + str(angles[current_index]))