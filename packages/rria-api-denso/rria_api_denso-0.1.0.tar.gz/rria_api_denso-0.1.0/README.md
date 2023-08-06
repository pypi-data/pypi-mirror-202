# RRIA-API-DENSO

The `rria-api` is an easy-to-use package that provides a common interface to control robots used by the Residence in
Robotics and AI at the UFPE's informatics center. The API currently supports the use of Denso robot.

### **Requirements**

- Python 3.11
- Denso Setup Installation

### **Instalation**

1. Install the latest `rria-api-denso` package with `pip`:

```
$ pip install rria-api-denso
```

### **Example**

```
from rria_api.robot_object import *

# Create Denso RobotObject
denso_robot = RobotObject('192.168.160.226', 'denso')
denso_robot.connect_robot()

denso_robot.motor_on()

denso_robot.move_joints(30.0, 30.0, 30.0, 30.0, 30.0, 30.0)

denso_robot.move_to_home()

denso_robot.safe_disconnect()
```