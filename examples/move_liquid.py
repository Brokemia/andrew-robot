#!/usr/bin/env python
from context import andrew_robot

import time
from andrew_robot import AndrewRobot

# Moves liquid from one test tube to another at the corners of a domino
# Tested using a "Falcon 14mL round bottom tube domino"
def main():
    # The ports and config file path will likely need to be changed to try this example
    robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM4', 250000, 'COM3')
    robot.max_speed = 30
    robot.linear.moving_speed = 50
    robot.gripper.moving_speed = 50
    robot.thumb.moving_speed = 70
    # LED needs time to init
    time.sleep(.1)

    robot.led_arm(0)
    robot.led_body(0)

    starts_with_pipette = False

    if not starts_with_pipette:
        robot.grab_pipette(5)

    # Make sure pipette is all the way up in gripper and pipette tip is on
    input("Ready?")
    robot.close_gripper()

    while True:
        for i in range(10):
            # Test tube 1
            robot.move_arm_servos(1330, 1278, 1283, 270)
            robot.move_arm_servos(linear=1289)
            # Get water
            robot.thumb_depress_first_position()
            time.sleep(.5)
            robot.thumb_neutral()
            robot.move_arm_servos(linear=270)

            # Test tube 2
            robot.move_arm_servos(1841, 1061, 1017)
            # Dispense water
            robot.thumb_depress_first_position()
            time.sleep(.5)
            robot.thumb_neutral()
        
        for i in range(10):
            # Test tube 2
            robot.move_arm_servos(1841, 1061, 1017, 270)
            robot.move_arm_servos(linear=1289)
            # Get water
            robot.thumb_depress_first_position()
            time.sleep(.5)
            robot.thumb_neutral()
            robot.move_arm_servos(linear=270)

            # Test tube 1
            robot.move_arm_servos(1330, 1278, 1283)
            # Dispense water
            robot.thumb_depress_first_position()
            time.sleep(.5)
            robot.thumb_neutral()

if __name__ == '__main__':
    main()