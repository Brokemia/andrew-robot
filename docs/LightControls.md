# Controlling the Lights
One of the serial devices connected to the Andrew USB hub can be used to control the lights on the robot. The serial protocol for this is fairly simple and just uses ASCII digits.
- Send a single digit to indicate which light should be controlled (1 or 2)
  - LED 1 is on the robot arm near the gripper
  - LED 2 is at the top near the twister
- Send a three digit number representing the intensity (000-255)

These digits should be sent as normal ASCII text, and should not have any spaces, newlines, or other characters separating them, even between different commands. For example, sending `1255225510002000` will turn both lights to full power, and then off.

Successfully entering a command will return the response:
```
LEDX Y
```
Where X is the light ID, and Y is the intensity it has been set to.

Entering an invalid command will result in the following error being returned:
```
error
deve ssere inserito prima il canale 1o2 seguito dal valore compreso tra 0 e 255
```
Which is roughly Italian for:
```
error
channel 1 or 2 must be entered first followed by the value between 0 and 255
```