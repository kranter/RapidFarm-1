from serial import Serial
from struct import pack, unpack

def send_command_to_com(command):
    with Serial('COM2', timeout=1) as ser:
        ser.write(command)

def get_data_from_com():
    with Serial('COM2', timeout=10) as ser:
        data = ser.readlines()
        print(data)
        return data


send_command_to_com(bytes('i changed some occurenced '.encode('utf-8')))
print(get_data_from_com())
