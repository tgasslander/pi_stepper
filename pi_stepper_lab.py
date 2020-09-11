######################################
##
## File: pi_stepper_lab.py
##
## Desc: Raspberry Pi Stepper Motor lab
##
##
## License Apache 2.0
## Use any way you like
##
#####################################

import RPi.GPIO as GPIO
import time
from os import system, name 

GPIO.setmode(GPIO.BOARD)

# Empirical defaults
step_delay = 0.001
min_step_delay = 0.001

# Note: Update to fit your cable connections
control_pins = [7,11,13,15]

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

# Set the angle relative to your current position 
def set_relative_angle(angle):
  step_array = halfstep_seq
  steps = (512 * angle) / 360 
  print("steps to move " + str(steps))
  if angle < 0:
    step_array = halfstep_seq[::-1]
    steps = -steps
  for i in range(steps):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], step_array[halfstep][pin])
      time.sleep(step_delay)

# Tidy the screen
def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")

# Menu
def usage():
  clear()
  print("PiStepperLab v0.0.1")
  menu =  "-----------------------------------\n\r"
  menu += "current step delay: " + str(step_delay) + "\n\r"
  menu += "\n\r"
  menu += "a\t- set arbitrary angle\n\r" 
  menu += "t\t- run 15, 90 and back\n\r"
  menu += "tc\t- run firstAngle, secondAngle-firstAngle and back\n\r"
  menu += "q\t- quit"
  menu += "\n\r\n\r"
  menu += "settings:\n\r"
  menu += "s\t- speed\n\r"
  return menu

# Menu handler
def menu():
  global step_delay
  print(usage())
  choice = raw_input("choice: ")
  if choice == "a":
    arbitrary_angle()
  elif choice == "t":
    run_sequence(15, 90)
  elif choice == "q":
    GPIO.cleanup()
    exit(0)
  elif choice == "tc":
    run_sequence(input("firstAngle angle: "), input("secondAngle angle: "))
  elif choice == "s":
    set_step_delay()
    menu()
  else:
    print("nonexistent menu item")
    d = raw_input("enter to continue")
    menu()

# Handle step delay input
def set_step_delay():
  global step_delay
  global min_step_delay
  delay = input("step delay (default: 0.001, current: " + str(step_delay) + "): ")
  if delay < min_step_delay:
    print("cannot use smaller delay than 0.001")
    _ = raw_input("enter to continue")
    menu()
  step_delay = delay 

# Set an arbitrary angle to move to
def arbitrary_angle():
  angle = input("angle: ")
  set_relative_angle(angle)
  print("done")
  menu()

# Run a pre-defined sequence
def run_sequence(firstAngle, secondAngle):
  if abs(secondAngle) <= abs(firstAngle):
    print("illegal angles. secondAngle must be > firstAngle")
    d = raw_input("enter to continue")
    menu() 
  set_relative_angle(firstAngle)
  print("firstAngle at", firstAngle, " degrees")
  time.sleep(3)
  set_relative_angle(secondAngle-firstAngle)
  print("secondAngle at", secondAngle, " degrees")
  time.sleep(3)
  print("returning with", -secondAngle, "degrees")
  set_relative_angle(-secondAngle)
  print("done")
  menu()

while(1):
  print("pi stepper v0.0.1")
  menu()

GPIO.cleanup()
