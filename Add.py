#    Name: Omkar Bhoite (Neuro Computing Systems)
#    Email ID: omkarbhoite97@gmail.com
###########################################################################################################################################
ADDRESS_MX_28_TORQUE_ENABLE      = 24                   # Control table address is different in Dynamixel model
ADDRESS_MX_28_GOAL_POSITION      = 30
ADDRESS_MX_28_PRESENT_POSITION   = 36

# Protocol version
PROTOCOL_VERSION                 = 1.0                  # See which protocol version is used in the Dynamixel

# Default setting
MOTOR_ID                         = 1                    # Dynamixel ID : 1
BAUDRATE                         = 57600                  # Dynamixel default baudrate : 57600
DEVICENAME                       = '/dev/ttyUSB0'       # For Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE                    = 1                    # Value for enabling the torque
TORQUE_DISABLE                   = 0                    # Value for disabling the torque
MIN_POS_VALUE                    = 0                    # Dynamixel will rotate between this value
MAX_POS_VALUE                    = 4095        # Enter the Value  
MOVING_STATUS_THRESHOLD          = 0                    # Dynamixel moving status threshold

