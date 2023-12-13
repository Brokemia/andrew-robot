#!/usr/bin/env python
from context import andrew

import time
from andrew.robot import AndrewRobot

def main():
    robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM5', 250000, 'COM6')
    robot.max_speed = 50
    # LED needs time to init
    time.sleep(.1)

    robot.led_arm(0)
    robot.led_body(0)

    robot.open_gripper()
    # while True:
    #     pass
    
    robot.open_gripper()
    robot.move_servos(1065, 1530, 1300, 2035, 1779)
    robot.move_arm_servos(987, 1413, 1580)
    robot.close_gripper()
    robot.move_servos(linear=1600)
    robot.move_arm_servos(1065, 1530, 1300)
    robot.move_arm_servos(1871, 1905, 1977)
    
    # robot.open_gripper()
    print("Done")
    while True:
        pass

if __name__ == '__main__':
    main()