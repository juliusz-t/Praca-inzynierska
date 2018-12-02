#!/usr/bin/env python

import rgoap_agent

import time
import rospy
from std_msgs.msg import String

from rgoap_ros import SMACHRunner
from rgoap import Runner, WorldState, Condition

def tasker():
  rospy.init_node('nao_rgoap')
  runner = Runner(rgoap_agent)

  rospy.sleep(1) 
  pub_pose = rospy.Publisher('/nao_rgoap/pose', String, latch=True, queue_size = 1)
  pub_squat = rospy.Publisher('/nao_rgoap/squat', String, latch=True, queue_size = 1)

  rospy.sleep(1) 
  pub_pose.publish('init')
  pub_squat.publish('not_ready')

  rospy.sleep(1) 
  print "\33[32m[INFO] [WallTime: %s] Try to plan and to execute goals \033[0m" % time.time()
  runner.plan_and_execute_goals(rgoap_agent.get_all_goals())

tasker()