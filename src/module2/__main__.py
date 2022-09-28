from controller_manager import ControllerManager
from input_types import Button, InputPin, Joystick, Switch
import time
import RPi.GPIO as GPIO
from socket_manager import SocketManager
import json

# initialize input manager with pins
sm = SocketManager("ws://10.0.0.165:3000/")

def handler_button(self: InputPin, channel):
    """Handler for button input"""
    time.sleep(0.01) # pause a bit to get rid of jitter (10ms)
    state = self.getState()
    sm.send(state)
button = Button(15, handler_button)

def handler_switch(self, channel):
    """Handler for switch input"""
    time.sleep(0.01) # pause a bit to get rid of jitter (10ms)
    state = self.getState()
    sm.send(state)
switch = Switch(16, handler_switch)

def handler_joystick(self, joystickSelf, channel):
    """Handler for joystick input"""
    state = self.getState()
    sm.send(state)
joystick = Joystick(29,31,33,handler_joystick)
joystick.only_axes = True

# build the input manager
im = ControllerManager([button, switch, joystick])

if __name__ == "__main__":
    #  listen on the websocket until we quit
    sm.connect()
    sm.send(im.getAllStates())
    im.run()
    sm.close()