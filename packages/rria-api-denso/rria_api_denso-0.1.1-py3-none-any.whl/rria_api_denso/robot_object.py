from time import sleep

from rria_api_denso.action_denso import ActionDenso
from rria_api_denso.connect_denso import ConnectDenso


class RobotObject:
    def __init__(self, ip_address, robot_type):
        self.ip_address = ip_address
        self.robot_type = robot_type

        # This attribute is used to store the general robot instance
        self.robot_instance = None
        self.robot_handle = None

        # This attribute is used to store the general connection instance
        self.connection_instance = None

        # This attribute is used to store the general action instance
        self.action_object = None

    def connect_robot(self):
        """
        Connect robot depends on the robot type
        :rtype: bool

        """

        if self.robot_type == 'denso':
            try:
                self.connection_instance = ConnectDenso(self.ip_address)
                self.connection_instance.set_parameters(option="Server=" + self.ip_address)
                self.robot_instance, self.robot_handle = self.connection_instance.connect_robot()

                # Create action object
                self.action_object = ActionDenso(self.robot_instance, self.robot_handle)

                return True

            except(Exception,):
                print('The connection attempt failed. Check the physical connection to the robot and try again later.')

                return False

        if self.robot_type == 'test':
            sleep(1)
            return True

    def disconnect_robot(self):
        """
        Close connection with robot
        :rtype: None

        """
        if self.robot_type == 'denso':
            self.connection_instance.disconnect_robot()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def safe_disconnect(self):
        """
        Move robot for home position and close connection with robot. Home position depends on robot type. For Gen3 is
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  degrees and for Ned is [0.0, 0.3, -1.3, 0.0, 0.0, 0.0] radians.
        :rtype: None

        """
        if self.robot_type == 'denso':
            self.action_object.move_to_zero()
            self.connection_instance.disconnect_robot()

        if self.robot_type == 'test':
            sleep(1)
            return True

    # Motor methods
    def motor_on(self):
        """
        Turn motor on
        :rtype: None

        """
        if self.robot_type == 'denso':
            self.action_object.motor_on()

        if self.robot_type == 'test':
            sleep(1)
            print('Motor on Tac Tac Tac')
            return True

    def motor_off(self):
        """
        Turn motor off
        :rtype: None

        """
        if self.robot_type == 'denso':
            self.action_object.motor_off()

        if self.robot_type == 'test':
            sleep(1)
            print('Motor off Tac')
            return True

    # Move Joints/Cartesian methods
    def joints(self):
        return self.get_joints()

    def get_joints(self):
        """
        Get joints value in radians
        You can also use a getter ::

            joints = robot.get_joints()
            joints = robot.joints

        :return: List of joints value
        :rtype: list[float]
        """
        if self.robot_type == 'denso':
            return self.action_object.get_joints()

        if self.robot_type == 'test':
            sleep(0.5)
            return ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']

    def move_joints(self, j1, j2, j3, j4, j5, j6):
        """
        Move robot joints. Joints are expressed in degrees.

        All lines of the next example realize the same operation: ::

            robot.move_joints(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)

        :param j1: joint 1,
        :type j1: float
        :param j2: joint 2,
        :type j2: float
        :param j3: joint 3,
        :type j3: float
        :param j4: joint 4,
        :type j4: float
        :param j5: joint 5,
        :type j5: float
        :param j6: joint 6,
        :type j6: float
        :rtype: None
        """
        if self.robot_type == 'denso':
            self.action_object.move_joints(j1, j2, j3, j4, j5, j6)

        if self.robot_type == 'test':
            sleep(1)
            return True

    def cartesian(self):
        return self.get_cartesian()

    def get_cartesian(self):
        """
        Get end effector link pose as [x, y, z, roll, pitch, yaw].
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians
        You can also use a getter ::

            pose = robot.get_pose()
            pose = robot.pose

        :rtype: PoseObject
        """
        if self.robot_type == 'denso':
            return self.action_object.get_cartesian()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def move_cartesian(self, x, y, z, roll, pitch, yaw):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw, frame_name) pose
        in a particular frame (frame_name) if defined.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians

        All lines of the next example realize the same operation: ::

            robot.move_cartesian(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)

        :param x: coordinate x,
        :type x: float
        :param y: coordinate y,
        :type y: float
        :param z: coordinate z,
        :type z: float
        :param roll: rotation on x-axis,
        :type roll: float
        :param pitch: rotation on y-axis,
        :type pitch: float
        :param yaw: rotation on z-axis,
        :type yaw: float
        :rtype: None
        """
        if self.robot_type == 'denso':
            return self.action_object.move_cartesian([x, y, z, roll, pitch, yaw])

        if self.robot_type == 'test':
            sleep(1)
            return True

    def move_to_home(self):
        """
        Move robot for home position. Home position depends on robot type. For Gen3 is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        degrees and for Ned is [0.0, 0.3, -1.3, 0.0, 0.0, 0.0] radians.

        :rtype: None
        """
        if self.robot_type == 'denso':
            self.action_object.move_to_home()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def move_to_zero(self):
        """
        Move robot for zero position. Home position depends on robot type. For Gen3 is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        degrees and for Ned is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] radians.

        :rtype: None
        """
        if self.robot_type == 'denso':
            self.action_object.move_to_zero()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def open_gripper(self):
        """
        Open gripper.
        :rtype: None
        """
        if self.robot_type == 'denso':
            self.action_object.open_gripper()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def close_gripper(self):
        """
        Close gripper
        :rtype: None
        """
        if self.robot_type == 'denso':
            self.action_object.close_gripper()

        if self.robot_type == 'test':
            sleep(1)
            return True

    def set_velocity(self, speed, acceleration=10, deceleration=10):
        """
        Limit arm max velocity to a percentage of its maximum velocity. For niryo one, velocity is a percentage of 100.
        For gen3, there are two types of velocities, an angular and a cartesian. The speed used in this method is
        angular.

        Args:
            speed: Should be between 1 & 100
            acceleration: Should be between 1 & 100, value default is 10.
            deceleration: Should be between 1 & 100, value default is 10.

        """
        if self.robot_type == 'denso':
            self.action_object.set_velocity(speed, acceleration, deceleration)

        if self.robot_type == 'test':
            sleep(1)
            return True

    def calibrate(self):
        """
        Start an automatic motors calibration if motors are not calibrated yet

        *NOT IMPLEMENTED*

        :rtype: None
        """
        if self.robot_type == 'denso':
            ...

        if self.robot_type == 'test':
            sleep(1)
            return True

    def go_to_sleep(self):
        """
        Go home pose and activate learning mode. The function is available only for Ned robot.

        *NOT IMPLEMENTED*

        :rtype: None
        """
        if self.robot_type == 'denso':
            ...

        if self.robot_type == 'test':
            sleep(1)
            return True
