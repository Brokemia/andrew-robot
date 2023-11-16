#!/usr/bin/env python
from context import andrew

import time
from andrew.robot import AndrewRobot

def main():
    # print(pkt.read2ByteTxRx(port, 1, 0))
    robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM4', 250000, 'COM3')
    robot.max_speed = 40
    # LED needs time to init
    time.sleep(.1)

    robot.led_arm(0)
    robot.led_body(0)
    
    robot.open_gripper()
    robot.grab_pipette(5)
    robot.move_servos(linear=1600)
    robot.move_arm_servos(1065, 1530, 1300)
    robot.move_arm_servos(1871, 1905, 1977)
    
    robot.open_gripper()
    print("done")
    while True:
        pass

if __name__ == '__main__':
    main()