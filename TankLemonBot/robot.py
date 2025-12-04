from lib import FiniteStateMachine
import wpilib
import wpilib.drive

FULL_VOLTAGE = 16.0
DEADBAND = 0.3

class MyRobot(wpilib.TimedRobot):
    def _construct_states(self):
        self.fsm.construct_state(
            "forward",
            lambda: self.leftStick.getY() > DEADBAND,
            lambda: self.robotDrive.tankDrive(self.leftStick.getY(), self.leftStick.getY()),
            lambda: print("MOVE: forward")
        )

        self.fsm.construct_state(
            "backward",
            lambda: self.leftStick.getY() < -DEADBAND,
            lambda: self.robotDrive.tankDrive(self.leftStick.getY(), self.leftStick.getY()),
            lambda: print("MOVE: backward")
        )

        self.fsm.construct_state(
            "left_turn",
            lambda: self.rightStick.getX() < -DEADBAND,
            lambda: self.robotDrive.tankDrive(self.rightStick.getX(), -self.rightStick.getX()),
            lambda: print("TURN: left")
        )

        self.fsm.construct_state(
            "right_turn",
            lambda: self.rightStick.getX() > DEADBAND,
            lambda: self.robotDrive.tankDrive(self.rightStick.getX(), -self.rightStick.getX()),
            lambda: print("TURN: right")
        )

        self.fsm.construct_state(
            "stopped",
            lambda: abs(self.leftStick.getY()) < DEADBAND,
            lambda: self.robotDrive.tankDrive(0, 0),
            lambda: print("Stopped")
        )

    def robotInit(self) -> None:
        self.fsm = FiniteStateMachine(False)
        
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

        self.left = wpilib.PWMSparkMax(0)
        self.right = wpilib.PWMSparkMax(1)

        self.right.setInverted(True)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self._construct_states()

    def teleopPeriodic(self) -> None:
        self.fsm.execute()