from typing import NamedTuple

ADDR_MODEL_NUMBER = 0

class ServoDef(NamedTuple):
    model_number: int
    # EEPROM
    addr_model_number: int = ADDR_MODEL_NUMBER
    addr_firmware_version: int = -1
    addr_id: int = -1
    addr_baud_rate: int = -1
    addr_return_delay_time: int = -1
    addr_angle_limit_cw: int = -1
    addr_angle_limit_ccw: int = -1
    addr_drive_mode: int = -1
    addr_temperature_limit: int = -1
    addr_min_voltage: int = -1
    addr_max_voltage: int = -1
    addr_max_torque: int = -1
    addr_status_return_level: int = -1
    addr_alarm_led: int = -1
    addr_shutdown: int = -1
    addr_multi_turn_offset: int = -1
    addr_resolution_divider: int = -1
    # RAM
    addr_torque_enable: int = -1
    addr_led: int = -1
    addr_d_gain: int = -1
    addr_i_gain: int = -1
    addr_p_gain: int = -1
    addr_goal_position: int = -1
    addr_moving_speed: int = -1
    addr_torque_limit: int = -1
    addr_present_position: int = -1
    addr_present_speed: int = -1
    addr_present_load: int = -1
    addr_present_voltage: int = -1
    addr_present_temperature: int = -1
    addr_registered: int = -1
    addr_moving: int = -1
    addr_lock: int = -1
    addr_punch: int = -1
    addr_realtime_tick: int = -1
    addr_current: int = -1
    addr_torque_control_mode_enable: int = -1
    addr_goal_torque: int = -1
    addr_goal_acceleration: int = -1

# https://emanual.robotis.com/docs/en/dxl/mx/mx-106/
MX106 = ServoDef(
    model_number=320,
    addr_firmware_version=2,
    addr_id=3,
    addr_baud_rate=4,
    addr_return_delay_time=5,
    addr_angle_limit_cw=6,
    addr_angle_limit_ccw=8,
    addr_drive_mode=10,
    addr_temperature_limit=11,
    addr_min_voltage=12,
    addr_max_voltage=13,
    addr_max_torque=14,
    addr_status_return_level=16,
    addr_alarm_led=17,
    addr_shutdown=18,
    addr_multi_turn_offset=20,
    addr_resolution_divider=22,
    addr_torque_enable=24,
    addr_led=25,
    addr_d_gain=26,
    addr_i_gain=27,
    addr_p_gain=28,
    addr_goal_position=30,
    addr_moving_speed=32,
    addr_torque_limit=34,
    addr_present_position=36,
    addr_present_speed=38,
    addr_present_load=40,
    addr_present_voltage=42,
    addr_present_temperature=43,
    addr_registered=44,
    addr_moving=46,
    addr_lock=47,
    addr_punch=48,
    addr_realtime_tick=50,
    addr_current=68,
    addr_torque_control_mode_enable=70,
    addr_goal_torque=71,
    addr_goal_acceleration=73,
)

# https://emanual.robotis.com/docs/en/dxl/mx/mx-28/
MX28 = ServoDef(
    model_number=29,
    addr_firmware_version=2,
    addr_id=3,
    addr_baud_rate=4,
    addr_return_delay_time=5,
    addr_angle_limit_cw=6,
    addr_angle_limit_ccw=8,
    addr_temperature_limit=11,
    addr_min_voltage=12,
    addr_max_voltage=13,
    addr_max_torque=14,
    addr_status_return_level=16,
    addr_alarm_led=17,
    addr_shutdown=18,
    addr_multi_turn_offset=20,
    addr_resolution_divider=22,
    addr_torque_enable=24,
    addr_led=25,
    addr_d_gain=26,
    addr_i_gain=27,
    addr_p_gain=28,
    addr_goal_position=30,
    addr_moving_speed=32,
    addr_torque_limit=34,
    addr_present_position=36,
    addr_present_speed=38,
    addr_present_load=40,
    addr_present_voltage=42,
    addr_present_temperature=43,
    addr_registered=44,
    addr_moving=46,
    addr_lock=47,
    addr_punch=48,
    addr_realtime_tick=50,
    addr_goal_acceleration=73,
)

servo_models = {
    MX106.model_number: MX106,
    MX28.model_number: MX28,
}

def identify_servo(servo):
    return servo_models[servo.read_bytes(ADDR_MODEL_NUMBER, 2)]
