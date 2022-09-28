from abc import ABC, abstractmethod
from typing import Callable
from functools import partial
import RPi.GPIO as GPIO

class InputPin(ABC):
  """Abstraction around a basic GPIO pin + controller"""
  pin: int
  event_listener: Callable

  def __init__(self, pin: int, listener: Callable):
    self.pin = pin
    self.event_listener = listener

  @abstractmethod
  def setup(self):
    pass
  
  @abstractmethod
  def listen(self):
    pass

  @abstractmethod
  def getState(self):
    pass


class Button(InputPin):
  def setup(self):
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  def listen(self):
    GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=partial(self.event_listener, self), bouncetime=20)
  def getState(self):
    return {
        "type": "button",
        "data": "pressed" if GPIO.input(self.pin) else "unpressed"
    }

class Switch(InputPin):
  def setup(self):
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  def listen(self):
    GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=partial(self.event_listener, self), bouncetime=20)
  def getState(self):
    return {
        "type": "switch",
        "data": "on" if GPIO.input(self.pin) else "off"
    }

class JoystickPressPin(InputPin):
  def setup(self):
    GPIO.setup(self.pin, GPIO.IN)
  def listen(self):
    GPIO.add_event_detect(self.pin, GPIO.RISING, callback=partial(self.event_listener, self), bouncetime=20)
  def getState(self):
    pass

class JoystickAxisPin(InputPin):
  def setup(self):
    GPIO.setup(self.pin, GPIO.IN)
  def listen(self):
    GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=partial(self.event_listener, self), bouncetime=20)
  def getState(self):
    pass

class Joystick(InputPin):
  pin_xaxis: JoystickAxisPin
  pin_yaxis: JoystickAxisPin
  pin_press: JoystickPressPin

  only_axes: bool = False

  def __init__(self, pin_xaxis: int, pin_yaxis: int, pin_press: int, listener: Callable):
    self.pin_xaxis = JoystickAxisPin(pin_xaxis, partial(listener, self))
    self.pin_yaxis = JoystickAxisPin(pin_yaxis, partial(listener, self))
    self.pin_press = JoystickPressPin(pin_press, partial(listener, self))
    self.pin = None

  def setup(self):
    self.pin_xaxis.setup()
    self.pin_yaxis.setup()
    self.pin_press.setup()

  def listen(self):
    self.pin_xaxis.listen()
    self.pin_yaxis.listen()
    if not self.only_axes:
      self.pin_press.listen()
  
  def getState(self):
    state = {
      "x": GPIO.input(self.pin_xaxis.pin),
      "y": GPIO.input(self.pin_yaxis.pin)
    }
    if not self.only_axes:
      state["press"] = GPIO.input(self.pin_press.pin)
    return {
        "type": "joystick",
        "data": state
    }
