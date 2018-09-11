#!/usr/bin/env python
import numpy
import rospy
import mavros
from geometry_msgs.msg import PoseStamped,Vector3
from mavros_msgs.msg import State,AttitudeTarget
from mavros_msgs.srv import CommandBool, SetMode

from std_msgs.msg import Bool,Float32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import tf.transformations
import sys, time
import PID

import timeit

from argparse import ArgumentParser

from pyquaternion import Quaternion

import roslaunch
class test:
	def __init__(self):
		self.vicon_cb_flag = False
		self.state_cb_flag = False

		self.state_pid_reset_flag=False
		self.pid_reset_flag=False

		self.pos_sp_cb_flag = False



		self.P = rospy.get_param('/attitude_thrust_publisher/height_hover_P')
		self.I = rospy.get_param('/attitude_thrust_publisher/height_hover_I')
		self.D = rospy.get_param('/attitude_thrust_publisher/height_hover_D')

		self.height_pid = PID.PID(self.P, self.I, self.D)

		#Rate init
		#DECIDE ON PUBLISHING RATE

		self.rate = rospy.Rate(100.0) # MUST be more then 2Hz
		
		self.height_target_pub = rospy.Publisher("/px4_quad_controllers/thrust_setpoint", PoseStamped, queue_size=10)

		#ADD SUBSCRIBER FOR VICON DATA
		vicon_sub = rospy.Subscriber("/intel_aero_quad/odom", Odometry, self.vicon_sub_callback)

		state_sub = rospy.Subscriber("/mavros/state", State, self.state_subscriber_callback)

		while not rospy.is_shutdown():
		
			if(self.vicon_cb_flag==True and self.state_cb_flag==True):
				#Update PID
				self.P = rospy.get_param('/attitude_thrust_publisher/height_hover_P')
				self.I = rospy.get_param('/attitude_thrust_publisher/height_hover_I')
				self.D = rospy.get_param('/attitude_thrust_publisher/height_hover_D')
				self.height_pid.setKp(self.P)
				self.height_pid.setKi(self.I)
				self.height_pid.setKd(self.D)
				#Update setpoint
				if(self.pos_sp_cb_flag==False):
					self.height_sp = rospy.get_param('/attitude_thrust_publisher/height_sp')
				else:
					self.height_sp = self.pos_sp_z				

				self.height_pid.SetPoint = self.height_sp
				
				if(self.current_state=='OFFBOARD'):
					if(self.pid_reset_flag==False):
						self.height_pid.clear()
						self.pid_reset_flag=True
					self.height_pid.update(self.vicon_height)
				else:
					self.pid_reset_flag=False
					self.state_pid_reset_flag=False
				#For this to work, we have to align x,y of quad and vicon

				self.hover_thrust = rospy.get_param('/attitude_thrust_publisher/hover_thrust')
				
				thrust_output = self.height_pid.output+self.hover_thrust
				target_thrust = PoseStamped()
				target_thrust.header.frame_id = "home"
				target_thrust.header.stamp = rospy.Time.now()

				self.min_thrust = rospy.get_param('/attitude_thrust_publisher/min_thrust')
				self.max_thrust = rospy.get_param('/attitude_thrust_publisher/max_thrust')

				#Thrust threshold
				if(thrust_output<=self.max_thrust and thrust_output>=self.min_thrust):
					target_thrust.pose.position.x = thrust_output
				elif(thrust_output>self.max_thrust):
					target_thrust.pose.position.x = self.max_thrust
				elif(thrust_output<self.min_thrust):
					target_thrust.pose.position.x = self.min_thrust
				else:
					print("HEIGHT CONTROLLER ERROR!")
					target_thrust.pose.position.x = self.min_thrust
				self.height_target_pub.publish(target_thrust)

			self.rate.sleep()

	def vicon_sub_callback(self,state):
		self.vicon_height = state.pose.pose.position.z
		self.vicon_cb_flag = True

		self.rate = rospy.Rate(20.0) # MUST be more then 2Hz
		
		self.height_target_pub = rospy.Publisher("/px4_quad_controllers/thrust_setpoint", PoseStamped, queue_size=10)

		#ADD SUBSCRIBER FOR VICON DATA
		vicon_sub = rospy.Subscriber("/intel_aero_quad/odom", Odometry, self.vicon_sub_callback)

		state_sub = rospy.Subscriber("/mavros/state", State, self.state_subscriber_callback)

		pos_sp_sub = rospy.Subscriber("/px4_quad_controllers/pos_sp", PoseStamped, self.pos_sp_subscriber_callback)

	def vicon_sub_callback(self,state):
		self.vicon_height = state.pose.pose.position.z
		self.vicon_cb_flag = True


	#Current state subscriber
	def state_subscriber_callback(self,state):
		self.current_state = state.mode
		self.state_cb_flag = True

		if(self.current_state!='OFFBOARD' and self.state_pid_reset_flag==False):
			self.height_pid.clear()
			self.state_pid_reset_flag=True


	def pos_sp_subscriber_callback(self,state):
		self.pos_sp_z = state.pose.position.z
		self.pos_sp_cb_flag = True


		self.rate.sleep()
def main(args):
	rospy.init_node('offb_node', anonymous=True)
	ic=test()

	try:
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
	main(sys.argv)
