import serial
import keyboard  
import time

ser = serial.Serial('com4', 115200)


commands = {
    'up': 'f',
    'down': 'b',
    'left': 'l',
    'right': 'r',
    'space': 's'
}

try:
    print("Use arrow keys to control the Arduino. Press 'Esc' to exit.")
    while True:
        prev = 'space'
        for key, command in commands.items():
            if keyboard.is_pressed(key):
                if prev != key:
                    ser.write(('s' + '\n').encode())  # Send command to Arduino
                    prev = key
                
                ser.write((command + '\n').encode())  # Send command to Arduino
                
                print(f'Sent command: {command}')
                
        time.sleep(0.01)
           
                
        # Exit the loop if 'Esc' is pressed
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break

finally:
    ser.close()  # Close the serial connection
