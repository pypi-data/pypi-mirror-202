from utils.bcapclient import BCAPClient


class ConnectDenso:
    def __init__(self, ip_address, port=5007, timeout=2000):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.parameters = None
        self.bcap_client = None
        self.controller_handle = None
        self.robot_handle = None

    def set_parameters(self, name="", provider="CaoProv.DENSO.RC8", machine="", option="Server=192.168.160.226"):
        """
        Args:
            name: string,
            provider: string,
            machine: string,
            option: string

        Returns:
            list: list of values from parameters

        Examples:
            >>> ConnectDenso.set_parameters(name="", provider="CaoProv.DENSO.RC8", machine="", option="Server=192.168.160.226")
                ['', 'CaoProv.DENSO.RC8', '', 'Server=192.168.160.226']
        """
        self.parameters = [name, provider, machine, option]

    def connect_robot(self):
        """
        Return the bcap_client and robot_handle objects. The bcap_client object is used to send all commands to the
        robot and the robot_handle is used in movements commands.

        Returns:
            self.bcap_client: object
            self.robot_handle: object
        """
        # Connection processing of tcp communication
        self.bcap_client = BCAPClient(self.ip_address, self.port, self.timeout)
        self.bcap_client.service_start("")

        # Connect to RC8 (RC8 provider)
        self.controller_handle = self.bcap_client.controller_connect(self.parameters[0], self.parameters[1],
                                                                     self.parameters[2], self.parameters[3])

        # Get Robot Object robot_handle
        self.robot_handle = self.bcap_client.controller_getrobot(self.controller_handle, "Arm", "")

        # TakeArm
        self.bcap_client.robot_execute(self.robot_handle, "TakeArm", [0, 0])

        return self.bcap_client, self.robot_handle

    def disconnect_robot(self, command, param):
        # Give Arm
        self.bcap_client.robot_execute(self.robot_handle, command, param)

        # Disconnect
        if self.robot_handle != 0:
            self.bcap_client.robot_release(self.robot_handle)

        if self.controller_handle != 0:
            self.bcap_client.controller_disconnect(self.controller_handle)

        self.bcap_client.service_stop()
