from dynamixel_sdk import PortHandler, Protocol1PacketHandler, Protocol2PacketHandler, COMM_SUCCESS
from .servo_defs import identify_servo

class ServoCommunicationException(Exception):
    def __init__(self, error: int, message: str) -> None:
        super().__init__(message)
        self.error = error

class ServoPacketException(Exception):
    def __init__(self, error: int, message: str) -> None:
        super().__init__(message)
        self.error = error

class Servo:
    def __init__(self, id: int, port_handler: PortHandler, packet_handler: Protocol1PacketHandler | Protocol2PacketHandler) -> None:
        self.id = id
        self.port_handler = port_handler
        self.packet_handler = packet_handler
        self.control_table = identify_servo(self)
    
    def int_to_bytelist(self, value: int, length: int) -> list[int]:
        return [value >> (8 * i) & 0xFF for i in range(length)]
    
    def bytelist_to_int(self, data: list[int]) -> int:
        return sum([data[i] << (8 * i) for i in range(len(data))])

    def write_bytes(self, address: int, length: int, data: int):
        if address < 0:
            raise ValueError("Unsupported write address")
        dxl_comm_result, dxl_error = self.packet_handler.writeTxRx(
            self.port_handler,
            self.id,
            address,
            length,
            self.int_to_bytelist(data, length))
        self.raise_errors(dxl_comm_result, dxl_error)

    def stage_write(self, address: int, length: int, data: int):
        if address < 0:
            raise ValueError("Unsupported write address")
        dxl_comm_result, dxl_error = self.packet_handler.regWriteTxRx(
            self.port_handler,
            self.id,
            address,
            length,
            self.int_to_bytelist(data, length))
        self.raise_errors(dxl_comm_result, dxl_error)
    
    def read_bytes(self, address: int, length: int):
        if address < 0:
            raise ValueError("Unsupported read address")
        res, dxl_comm_result, dxl_error = self.packet_handler.readTxRx(
            self.port_handler,
            self.id,
            address,
            length)
        self.raise_errors(dxl_comm_result, dxl_error)
        return self.bytelist_to_int(res)
    
    def ping(self) -> (bool, str | None):
        _, dxl_comm_result, dxl_error = self.packet_handler.ping(self.port_handler, self.id)
        error = self.get_error(dxl_comm_result, dxl_error)
        if error is None:
            return True, None
        return False, error

    def get_error(self, dxl_comm_result: int, dxl_error: int) -> str | None:
        if dxl_comm_result != COMM_SUCCESS:
            return self.packet_handler.getTxRxResult(dxl_comm_result)
        if dxl_error != 0:
            return self.packet_handler.getRxPacketError(dxl_error)
        return None

    def raise_errors(self, dxl_comm_result: int, dxl_error: int):
        if dxl_comm_result != COMM_SUCCESS:
            raise ServoCommunicationException(dxl_comm_result, self.packet_handler.getTxRxResult(dxl_comm_result))
        if dxl_error != 0:
            raise ServoPacketException(dxl_error, self.packet_handler.getRxPacketError(dxl_error))
    
    def write_or_stage(self, address: int, length: int, data: int, stage: bool):
        if stage:
            self.stage_write(address, length, data)
        else:
            self.write_bytes(address, length, data)

    @property
    def model_number(self):
        if not hasattr(self, "_model_number"):
            self._model_number = self.read_bytes(
                self.control_table.addr_model_number, 2)
        return self._model_number
    
    @property
    def firmware_version(self):
        if not hasattr(self, "_firmware_version"):
            self._firmware_version = self.read_bytes(
                self.control_table.addr_firmware_version, 1)
        return self._firmware_version
    
    @property
    def return_delay_time(self):
        return self.read_bytes(self.control_table.addr_return_delay_time, 1)
    
    @return_delay_time.setter
    def return_delay_time(self, delay: int):
        self.write_bytes(self.control_table.addr_return_delay_time, 1, delay)

    def set_angle_limits(self, cw: int, ccw: int):
        self.write_bytes(self.control_table.addr_angle_limit_cw, 2, cw)
        self.write_bytes(self.control_table.addr_angle_limit_ccw, 2, ccw)

    def get_angle_limits(self):
        return (
            self.read_bytes(self.control_table.addr_angle_limit_cw, 2),
            self.read_bytes(self.control_table.addr_angle_limit_ccw, 2)
        )
    
    # The servo mode is controlled by special values of the angle limits
    def set_joint_mode(self, cw: int, ccw: int):
        self.set_angle_limits(cw, ccw)

    def set_wheel_mode(self):
        self.set_angle_limits(0, 0)

    def is_wheel_mode(self) -> bool:
        return self.get_angle_limits() == (0, 0)

    def set_multiturn_mode(self):
        self.set_angle_limits(4095, 4095)
    
    @property
    def drive_mode(self):
        return self.read_bytes(self.control_table.addr_drive_mode, 1)
    
    @drive_mode.setter
    def drive_mode(self, mode: int):
        self.write_bytes(self.control_table.addr_drive_mode, 1, mode)
    
    def set_drive_mode(self, reverse: bool, joint_slave: bool=False):
        self.drive_mode = (joint_slave << 1) | reverse
    
    def is_drive_mode_reversed(self) -> bool:
        return self.drive_mode & 1
    
    @property
    def temperature_limit(self):
        return self.read_bytes(self.control_table.addr_temperature_limit, 1)
    
    @temperature_limit.setter
    def temperature_limit(self, limit: int):
        self.write_bytes(self.control_table.addr_temperature_limit, 1, limit)

    def set_voltage_limits(self, min: int, max: int):
        self.write_bytes(self.control_table.addr_min_voltage, 1, min)
        self.write_bytes(self.control_table.addr_max_voltage, 1, max)

    def get_voltage_limits(self):
        return (
            self.read_bytes(self.control_table.addr_min_voltage, 1),
            self.read_bytes(self.control_table.addr_max_voltage, 1)
        )
    
    @property
    def max_torque(self):
        return self.read_bytes(self.control_table.addr_max_torque, 2)
    
    @max_torque.setter
    def max_torque(self, torque: int):
        self.write_bytes(self.control_table.addr_max_torque, 2, torque)

    # TODO test effects of changing this
    # We may need to use readTxOnly and writeTxOnly depending on the value
    @property
    def status_return_level(self):
        return self.read_bytes(self.control_table.addr_status_return_level, 1)
    
    @status_return_level.setter
    def status_return_level(self, level: int):
        self.write_bytes(self.control_table.addr_status_return_level, 1, level)

    @property
    def alarm_led(self):
        return self.read_bytes(self.control_table.addr_alarm_led, 1)
    
    # TODO I think each bit might correspond to different errors
    # similar to shutdown
    @alarm_led.setter
    def alarm_led(self, level: int):
        self.write_bytes(self.control_table.addr_alarm_led, 1, level)

    @property
    def shutdown(self):
        return self.read_bytes(self.control_table.addr_shutdown, 1)
    
    @shutdown.setter
    def shutdown(self, level: int):
        self.write_bytes(self.control_table.addr_shutdown, 1, level)

    def get_shutdown_conditions(self) -> (bool, bool, bool, bool, bool, bool, bool):
        shutdown = self.shutdown
        return (
            shutdown & 1,
            shutdown & 2,
            shutdown & 4,
            shutdown & 8,
            shutdown & 16,
            shutdown & 32,
            shutdown & 64
        )
    
    def set_shutdown_conditions(self,
                                input_voltage=False,
                                angle_limit=False,
                                overheating=False,
                                range=False,
                                checksum=False,
                                overload=False,
                                instruction=False):
        self.shutdown = (
            (input_voltage << 0) |
            (angle_limit << 1) |
            (overheating << 2) |
            (range << 3) |
            (checksum << 4) |
            (overload << 5) |
            (instruction << 6)
        )

    @property
    def multi_turn_offset(self):
        return self.read_bytes(self.control_table.addr_multi_turn_offset, 2)
    
    @multi_turn_offset.setter
    def multi_turn_offset(self, offset: int):
        self.write_bytes(self.control_table.addr_multi_turn_offset, 2, offset)

    @property
    def resolution_divider(self):
        return self.read_bytes(self.control_table.addr_resolution_divider, 1)
    
    @resolution_divider.setter
    def resolution_divider(self, divider: int):
        self.write_bytes(self.control_table.addr_resolution_divider, 1, divider)
    
    # RAM

    def enable_torque(self, stage=False):
        self.write_or_stage(self.control_table.addr_torque_enable, 1, 1, stage)

    def disable_torque(self, stage=False):
        self.write_or_stage(self.control_table.addr_torque_enable, 1, 0, stage)

    @property
    def led(self):
        return self.read_bytes(self.control_table.addr_led, 1)
    
    @led.setter
    def led(self, on: bool):
        self.write_bytes(self.control_table.addr_led, 1, int(on))

    @property
    def d_gain(self):
        return self.read_bytes(self.control_table.addr_d_gain, 1)
    
    @d_gain.setter
    def d_gain(self, gain: int):
        self.write_bytes(self.control_table.addr_d_gain, 1, gain)

    @property
    def i_gain(self):
        return self.read_bytes(self.control_table.addr_i_gain, 1)
    
    @i_gain.setter
    def i_gain(self, gain: int):
        self.write_bytes(self.control_table.addr_i_gain, 1, gain)

    @property
    def p_gain(self):
        return self.read_bytes(self.control_table.addr_p_gain, 1)
    
    @p_gain.setter
    def p_gain(self, gain: int):
        self.write_bytes(self.control_table.addr_p_gain, 1, gain)

    def set_pid(self, p: int, i: int, d: int):
        self.p_gain = p
        self.i_gain = i
        self.d_gain = d

    def get_pid(self):
        return (self.p_gain, self.i_gain, self.d_gain)
    
    def set_goal_position(self, position: int, stage=False):
        self.write_or_stage(self.control_table.addr_goal_position, 2, position, stage)

    def get_goal_position(self):
        return self.read_bytes(self.control_table.addr_goal_position, 2)

    @property
    def moving_speed(self):
        return self.read_bytes(self.control_table.addr_moving_speed, 2)

    @moving_speed.setter
    def moving_speed(self, speed: int):
        self.write_bytes(self.control_table.addr_moving_speed, 2, speed)

    @property
    def torque_limit(self):
        return self.read_bytes(self.control_table.addr_torque_limit, 2)
    
    @torque_limit.setter
    def torque_limit(self, limit: int):
        self.write_bytes(self.control_table.addr_torque_limit, 2, limit)

    @property
    def position(self):
        return self.read_bytes(self.control_table.addr_present_position, 2)
    
    @property
    def present_speed(self):
        return self.read_bytes(self.control_table.addr_present_speed, 2)
    
    @property
    def present_load(self):
        return self.read_bytes(self.control_table.addr_present_load, 2)
    
    @property
    def present_voltage(self):
        return self.read_bytes(self.control_table.addr_present_voltage, 1)
    
    @property
    def present_temperature(self):
        return self.read_bytes(self.control_table.addr_present_temperature, 1)
    
    def has_staged_write(self):
        return self.read_bytes(self.control_table.addr_registered, 1)
    
    @property
    def moving(self):
        return self.read_bytes(self.control_table.addr_moving, 1)
    
    def lock_eeprom(self):
        self.write_bytes(self.control_table.addr_lock, 1, 1)

    def is_eeprom_locked(self):
        return self.read_bytes(self.control_table.addr_lock, 1)
    
    @property
    def punch(self):
        return self.read_bytes(self.control_table.addr_punch, 2)
    
    @punch.setter
    def punch(self, punch: int):
        self.write_bytes(self.control_table.addr_punch, 2, punch)

    @property
    def realtime_tick(self):
        return self.read_bytes(self.control_table.addr_realtime_tick, 2)
    
    @property
    def current(self):
        return self.read_bytes(self.control_table.addr_present_current, 2)
    
    @property
    def torque_control_mode(self):
        return self.read_bytes(self.control_table.addr_torque_control_mode_enable, 1)
    
    @torque_control_mode.setter
    def torque_control_mode(self, enable: bool):
        self.write_bytes(self.control_table.addr_torque_control_mode_enable, 1, enable)

    def set_goal_torque(self, torque: int, stage=False):
        self.write_or_stage(self.control_table.addr_goal_torque, 2, torque, stage)

    def get_goal_torque(self):
        return self.read_bytes(self.control_table.addr_goal_torque, 2)
    
    def set_goal_acceleration(self, acceleration: int, stage=False):
        self.write_or_stage(self.control_table.addr_goal_acceleration, 1, acceleration, stage)

    def get_goal_acceleration(self):
        return self.read_bytes(self.control_table.addr_goal_acceleration, 1)
