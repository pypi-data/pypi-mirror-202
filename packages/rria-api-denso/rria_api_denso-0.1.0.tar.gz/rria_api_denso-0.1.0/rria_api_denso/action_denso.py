class ActionDenso:
    def __init__(self, robot_object, robot_handle):
        self.robot_object = robot_object
        self.robot_handle = robot_handle

    def motor_on(self):
        command = "Motor"
        parameters = [1, 0]
        self.robot_object.robot_execute(self.robot_handle, command, parameters)

    def motor_off(self):
        command = "Motor"
        parameters = [0, 0]
        self.robot_object.robot_execute(self.robot_handle, command, parameters)

    def move_joints(self, j1, j2, j3, j4, j5, j6):
        joints_value = [j1, j2, j3, j4, j5, j6]
        pose = [joints_value, "J", "@E"]
        comp = 1

        self.robot_object.robot_move(self.robot_handle, comp, pose, "")

    def get_joints(self):
        raise NotImplementedError("get_joints() is not implemented yet")

    def move_cartesian(self, x, y, z, rx, ry, rz, fig):
        cartesian_value = [x, y, z,  rx, ry, rz, fig]
        pose = [cartesian_value, "P", "@E"]
        comp = 1

        self.robot_object.robot_move(self.robot_handle, comp, pose, "")

    def get_cartesian(self):
        raise NotImplementedError("get_cartesian() is not implemented yet")

    def move_to_home(self):
        self.move_to_zero()

    def move_to_zero(self):
        joints_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        pose = [joints_value, "J", "@E"]
        comp = 1

        self.robot_object.robot_move(self.robot_handle, comp, pose, "")

    def open_gripper(self):
        raise NotImplementedError("open_gripper() is not implemented yet")

    def close_gripper(self):
        raise NotImplementedError("close_gripper() is not implemented yet")

    def set_velocity(self, speed=10, acceleration=10, deceleration=10):
        command = "ExtSpeed"
        parameters = [speed, acceleration, deceleration]

        self.robot_object.robot_execute(self.robot_handle, command, parameters)

    def calibrate(self):
        raise NotImplementedError("calibrate() is not implemented yet")

    def go_to_sleep(self):
        raise NotImplementedError("go_to_sleep() is not implemented yet")
