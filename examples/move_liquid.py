#!/usr/bin/env python
from context import andrew

import time
from andrew.robot import AndrewRobot

def main():
    robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM4', 250000, 'COM3')
    robot.max_speed = 30
    robot.linear.moving_speed = 50
    robot.gripper.moving_speed = 50
    robot.thumb.moving_speed = 70
    # LED needs time to init
    time.sleep(.1)

    robot.led_arm(0)
    robot.led_body(0)

    starts_with_pipette = True

    if not starts_with_pipette:
        robot.open_gripper()
        robot.move_servos(1065, 1530, 1300, 2035, 1779)
        robot.move_arm_servos(987, 1413, 1580)
        robot.close_gripper()
        robot.move_servos(linear=1600)
        robot.move_arm_servos(1065, 1530, 1300)
        robot.move_arm_servos(1871, 1905, 1977)

    robot.close_gripper()
    # Make sure pipette is all the way up in gripper and pipette tip is on
    input("Ready?")

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