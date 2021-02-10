#    Name: Omkar Bhoite (Neuro Computing Systems)
#    Email ID: omkarbhoite97@gmail.com
###########################################################################################################################################
import time
from dynamixel_sdk import *             #Library provided by the Dynamixel.
from ControlMX28 import *               #Importing Control.py file containing the addresses and ID for the motor
from Setup import *
############################################################################################################################################


##############################################################################################################################################

'''
ping function
    inputs: We provide with motor id and the portHandler
    outputs: We receive the Model Number of the motor.
'''

def ping():
    while 1:
        motor_id, ping_result, ping_error = packetHandler.ping(portHandler, MOTOR_ID)
        if ping_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(ping_result))
        elif ping_error != 0:
            print("%s" % packetHandler.getRxPacketError(ping_error))
        else:
            print("[ID:%03d] Ping Succeeded. Dynamixel model number : %d" % (MOTOR_ID, motor_id))
            return


'''
start function
    working: When this function is called it makes sure that the motor is back to the zeroth position (Meaning 0 degree angle) 
'''

def start():
    motor_run, motor_run_error = packetHandler.write2ByteTxRx(portHandler, MOTOR_ID, ADDRESS_MX_28_GOAL_POSITION, 0)
    return motor_run, motor_run_error, print()

'''
stop function
    working: When this function is called then when we press the ESC key we terminate the program.
'''
def stop():
    while 1:
        if getch() == chr(0x1b):
            break
        return print('Break')

'''
input_position function
    input: We provide with the position value to which one wants the motor to go.
    output: The motor is moved to the desired position
'''
def input_position(Position):
    motor_run, motor_run_error = packetHandler.write2ByteTxRx(portHandler, MOTOR_ID, ADDRESS_MX_28_GOAL_POSITION, Position)
    return motor_run, motor_run_error, print('Position',Position)

'''
gui_input function
    input: The user provide the desired position value.
    output: the valu of position is passed into the input_position function.
'''

def gui_input():
    Position = int(input('Enter value between 0 to 4095 to rotate the servo motor: ',))
    input_position(Position)

'''
read_position function
    working: When this function is called we can read the current position of the motor.
'''

def read_position():
    while 1:
        Current_position, communication_result, read_position_error = packetHandler.read4ByteTxRx(portHandler, MOTOR_ID, ADDRESS_MX_28_PRESENT_POSITION)
        if communication_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(communication_result))
        elif read_position_error != 0:
            print("%s" % packetHandler.getRxPacketError(read_position_error))
        print("[ID:%03d]  PresPos:%03d" % (MOTOR_ID,  Current_position))
        return

'''
torque function
    working: It is used to enable and disable the torque of the motor
'''


def torque(data):
    print(data)
    motor_torque_enable, motor_torque_enable_error = packetHandler.write1ByteTxRx(portHandler, MOTOR_ID, ADDRESS_MX_28_TORQUE_ENABLE, data)
    if motor_torque_enable != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(motor_torque_enable))
    elif motor_torque_enable_error != 0:
        print("%s" % packetHandler.getRxPacketError(motor_torque_enable_error))
    else:
        print("Dynamixel has been successfully connected")
    return

'''
gui_torque_input function 
    woring: To get the user input for enabling or disabling the torque for the motor, and then the value is passed to the torque() function to do so.
'''


def gui_torque_input():
    data = int(input('Enter 1 to enable and 0 to disable the torque: ',))
    torque(data)

##############################################################################################################################################



##############################################################################################################################################
if __name__=="main":
    ping()
    start()
    stop()
    input_position(10)
    gui_input()
    read_position()


