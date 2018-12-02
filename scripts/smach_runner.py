#!/usr/bin/env python

import rospy
import smach
import smach_ros

from robot import Robot

class POSE_ZERO(smach.State):
  def __init__(self, robot):
    smach.State.__init__(self, outcomes=['outcome1', 'outcome2'])
    self.robot = robot
    self.counter = 0

  def execute(self, userdata):
    rospy.loginfo('Executing "zero" pose')
    self.robot.poseZero()
    if self.counter < 3:
      self.counter += 1
      return 'outcome1'
    else:
      return 'outcome2'

class POSE_CROUCH(smach.State):
  def __init__(self, robot):
    smach.State.__init__(self, outcomes=['outcome1'])
    self.robot = robot

  def execute(self, userdata):
    rospy.loginfo('Executing "crouch" pose')
    self.robot.crouch()
    return 'outcome1'

class SIT_POSE(smach.State):
  def __init__(self, robot):
    smach.State.__init__(self, outcomes=['outcome1'])
    self.robot = robot

  def execute(self, userdata):
    rospy.loginfo('Executing "sit" pose')
    self.robot.sit()
    return 'outcome1'

def main():
  NAO = Robot()
  rospy.init_node('nao_instance')
  sm = smach.StateMachine(outcomes=['outcome'])  

  with sm:
    smach.StateMachine.add('POSE_ZERO', POSE_ZERO(NAO),
                transitions={'outcome2': 'SIT_POSE', 'outcome1': 'POSE_CROUCH'} )
    smach.StateMachine.add('POSE_CROUCH', POSE_CROUCH(NAO),
                transitions={'outcome1': 'POSE_ZERO'} )
    smach.StateMachine.add('SIT_POSE', SIT_POSE(NAO),
                transitions={'outcome1': 'outcome'} )

  # Create and start the introspection server
  sis = smach_ros.IntrospectionServer('nao_server', sm, '/SM_ROOT')
  sis.start()
  
  outcome = sm.execute() # Execute the state machine
  rospy.spin() # Wait for ctrl-c to stop the application
  sis.stop()

if __name__ == '__main__':
  main()