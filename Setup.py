#    Name: Omkar Bhoite (Neuro Computing Systems)
#    Email ID: omkarbhoite97@gmail.com
###########################################################################################################################################
import os
from ControlMX28 import *                   
from dynamixel_sdk import *             #Library provided by the Dynamixel.


if os.name == 'nt':                     #"nt" if you're using windows and posix for mac
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

portHandler = PortHandler(DEVICENAME) 
packetHandler = PacketHandler(PROTOCOL_VERSION) #The protocol version 
if portHandler.openPort():
    print("Communication successful")
else:
    print("Communication failed. \n Press any key to terminate................")
    getch()                             #User Input, but not displayed on the screen             
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate Accepted") 
else:
    print("Baudrate Not Accepted. \n Press any key to terminate.............")
    getch()                             #User Input, but not displayed on the screen
    quit()

# To Enable the torque for the Motor so that it can be moved as per the users choice.
# communication_result, error = packetHandler.write1ByteTxRx(portHandler, MOTOR_ID, ADDRESS_MX_28_TORQUE_ENABLE, TORQUE_ENABLE)
# print('communication',communication_result)
# print('error',error)
# if communication_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(communication_result))
#     print('communication_result',communication_result)
# elif error != 0:
#     print("%s" % packetHandler.getRxPacketError(error))
#     print('error',error)
# else:
#     print("Dynamixel has been successfully connected to the PC")