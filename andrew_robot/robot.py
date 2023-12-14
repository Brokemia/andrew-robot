from dynamixel_sdk import PortHandler, PacketHandler
from .servo import Servo
from .led import LedController
from .config import AndrewConfig

class AndrewRobot:
    DXL_PROTOCOL_VERSION = 1.0
    DXL_ALL_ID = 254
    POSITION_ERROR_MARGIN = 10
    # TODO Most of these should be read from config files on the robot rather than being hardcoded
    # They may function incorrectly on the wrong model of robot
    SAFE_HEIGHT = 1600
    GRAB_HEIGHT = 2035
    GRIPPER_CLOSED_LOAD = 250
    GRIPPER_CLOSED_POSITION = 2100
    GRIPPER_OPEN_POSITION = 2531
    THUMB_NEUTRAL_POSITION = 1700
    THUMB_DEPRESS_FIRST_POSITION = 2970
    THUMB_DEPRESS_SECOND_POSITION = 3050
    THUMB_EJECT_POSITION = 1498
    ARM_LED_ID = 1
    BODY_LED_ID = 2

    # Relatively slow default speed
    _max_speed = 60

    def __init__(self, config_path: str, servo_com: str, servo_baud: int, led_com: str) -> None:
        self.config = AndrewConfig(config_path)
        self.port_handler = PortHandler(servo_com)
        # The baudrate passed to setupPort is ignored
        # So we have to set it separately
        self.port_handler.baudrate = servo_baud
        self.port_handler.setupPort(servo_baud)
        self.packet_handler = PacketHandler(self.DXL_PROTOCOL_VERSION)

        self._init_servos()
        self.led = LedController(led_com)

    def _init_servos(self):
        # I increased the Ki for the linear and gripper because they had trouble at low speeds

        # Values taken from AndrewOS logs
        self.shoulder = Servo(1, self.port_handler, self.packet_handler)
        self.shoulder.torque_limit = 750
        self.shoulder.set_joint_mode(0, 4095)
        self.shoulder.set_pid(20, 0, 0)
        self.shoulder.temperature_limit = 75

        self.elbow = Servo(2, self.port_handler, self.packet_handler)
        self.elbow.torque_limit = 750
        self.elbow.set_joint_mode(0, 4095)
        self.elbow.set_pid(20, 0, 0)
        self.elbow.temperature_limit = 75

        self.wrist = Servo(3, self.port_handler, self.packet_handler)
        self.wrist.torque_limit = 750
        self.wrist.set_joint_mode(0, 4095)
        self.wrist.set_pid(20, 0, 0)
        self.wrist.temperature_limit = 75

        self.linear = Servo(4, self.port_handler, self.packet_handler)
        self.linear.torque_limit = 1023
        self.linear.set_joint_mode(0, 4095)
        self.linear.set_pid(40, 5, 0)
        self.linear.temperature_limit = 90

        self.thumb = Servo(5, self.port_handler, self.packet_handler)
        self.thumb.torque_limit = 1023
        self.thumb.set_joint_mode(0, 4095)
        self.thumb.set_pid(50, 0, 0)
        self.thumb.temperature_limit = 75

        self.gripper = Servo(6, self.port_handler, self.packet_handler)
        self.gripper.torque_limit = 1023
        self.gripper.set_joint_mode(0, 4095)
        self.gripper.set_pid(50, 5, 0)
        self.gripper.temperature_limit = 75

        # Twister seems to follow different rules
        self.twister = Servo(7, self.port_handler, self.packet_handler)
        self.twister.torque_limit = 1023
        self.twister.set_wheel_mode()
        self.twister.set_pid(50, 0, 0)
        self.twister.temperature_limit = 75

        self.servos = [
            self.shoulder,
            self.elbow,
            self.wrist,
            self.linear,
            self.thumb,
            self.gripper,
            self.twister]
        
        # Make sure the setter gets called
        self.max_speed = self._max_speed
        
    @property
    def max_speed(self):
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = value
        for s in self.servos:
            if s.is_wheel_mode():
                continue
            curr_speed = s.moving_speed
            if curr_speed == 0 or curr_speed > value:
                s.moving_speed = value

    def get_servo_positions(self):
        return [s.position for s in self.servos]

    def execute_staged_writes(self):
        self.packet_handler.action(self.port_handler, self.DXL_ALL_ID)

    def close_gripper(self):
        self.gripper.set_goal_position(self.GRIPPER_CLOSED_POSITION)
        self.gripper.enable_torque()

        while abs(self.gripper.position - self.GRIPPER_CLOSED_POSITION) > self.POSITION_ERROR_MARGIN:
            if self.gripper.present_load > self.GRIPPER_CLOSED_LOAD:
                break

    def open_gripper(self):
        self.move_servos(gripper=self.GRIPPER_OPEN_POSITION)

    def thumb_depress_first_position(self):
        self.move_servos(thumb=self.THUMB_DEPRESS_FIRST_POSITION)

    def thumb_depress_second_position(self):
        self.move_servos(thumb=self.THUMB_DEPRESS_SECOND_POSITION)

    def thumb_neutral(self):
        self.move_servos(thumb=self.THUMB_NEUTRAL_POSITION)

    def thumb_eject(self):
        self.move_servos(thumb=self.THUMB_EJECT_POSITION)

    def grab_pipette(self, slot_index: int):
        """
        Grabs a pipette from the specified slot. Slots are numbered 1-5, with 1 being closest to the robot.
        """
        slot = self.config.pipette_slots[f'slot{slot_index}']
        self.open_gripper()
        self.move_servos_proportional(*slot.start_position, linear=self.GRAB_HEIGHT)
        self.move_servos_proportional(*slot.grab_position)
        self.close_gripper()
        # Pull the pipette out so that the user doesn't need to worry about bumping into the holder
        self.move_servos_proportional(*slot.start_position, linear=self.SAFE_HEIGHT)

    def move_arm_servos(self,
                        shoulder: int=None,
                        elbow: int=None,
                        wrist: int=None,
                        linear: int=None):
        """
        Moves exclusively the servos related to arm movement. Same as move_servos, but clarifies the intent better.
        """
        self.move_servos(shoulder=shoulder, elbow=elbow, wrist=wrist, linear=linear)
    
    def move_servos_proportional(self,
                                 shoulder: int=None,
                                 elbow: int=None,
                                 wrist: int=None,
                                 linear: int=None,
                                 thumb: int=None,
                                 gripper: int=None):
        """
        Moves servos at speeds proportional to the distance they need to travel, so
        all servos reach their goal position at the same time.
        """
        # Exclude linear, as it needs to move up and down separately to reach a safe height
        goals = [shoulder, elbow, wrist, None, thumb, gripper, None]

        # Speeds to restore after this move
        old_speeds = []

        # Find the servo that will take the longest to move at its set speed
        distances = []
        max_time = 0
        max_servo = None
        for s, p in zip(self.servos, goals):
            if p is None:
                old_speeds.append(None)
                distances.append(None)
                continue

            dist = abs(s.position - p)
            distances.append(dist)
            speed = s.moving_speed
            old_speeds.append(speed)
            if speed == 0 and dist > self.POSITION_ERROR_MARGIN:
                raise Exception(f"Servo {s.id} cannot reach its destination with a speed of 0")

            time = dist / speed
            if time > max_time:
                max_time = time
                max_servo = s
        
        # No movement needed, so just return
        if max_servo is None:
            return
        
        # Calculate the speed for each servo
        for s, dist in zip(self.servos, distances):
            if dist is None:
                continue
            print(f"Servo {s.id} distance: {dist} speed: {int(dist / max_time)}")
            s.moving_speed = int(dist / max_time)

        self.move_servos(shoulder=shoulder,
                         elbow=elbow,
                         wrist=wrist,
                         linear=linear,
                         thumb=thumb,
                         gripper=gripper)
        
        # Restore the old speeds
        for s, speed in zip(self.servos, old_speeds):
            if speed is None:
                continue

            s.moving_speed = speed

    # Move such that it won't bump into the pipette holder (unless that's the specified goal)
    def move_servos(self,
                    shoulder: int=None,
                    elbow: int=None,
                    wrist: int=None,
                    linear: int=None,
                    thumb: int=None,
                    gripper: int=None):
        """
        Moves the servos to the specified positions. Attempts to avoid hitting the pipette holder by moving to a safe height before going sideways.
        """
        moving_xy = shoulder is not None or elbow is not None or wrist is not None
        # If we're moving the linear and there's a chance it could hit the pipette holder, move it up first
        if linear is not None and moving_xy and self.linear.position > self.SAFE_HEIGHT:
            # move to the higher of the two (lower servo position)
            self.move_servos_unsafe(linear=min(self.SAFE_HEIGHT, linear))

        # We should now be at a height where we can do whatever without hitting the pipette holder
        self.move_servos_unsafe(shoulder, elbow, wrist, thumb=thumb, gripper=gripper)

        self.move_servos_unsafe(linear=linear)

    def move_servos_unsafe(self,
                                shoulder: int=None,
                                elbow: int=None,
                                wrist: int=None,
                                linear: int=None,
                                thumb: int=None,
                                gripper: int=None):
        self._move_servos_unsafe([shoulder, elbow, wrist, linear, thumb, gripper, None])

    def _move_servos_unsafe(self, positions: [int]):
        zipped = zip(self.servos, positions)
        for s, p in zipped:
            if p is not None:
                s.set_goal_position(p, stage=True)

        self.execute_staged_writes()

        for s, p in zipped:
            if p is not None:
                s.enable_torque(stage=True)

        self.execute_staged_writes()

        done = False
        while not done:
            done = True
            for s, p in zip(self.servos, positions):
                # if not there yet, we need to continue
                if p is not None and abs(s.position - p) > self.POSITION_ERROR_MARGIN:
                    done = False
                    break

    def enable_torque(self):
        for s in self.servos:
            s.enable_torque()

    def disable_torque(self):
        for s in self.servos:
            s.disable_torque()

    def led_arm(self, power=255):
        self.led.set_power(self.ARM_LED_ID, power)

    def led_body(self, power=255):
        self.led.set_power(self.BODY_LED_ID, power)