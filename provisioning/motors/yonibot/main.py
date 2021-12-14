from flask import Flask, render_template
from flask import request
import datetime
import RPi.GPIO as GPIO
import sys
import os
from threading import Thread
from time import sleep

app = Flask(__name__)
print = app.logger.info

MotorLA = 32
MotorLB = 36
MotorLE = 38

MotorRA = 23
MotorRB = 21
MotorRE = 19

pR = None
pL = None

def setup_motors():
  GPIO.cleanup()
  sleep(0.5)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(MotorRA,GPIO.OUT)
  GPIO.setup(MotorRB,GPIO.OUT)
  GPIO.setup(MotorRE,GPIO.OUT)
  GPIO.setup(MotorLA,GPIO.OUT)
  GPIO.setup(MotorLB,GPIO.OUT)
  GPIO.setup(MotorLE,GPIO.OUT)
  global pR
  pR = GPIO.PWM(MotorRE, 50)
  global pL
  pL = GPIO.PWM(MotorLE, 50)

@app.route("/motors_tank")
def motors_tank():
  try:
    leftMotorPower = int(request.args.get('lmp'))
    rightMotorPower = int(request.args.get('rmp'))

    print("left: " + str(leftMotorPower) + " right: " + str(rightMotorPower))

    if rightMotorPower > 0:
      print(f'turning on {MotorRA}')
      GPIO.output(MotorRA,GPIO.HIGH)
      GPIO.output(MotorRB,GPIO.LOW)

    if rightMotorPower < 0:
      print(f'turning on {MotorRB}')
      GPIO.output(MotorRA,GPIO.LOW)
      GPIO.output(MotorRB,GPIO.HIGH)

    if leftMotorPower > 0:
      print(f'turning on {MotorLA}')
      GPIO.output(MotorLA,GPIO.HIGH)
      GPIO.output(MotorLB,GPIO.LOW)

    if leftMotorPower < 0:
      print(f'turning on {MotorLB}')
      GPIO.output(MotorLA,GPIO.LOW)
      GPIO.output(MotorLB,GPIO.HIGH)


    pR.start(abs(rightMotorPower))
    pL.start(abs(leftMotorPower))
    
    sleep(1)    
    print('states:')
    print(f'left motor A ({MotorLA}): {GPIO.input(MotorLA)}')
    print(f'left motor B ({MotorLB}): {GPIO.input(MotorLB)}')
    print(f'right motor A ({MotorRA}): {GPIO.input(MotorRA)}')
    print(f'right motor B ({MotorRB}): {GPIO.input(MotorRB)}')
    print(f'Right PWM state ({ MotorRE }) is {GPIO.input(MotorRE)}')
    print(f'Left PWM state ({ MotorLE }) is {GPIO.input(MotorLE)}')

    return 'OK'

  except Exception as e: 
    print(e)
    return "ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route("/motors_stop")
def motors_stop():
  try:
    print("Now stop")
    pR.stop()
    pL.stop()

    return 'OK'

  except Exception as e:
    print(e)
    return "ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route("/hard_reset")
def hard_reset():
  # suicide. hopefully the supervisor will restart me..
  os.system("killall -KILL python")

@app.route("/")
def hello():
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")
  templateData = {
    'title' : 'HELLO!',
    'time': timeString
  }
  setup_motors()
  return render_template('main.html', **templateData)

if __name__ == "__main__":
  setup_motors()
  app.run(host='0.0.0.0', port=3232)
