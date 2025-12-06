from wpilib import TimedRobot
from drivetrain import DriveTrain

class LemonBot(TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = DriveTrain()

    def teleopPeriodic(self) -> None:
        self.drivetrain.fsm.execute()
        self.drivetrain.updateOdometry()