import math
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition
from phoenix6.hardware import TalonFX, CANcoder

WHEEL_DIAMETER_M = 0.1
GEAR_RATIO = 6
MAX_SPEED_MPS = 50
MAX_VOLTAGE = 12
KP = 3.0

class SwerveModule:
    def __init__(self, drive_id: int, steer_id: int, cancoder_id: int) -> None:
        self.drive_motor = TalonFX(drive_id, canbus="can0")
        self.steer_motor = TalonFX(steer_id, canbus="can0")
        self.cancoder = CANcoder(cancoder_id, canbus="can0")

        self.drive_motor.set_position(0)

    def _read_cancoder_angle_radians(self) -> float:
        """ Returns the CANcoder absolute position in radians instead of rotations. """
        rotations = self.cancoder.get_absolute_position().value
        angle_rad = rotations * (2.0 * math.pi)
        return angle_rad
    
    def _applySteerControl(self, desired_angle: float) -> None:
        """ Drives the steering motor toward the target angle. """
        current_angle = self._read_cancoder_angle_radians()
        angle_error = (desired_angle - current_angle + math.pi) % (2 * math.pi) - math.pi

        turn_voltage = KP * angle_error
        turn_voltage = max(min(turn_voltage, 12), -12)

        self.steer_motor.setVoltage(turn_voltage)
    
    def getPosition(self) -> SwerveModulePosition:
        """ Returns the total drive position and rotation of the wheels. """
        drive_position_m = self.drive_motor.get_position().value
        angle_rad = self._read_cancoder_angle_radians()
        return SwerveModulePosition(drive_position_m, Rotation2d(angle_rad))

    def setDesiredState(self, desired_state: SwerveModuleState) -> None:
        """ Commands the SwerveModule to get to the provided state. """
        speed_fraction = desired_state.speed / MAX_SPEED_MPS
        voltage = speed_fraction * MAX_VOLTAGE
        self.drive_motor.setVoltage(voltage)

        self._applySteerControl(desired_state.angle.radians())