#!/usr/bin/env python

import rospy
from naoqi import ALProxy

class Robot():
  def __init__(self):
    # Replace the IP and the PORT numbers with the correct values - from a physical or simulated robot
    ip = rospy.get_param('~ip', '127.0.0.1')
    port = int(rospy.get_param('~port', '9559'))
    self.connect(ip,port)
    self.poseInit()
    
  def connect(self,ip,port):
    self.postureProxy = ALProxy("ALRobotPosture", ip, port)
    self.tts = ALProxy("ALTextToSpeech", ip, port)
    self.motionProxy = ALProxy("ALMotion", ip, port)

  def poseZero(self):
    if(self.postureProxy != None):
      result = self.postureProxy.goToPosture("StandZero", 2)
      if not(result):
        assert Exception
    else:
      assert Exception

  def poseInit(self):
    if(self.postureProxy != None):
      result = self.postureProxy.goToPosture("StandInit", 2)
      if not(result):
        assert Exception
    else:
      assert Exception

  def sit(self):
    if(self.postureProxy != None):
      result = self.postureProxy.goToPosture("Sit", 2)
      if not(result):
        assert Exception
    else:
      assert Exception

  def crouch(self):
    if(self.postureProxy != None):
      result = self.postureProxy.goToPosture("Crouch", 2)
      if not(result):
        assert Exception
    else:
      assert Exception
