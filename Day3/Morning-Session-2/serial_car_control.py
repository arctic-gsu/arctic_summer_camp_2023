import serial
import json
from time import sleep
from typing import Union, List


class SerialController:
    def __init__(
        self,
        com_port: str,
        baudrate: int,
        timeout: int,
        default_speed: int,
    ):
        self.ser = serial.Serial(com_port, baudrate, timeout=timeout)

        self.default_speed = default_speed
        self.ser.readlines()

    def close_connection(self):
        self.stop()
        self.ser.close()

    def stop(self):
        payload = self.__build_payload(100)
        self.ser.write(payload)
        self.ser.readline()

    def get_yaw(self) -> float:
        payload = self.__build_payload(120)
        if self.ser.in_waiting > 0:
            self.ser.readall()
        self.ser.write(payload)
        try:
            return float(self.ser.readline())
        except ValueError:
            return None

    def set_left_and_right(self, left: int, right: int):
        payload = self.__build_payload(4, [right, left])
        self.ser.write(payload)
        self.ser.readline()

    def forward(self, time: Union[float, None] = None, speed: Union[int, None] = None):
        self.__movement(1, time, speed)

    def back(self, time: Union[float, None] = None, speed: Union[int, None] = None):
        self.__movement(2, time, speed)

    def turn_left(
        self, time: Union[float, None] = None, speed: Union[int, None] = None
    ):
        self.__movement(3, time, speed)

    def turn_right(
        self, time: Union[float, None] = None, speed: Union[int, None] = None
    ):
        self.__movement(4, time, speed)

    def left_front(
        self, time: Union[float, None] = None, speed: Union[int, None] = None
    ):
        self.__movement(5, time, speed)

    def rear_left(
        self, time: Union[float, None] = None, speed: Union[int, None] = None
    ):
        self.__movement(6, time, speed)

    def right_front(
        self, time: Union[float, None] = None, speed: Union[int, None] = None
    ):
        self.__movement(7, time, speed)

    def rear_right(self, time: Union[float, int, None], speed: Union[int, None] = None):
        self.__movement(8, time, speed)

    def __movement(
        self,
        direction: int,
        time: Union[float, None] = None,
        speed: Union[int, None] = None,
    ):
        if not speed:
            speed = self.default_speed
        payload = self.__build_payload(102, [direction, speed])
        self.ser.write(payload)
        self.ser.readline()
        if time:
            sleep(time)
            self.stop()

    def __build_payload(
        self, input_type: int, parameters: Union[List[int], None] = None
    ):
        payload = {"N": input_type}
        if parameters:
            for index, parameter in enumerate(parameters, start=1):
                payload["D" + str(index)] = parameter

        return json.dumps(payload).encode("ascii")
