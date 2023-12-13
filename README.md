# Reverse Engineering the Andrew Robot
Andrew is a robot designed to automatically perform bioscience experiments through pipetting precise quantities of liquids. The original Andrew robots are no longer supported by [the manufacturer](https://www.andrewalliance.com/). Additionally, the existing software is old and based on Adobe AIR, a product similar to Flash, which is no longer supported by Adobe. To revitalize old robots, this repo exists to document the hardware and software of the Andrew robots, along with providing a Python library to interface with the robot.

## Software Library
To install the package, run:
```
$ pip install andrew_robot
```

For basic usage, the `AndrewRobot` class can be used to control both the servos and lights of the robot.

```python
from andrew.robot import AndrewRobot

robot = AndrewRobot('D:\\Resources\\andrew.xml', 'COM3', 250000, 'COM4')
# Set the max speed to something reasonably slow
robot.max_speed = 50
```
The AndrewRobot constructor takes the path to the andrew.xml config file, the serial port for the servos, the baud rate for the servos (this is presumably 250000 for all Andrew robots), and the serial port for the LED controller.

To control the servos, the `move_servos()` fucntion can be used. This method will attempt to move the arm to a safe height before moving the rest of the servos to their desired position, and then changing the arm height to its own desired position.
```python
robot.move_servos(shoulder=1065, elbow=1530, wrist=1300, linear=2035, thumb=1779)
```
The right servo values for a desired pose can be found using the example `find_poses.py`.

Functions to control the LEDs are also provided. Note that these will need a slight delay after creating an `AndrewRobot` instance, as the LED controller restarts upon starting serial communication.
```python
# Delay to let the LED controller restart
time.sleep(.1)

robot.led_arm(0)
robot.led_body(0)
```

## Documentation
- [Communicating with the different parts of the robot](https://github.com/Brokemia/andrew-robot/blob/master/docs/Communication.md)
- [Deep dive into the hardware of Andrew](https://github.com/Brokemia/andrew-robot/blob/master/docs/HardwareBreakdown.md)
- [Servo communication and IDs](https://github.com/Brokemia/andrew-robot/blob/master/docs/Servos.md)
- [Controlling the LEDs](https://github.com/Brokemia/andrew-robot/blob/master/docs/LightControls.md)
- [Software provided by Andrew Alliance](https://github.com/Brokemia/andrew-robot/blob/master/docs/TheIntendedWay.md)

## Limitations
Research for this was done largely using the TODO model of Andrew robot. It is very possible that other robots may have issues with this library. Pull requests to improve the information and code here are welcome.