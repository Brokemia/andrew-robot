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

    robot.disable_torque()
    while True:
        print(robot.get_servo_positions())
        input()
        pass

if __name__ == '__main__':
    main()