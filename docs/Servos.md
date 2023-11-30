# Servos
The robot uses 7 different servos, labeled as the "shoulder", "elbow", "wrist", "linear", "thumb", "gripper", and "twister" servos. All of these servos are from Dynamixel, and may be of different types. In the robots we analyzed, they were the [MX-106T/R](https://emanual.robotis.com/docs/en/dxl/mx/mx-106/) and [MX-28T/R](https://emanual.robotis.com/docs/en/dxl/mx/mx-28/).

TODO insert diagram

Every servo has an ID, allowing it to be identified when communicating with multiple servos on a shared bus. In the Andrew robot these go from 1-7, although log files indicate servos for a "homogeniser" (8), "analab" (9), "magBead" (10), and "magBead2" (11) may also be present. These are not provided in our code, however.

The servos use [DYNAMIXEL Protocol 1.0](https://emanual.robotis.com/docs/en/dxl/protocol1/) for communication.
