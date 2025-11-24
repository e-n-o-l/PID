import serial
import time
import functools
import struct
while True:
    try:
        arduino = serial.Serial(input("enter serial port: "), 9600)
        time.sleep(5)
        break
    except serial.SerialException:
        print("serial port error, try another one")

history = []

def send_command(response_lines: int = 1, wait_end: bool = False):
    def dec(command):
        @functools.wraps(command)
        def wrapper() -> None:
            msg = command()
            checksum = ord(msg[0]) ^ msg[1]
            arduino.write(bytes(f'{msg[1]}{msg[0]}{checksum}'.encode()))
            print((msg := f'pc: {command.__name__}'))
            history.append(msg)
            counter, response = 0, ""
            while counter < response_lines or (wait_end and (response != 'ACK' and response != 'NACK')):
                print((response := arduino.readline().decode().strip()))
                history.append(f'arduino: {response}')
                counter += 1
        return wrapper
    return dec

def input_val_check(param: str,min_val: float = -255, max_val: float = 255):
    def dec(func):
        @functools.wraps(func)
        def wrapper():
            while True:
                try:
                    val = float(input(f'enter the {param}: '))
                    if val > max_val or val < min_val:
                        raise ValueError()
                    break
                except ValueError:
                    print(f'invalid {param}, please try again')
            return func(int(struct.unpack('!I', struct.pack('!f', val))[0]))
        return wrapper
    return dec