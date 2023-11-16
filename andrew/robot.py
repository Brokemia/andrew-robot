from dynamixel_sdk import PortHandler, PacketHandler
from .servo import Servo
from .led import LedController
from .config import AndrewConfig

class AndrewRobot:
    DXL_PROTOCOL_VERSION = 1.0
    DXL_ALL_ID = 254
    POSITION_ERROR_MARGIN = 10
    SAFE_HEIGHT = 1579
    GRIPPER_CLOSED_LOAD = 250
    GRIPPER_CLOSED_POSITION = 2100
    GRIPPER_OPEN_POSITION = 2531
    # TODO Get this from andrew.xml
    THUMB_NEUTRAL_POSITION = 1700
    THUMB_DEPRESS_FIRST_POSITION = 2980
    THUMB_DEPRESS_SECOND_POSITION = 3050
    THUMB_EJECT_POSITION = 1498
    ARM_LED_ID = 1
    BODY_LED_ID = 2

    _max_speed = 50

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

        # TODO set speeds
        # Values taken from AndrewOS logs
        self.shoulder = Servo(1, self.port_handler, self.packet_handler)
        self.shoulder.torque_limit = 750
        self.shoulder.set_joint_mode(0, 4095)
        # print(self.shoulder.resolution_divider)
        # self.shoulder.resolution_divider = 1
        # TODO resolution divider acting funky
        self.shoulder.set_pid(20, 0, 0)
        self.shoulder.temperature_limit = 75

        self.elbow = Servo(2, self.port_handler, self.packet_handler)
        self.elbow.torque_limit = 750
        self.elbow.set_joint_mode(0, 4095)
        # self.elbow.resolution_divider = 1
        self.elbow.set_pid(20, 0, 0)
        self.elbow.temperature_limit = 75

        self.wrist = Servo(3, self.port_handler, self.packet_handler)
        self.wrist.torque_limit = 750
        self.wrist.set_joint_mode(0, 4095)
        # self.wrist.resolution_divider = 1
        self.wrist.set_pid(20, 0, 0)
        self.wrist.temperature_limit = 75

        self.linear = Servo(4, self.port_handler, self.packet_handler)
        self.linear.torque_limit = 1023
        self.linear.set_joint_mode(0, 4095)
        # self.linear.resolution_divider = 1
        self.linear.set_pid(40, 5, 0)
        self.linear.temperature_limit = 90

        self.thumb = Servo(5, self.port_handler, self.packet_handler)
        self.thumb.torque_limit = 1023
        self.thumb.set_joint_mode(0, 4095)
        # self.thumb.resolution_divider = 1
        self.thumb.set_pid(50, 0, 0)
        self.thumb.temperature_limit = 75

        self.gripper = Servo(6, self.port_handler, self.packet_handler)
        self.gripper.torque_limit = 1023
        self.gripper.set_joint_mode(0, 4095)
        # self.gripper.resolution_divider = 1
        self.gripper.set_pid(50, 5, 0)
        self.gripper.temperature_limit = 75

        # Twister seems to follow different rules
        self.twister = Servo(7, self.port_handler, self.packet_handler)
        self.twister.torque_limit = 1023
        self.twister.set_wheel_mode()
        # self.twister.resolution_divider = 1
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
        slot = self.config.pipette_slots[f'slot{slot_index}']
        # TODO calculate height from config data
        self.move_arm_servos(*slot.start_position, linear=2035)
        self.max_speed = 12
        self.shoulder.moving_speed = 8
        self.elbow.moving_speed = 8
        # self.wrist.disable_torque()
        # self.shoulder.disable_torque()
        # self.elbow.disable_torque()
        # while True:
        #     pass
        self.move_arm_servos(*slot.grab_position)
        self.close_gripper()
        while True:
            pass

    def move_arm_servos(self,
                        shoulder: int=None,
                        elbow: int=None,
                        wrist: int=None,
                        linear: int=None):
        self.move_servos(shoulder=shoulder, elbow=elbow, wrist=wrist, linear=linear)
        

    # Move such that it won't bump into the pipette holder (unless that's the specified goal)
    def move_servos(self,
                    shoulder: int=None,
                    elbow: int=None,
                    wrist: int=None,
                    linear: int=None,
                    thumb: int=None,
                    gripper: int=None,
                    twister: int=None):
        moving_xy = shoulder is not None or elbow is not None or wrist is not None
        # If we're moving the linear and there's a chance it could hit the pipette holder, move it up first
        if linear is not None and moving_xy and self.linear.position > self.SAFE_HEIGHT:
            # move to the higher of the two (lower servo position)
            self.move_servos_unsafe(linear=min(self.SAFE_HEIGHT, linear))

        # We should now be at a height where we can do whatever without hitting the pipette holder
        self.move_servos_unsafe(shoulder, elbow, wrist, thumb=thumb, gripper=gripper, twister=twister)

        self.move_servos_unsafe(linear=linear)

    def move_servos_unsafe(self,
                                shoulder: int=None,
                                elbow: int=None,
                                wrist: int=None,
                                linear: int=None,
                                thumb: int=None,
                                gripper: int=None,
                                twister: int=None):
        self._move_servos_unsafe([shoulder, elbow, wrist, linear, thumb, gripper, twister])

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

    def led_arm(self, power=255):
        self.led.set_power(self.ARM_LED_ID, power)

    def led_body(self, power=255):
        self.led.set_power(self.BODY_LED_ID, power)