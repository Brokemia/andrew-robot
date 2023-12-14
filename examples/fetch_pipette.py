#!/usr/bin/env python
from context import andrew_robot

import time
from andrew_robot import AndrewRobot

def main():
    # The ports and config file path will likely need to be changed to try this example
    robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM4', 250000, 'COM3')
    robot.max_speed = 50
    # LED needs time to init
    time.sleep(.1)

    robot.led_arm(0)
    robot.led_body(0)
    
    # Grab the pipette in the most outwards slot
    robot.grab_pipette(5)
    # Present the pipette towards the user
    robot.move_servos(1871, 1905, 1977)
    
    robot.open_gripper()
    print("Done")

if __name__ == '__main__':
    main()