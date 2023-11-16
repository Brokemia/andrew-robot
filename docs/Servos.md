# Servos
The robot uses 7 different servos, labeled as the "shoulder", "elbow", "wrist", "linear", "thumb", "gripper", and "twister" servos. All of these servos are from Dynamixel, and may be of different types. In the robots we analyzed, they were TODO and TODO.

TODO insert diagram

Every servo has an ID, allowing it to be identified when communicating with multiple servos on a shared bus. In the Andrew robot these go from 1-7, although log files indicate servos for a "homogeniser" (8), "analab" (9), "magBead" (10), and "magBead2" (11) are also supported.