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
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

import socket


# Initialize the EV3 Brick
ev3 = EV3Brick()

# Setup socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.1', 8080))  # Bind to any IP on port 8080
server_socket.listen(1)

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
    elbow_motor.run_target(60, 0)


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


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

# Define the three destinations for picking up and moving the wheel stacks.

#def zone_config():
zone1 = 200
zone2 = 160
zone3 = 105
zone4 = 50
zone5 = 5

#zone_config()
PICK_UP_ZONE = zone3
BLUE = zone1
YELLOW = zone5
RED = zone4
GREEN = zone2

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

def set_pick_up_zone(new_Pickup_Zone):
    PICK_UP_ZONE = new_Pickup_zone

def set_drop_off_zones(new_Yellow, new_Blue, new_Red):
    YELLOW = new_Yellow
    BLUE = new_Blue
    RED = new_Red

def monitor_pick_up_zone(pick_up_zone):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(60, pick_up_zone)
    # Lower the arm.
    elbow_motor.run_target(60, -40)
    #elbow_motor.run_until_stalled(-60, then=Stop.HOLD, duty_limit=10)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(60, 0)

    #anta att 0 = stängd gripper och mindre än det är öppet
    #if gripper_motor.angle() < -10:   
    #   robot_release(get_color())
    #else:
    #   

# This is the main part of the program. It is a loop that repeats endlessly.
# 
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
print("Waiting for a connection...")
connection, client_address = server_socket.accept()

try:
    print("Connection from", client_address)
    while True:
        data = connection.recv(16).decode('utf-8')
        if data:
            print("Received command:", data)
            if data == 'pick':
                robot_pick(PICK_UP_ZONE)
            elif data == 'release':
                robot_release(get_color())
            #elif data == 'stop':
                #motor.stop()
        else:
            break
finally:
    connection.close()
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.
#while True:
    # Move a wheel stack from the right to the left.
    #robot_pick(PICK_UP_ZONE)
    #robot_release(get_color())