#!/usr/bin/env python

from robot import Robot
nao_robot = Robot()

from rgoap import Condition, Precondition, Effect, Action, Goal
from rgoap_ros import ROSTopicCondition, ROSTopicAction
import rospy
from std_msgs.msg import String

class ActionStandUp(ROSTopicAction):
  def __init__(self, queue_size=1):
    ROSTopicAction.__init__(
      self, "/nao_rgoap/ActionStandUp", String, 
      [Precondition(Condition.get('robot.pose'), 'init')], 
      [Effect(Condition.get('robot.pose'), 'stand_up')])
  def run(self, next_worldstate):
    nao_robot.poseInit()
  def cost(self):
    return 1
  def check_freeform_context(self):
    return True

class ActionSquat(ROSTopicAction):
  def __init__(self, queue_size=1):
    ROSTopicAction.__init__(
      self, "/nao_rgoap/ActionSquat", String, 
      [Precondition(Condition.get('robot.pose'), 'stand_up')],
      [Effect(Condition.get('robot.squat'), 'ready')])
  def run(self, next_worldstate):
    for i in range(3):
      nao_robot.crouch()
      nao_robot.poseZero()
  def cost(self):
    return 1
  def check_freeform_context(self):
    return True

class ActionSit(ROSTopicAction):
  def __init__(self, queue_size=1):
    ROSTopicAction.__init__(
      self, "/nao_rgoap/ActionStandUp", String, 
      [Precondition(Condition.get('robot.pose'), 'stand_up'),
      Precondition(Condition.get('robot.squat'), 'ready')], 
      [Effect(Condition.get('robot.pose'), 'sit')])
  def run(self, next_worldstate):
    nao_robot.sit()
  def cost(self):
    return 1
  def check_freeform_context(self):
    return True

class GoalReady(Goal):
  def __init__(self):
    Goal.__init__(self, 
      [Precondition(Condition.get('robot.pose'), 'sit'),
      Precondition(Condition.get('robot.squat'), 'ready')], 
      10)

def get_all_conditions(memory):
  return [
      ROSTopicCondition("robot.pose", "/nao_rgoap/pose", String, field='data'),
      ROSTopicCondition("robot.squat", "/nao_rgoap/squat", String, field='data')
    ]

def get_all_actions(memory):
  return [
      ActionStandUp(), 
      ActionSquat(), 
      ActionSit()]

def get_all_goals():
  return [GoalReady()]
