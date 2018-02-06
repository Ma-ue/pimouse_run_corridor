#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time, sys
from std_msgs.msg import UInt16
from std_srvs.srv import Trigger, TriggerResponse

class WallTraceTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('wall_trace',nodes, "node does not exist")
    
    def set_sensor_values(self,lf,ls,rs,rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf,rs,ls,lf))

    def get_freqs(self):
        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())
        return left, right

    def test_io(self):
        self.set_sensor_values?gc(400,100,100,0) #total: 600
        time.sleep(0.3)
        left, right = self.get_freqs()
        self.assertTrue(left == right == 0, "can't stop")
        
        self.set_sensor_values?gc(0,5,1000,0) #side direction is not a trigger of stop 
        time.sleep(0.3)
        left, right = self.get_freqs()
        self.assertTrue(left == right != 0, "stop wrongly by side sensors")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_trace')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_trace',WallTraceTest)
