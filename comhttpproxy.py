from serial import Serial, SerialException
import base64
import time
from threading import Thread, Lock
import signal
import sys
import requests

com_name = 'COM1'
api_for_new_data = 'http://62.109.9.21:80/new_data'
api_for_new_command = 'http://62.109.9.21:80/get_command'


def signal_handler(sig, frame):
    global stop_thread
    print('You pressed Ctrl+C!')
    stop_thread = True
    sys.exit(0)

def get_data_from_com():
    data = ser.readline()
    print('Got \'{str}\' from {com}'.format(str=data, com=com_name))
    return data

def send_data_to_server(data):
    try:
        r = requests.post(url=api_for_new_data, data=data)
        print(r)	
    except Exception as _exception:
        print(f'Connection to server error: {_exception}')

def check_command_from_server():
    try:
        r = requests.get(url=api_for_new_command)
        if r.status_code == 200:
            return r.content
        return ''
    except Exception as _exception:
        print(f'Connection to server error: {_exception}')

def send_command_to_com(command):
    ser.write(command)

def connect_to_com():
    try:
        global ser
        ser = Serial(com_name, timeout=10)
        return True
    except SerialException as _exception:
        print(f'Connection to COM error: {_exception}')
        time.sleep(3)
        return False
    return False


def listen_thread():
    global stop_thread
    while True:
        try:
            data = get_data_from_com()
            if data and len(data) != 0:
                send_data_to_server(data)
        except SerialException as _exception:
            connect_to_com()
        finally:
            if stop_thread: 
                break

if __name__ == '__main__':
    connected = False
    while not connected:
        connected = connect_to_com()

    stop_thread = False

    t = Thread(target = listen_thread, args = ())
    t.start()
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        command = check_command_from_server()
        if command and len(command) != 0:
            print('Got \'{cmd}\' command'.format(cmd=command))
            send_command_to_com(command)
        time.sleep(5)
