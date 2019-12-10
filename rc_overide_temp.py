#!/usr/bin/env python2
'''
TODO: 
1. Channel Min and Max read
2. Takeoff and Land
3. Autonomous Mode reading a switch
4. Read Odom?
5. Read Alt
6. Battery monitoring

'''

import sys
import rospy
import math
from mavros_msgs.msg import OverrideRCIn,RCIn

class rc_pub:
	def __init__(self):
		self.rate = rospy.Rate(50.0)  # MUST be more then 20Hz
		self.rcPub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size = 10)
		self.rcMsg = OverrideRCIn()

	def pubrcmg(self, channels):
		while not rospy.is_shutdown():
			self.rcMsg.channels = channels # [1500,0,0,0,0,0,0,0]
			self.rcPub.publish(self.rcMsg)
			self.rate.sleep()
	
	def takeoff(self):
		# PUB CHANNEL [2000,0,0,0,0,0,0,0]
		# wait 3 s
		# PUB CHANNEL [1000,0,0,0,0,0,0,0]

def main(args):
	rospy.init_node('rc_pub', anonymous=True)
	ic = rc_pub()
	ic.pubrcmg()

	try:
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
	main(sys.argv)
