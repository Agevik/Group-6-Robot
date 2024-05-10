# PA1473 - Software Development: Agile Project

## Introduction

This is Group 6's work of the 'Sorting System'-robot in PA1473-2024, BTH. 
Members: Lukas Roos, Feras Alnaser, Leo Lindahl Agevik


## Getting started

The LEGO® MINDSTORMS® EV3 MicroPython and ev3dev-browser extensions on VS Code are needed to further develop the code. To execute the code you need to upload the code onto a EV3 Brick with the necessary components (see LEGO® MINDSTORMS® EV3 Robot Arm H25).


## Building and running

Initializing:

The program begins by initializing the EV3 Brick and configuring the motors and sensors. The initialization code is taken from the default code given on the pybricks website.

Starting mode:

The program begins in a "starting-mode", waiting for user input to start the program. During this mode you may also change the values of your pick-up zone and drop-off zones. To start the program hold down the "down" button on the EV3 Brick, this will put the program in the "monitor-mode".


Monitor mode:

The program is now in a "monitor-mode". It will rotate it's body until it's above the pick-up zone. It will then try to detect a block by lowering down, gripping the block (or nothing) and finally scanning with the color sensor to see if a block is detected. If a block is detected it will then rotate to drop-off zone assigned to the blocks color and release it there. If no block was discovered it will simply try to detect a new block by lowering down, gripping the block and scanning. It will iterate this until a new mode is entered or the program is exited. Note: if the color sensor detects a color which is not one of either green, blue, yellow or red it will drop off the object at the color blue's drop-off zone.


Change angle of pick-up zone:

By holding the "up" button on the EV3 Brick (note: you may need to hold the button for a while, as it checks which button are pressed only on th beginning of each iteration in the monitor mode) you enter the mode to change the pick-up zone. In this mode you can change the angle of the pick-up zone. To increase the value, hold in the "up" button and to decrease the value, hold in the "down" button. To exit this mode and return to the monitor-mode, hold in the "center" button.


Change angles of drop-off zones:

Similarly as the previous mode, by holding the "right"-button you enter the mode to change the drop-off zones for each color. In this mode you can change the angle of each of the four drop-off zones. To increase/decrease hold in the "up"/"down" button and to scroll between the colors, hold in the "left" or "right" buttons.


Emergency stop:

To perform an emergency stop, you need to hold in the "down" button. The machine will immediately lower its elbow and stop running. You can continue running the program by holding in the "center" button. 
Note: when calling the emergency stop you need to hold in the button until it has completely stopped, or else it may start running again without stopping.


Pause:

To pause the program, hold in the "left" button. The machine will hold its position until the "right" button is held, at which point it will continue running. 
Note: the pause function is untested and may cause issues.


## Features

- [x] US01B: As a customer, I want the robot to pick up items from a designated position.
- [x] US02B: As a customer, I want the robot to drop items off at a designated position.
- [x] US03: As a customer, I want the robot to be able to determine if an item is present at a given location.
- [ ] US04B: As a customer, I want the robot to tell me the color of an item at a designated position.
- [x] US05: As a customer, I want the robot to drop items off at different locations based on the color of the item.
- [ ] US06: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] US08: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived.
- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item as arrived.
- [ ] US10: As a customer, I want the robots to sort items at a specific time.
- [ ] US11: As a customer, I want two robots (from two teams) to communicate and work together on items sorting without colliding with each other.
- [x] US12: As a customer, I want to be able to manually set the locations and heights of one pick up zone and two drop-off zones.
- [x] US13: As a customer, I want to easily reprogram the pickup and drop off zone of the robot.
- [ ] US14: As a customer, I want to easily change the schedule of the robot pick up task.
- [x] US15: As a customer, I want to have an emergency stop button, that immediately terminates the operation of the robot safely.
- [x] US16: As a customer, I want the robot to be able to pick an item up and put it in the designated drop-off location within 5 seconds.
- [ ] US17: As a customer, I want the robot to pick up items from a rolling belt and put them in the designated positions based on color and shape.
- [x] US18: As a customer, I want to have a pause button that pauses the robot's operation when the button is pushed and then resumes the program from the same point when I push the button again.
- [x] US19: As a customer, I want a very nice dashboard to configure the robot program and start some taska on demand.
