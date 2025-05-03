import sub_data
import cortex
from cortex import Cortex
import serial
import time
import threading
import json


def initialize_live_advance(serial):
    # Credentials
    your_app_client_id = 'eOkUjdmtu8y4WK8n0gGFW4TwpS8h1xvchKb3Xp9g'
    your_app_client_secret = 'lRNYu1TsAB9MmfcD7CqbEIlKbr14pI0cYwDvrgs8b5ZbLUMX2KPS5b1ryds23gIJRC38Cg8Up5N9BTHTK3kiK0W980ZTBqx913hoyeIsKfgoTuTki90x8zQztf3lUT7Z'

    try:
        s = sub_data.Subcribe(your_app_client_id, your_app_client_secret, serial)
        return s
    except Exception as e:
        print(f"Failed to start LiveAdvance. Error: {e}")
        return

def serial_open():
    try:
        port = input("Serial Port: ")
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(0.5)
        return ser
    except Exception as e:
        print(f"Failed to connect to Arduino. Error: {e}")
        return

def read_lidar(s, ser):
    while True:
        line_in_bytes = ''
        try:
            with s.serial_lock:
                line_in_bytes = ser.readline()  # Only lock for the serial read
        except serial.SerialTimeoutException as e:
            print(f"Readline timed out: {e}")
            continue

        if line_in_bytes:
            line_as_string = line_in_bytes.decode().strip()  # Decode and strip the line
            try:
                data = json.loads(line_as_string)  # Process JSON outside the lock
                if "lidar1" in data:
                    s.set_lidar1(data["lidar1"][0])
                    s.set_servo1(data["lidar1"][1])
                if "lidar2" in data:
                    s.set_lidar2(data["lidar2"][0])
                    s.set_servo2(data["lidar2"][1])
            except ValueError as e:
                print(f"Invalid JSON: {e}")

        time.sleep(0.1)
        print(f"lidar1: {s.get_lidar1()} servo1 angle: {s.get_servo1()}")
        print(f"lidar2: {s.get_lidar2()} servo2 angle: {s.get_servo2()}")

def write_command(s, ser):
    while True:
        command = s.get_command()
        if command:
            with s.command_lock:
                ser.write((command + '\n').encode())  # Send command to Arduino
                print(command)
        time.sleep(0.1)

def main():
    ser = serial_open()
    
    if not ser:
        return  # Exit if serial connection fails

    s = initialize_live_advance(ser)
    if not s:
        return  # Exit if LiveAdvance initialization fails

    serial_thread = threading.Thread(target=read_lidar, args=(s, ser))
    command_thread = threading.Thread(target=write_command, args=(s, ser))

    serial_thread.daemon = True
    command_thread.daemon = True

    serial_thread.start()
    command_thread.start()
    
    serial_thread.join()

    
    try:
        profile_name = input("Profile Name: ")
        streams = ['com', 'mot']
        s.start(streams, profile_name=profile_name)
    except Exception as e:
        print(f"Failed to start LiveAdvance. Error: {e}")


if __name__ == '__main__':
    main()
