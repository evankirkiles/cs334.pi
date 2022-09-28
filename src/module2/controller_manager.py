from abc import ABC
import time
import RPi.GPIO as GPIO
from input_types import InputPin
from socket_manager import SocketManager

class ControllerManager():

  # pin numbers for analog input
  pins: list[InputPin]

  def __init__(self, pins: list[InputPin]):
    """Listens for input on the specified pins"""
    self.pins = pins
    self.setup()
  
  def setup(self):
    """Sets up listeners on the pins"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in self.pins:
      pin.setup()
  
  def getAllStates(self):
    state = {
      "type": "state"
    }
    for pin_state in [pin.getState() for pin in self.pins]:
      state[pin_state["type"]] = pin_state["data"]
    return state
  
  def run(self):
    """Begins the input manager script"""

    # attach event listener to pins
    for pin in self.pins:
      pin.listen()

    # stall until user quits
    input("Press enter to quit\n\n")
    GPIO.cleanup()