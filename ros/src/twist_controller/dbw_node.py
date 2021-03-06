#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from dbw_mkz_msgs.msg import ThrottleCmd, SteeringCmd, BrakeCmd, SteeringReport
from geometry_msgs.msg import TwistStamped
import math

from twist_controller import Controller

class DBWNode(object):
    def __init__(self):
        rospy.init_node('dbw_node')

        # Vehicle properties params
        vehicle_mass = rospy.get_param('~vehicle_mass', 1736.35)
        #fuel_capacity = rospy.get_param('~fuel_capacity', 13.5)
        #brake_deadband = rospy.get_param('~brake_deadband', .1)
        decel_limit = rospy.get_param('~decel_limit', -5)
        accel_limit = rospy.get_param('~accel_limit', 1.)
        wheel_radius = rospy.get_param('~wheel_radius', 0.2413)
        wheel_base = rospy.get_param('~wheel_base', 2.8498)
        steer_ratio = rospy.get_param('~steer_ratio', 14.8)
        max_lat_accel = rospy.get_param('~max_lat_accel', 3.)
        max_steer_angle = rospy.get_param('~max_steer_angle', 8.)

        # Subscribers
        self.velocity_sub = rospy.Subscriber('/current_velocity', TwistStamped, self.velocity_cb)
        self.dbw_enabled_sub = rospy.Subscriber('/vehicle/dbw_enabled', Bool, self.dbw_enabled_cb)
        self.twist_cmd_sub = rospy.Subscriber('/twist_cmd', TwistStamped, self.twist_cb)

        # Publishers
        self.steer_pub = rospy.Publisher('/vehicle/steering_cmd',
                                         SteeringCmd, queue_size=1)
        self.throttle_pub = rospy.Publisher('/vehicle/throttle_cmd',
                                            ThrottleCmd, queue_size=1)
        self.brake_pub = rospy.Publisher('/vehicle/brake_cmd',
                                         BrakeCmd, queue_size=1)

        # DBW Node variables
        self.current_velocity = None
        self.dbw_enabled = None
        self.target_linear_velocity = None
        self.target_angular_velocity = None
        self.throttle_cmd = None
        self.brake_cmd = None
        self.steer_cmd = None
        self.controller = Controller(vehicle_mass=vehicle_mass,
                                     decel_limit=decel_limit,
                                     accel_limit=accel_limit,
                                     wheel_radius=wheel_radius,
                                     wheel_base=wheel_base,
                                     steer_ratio=steer_ratio,
                                     max_lat_accel=max_lat_accel,
                                     max_steer_angle=max_steer_angle)

        self.step()

    def step(self):
        rate = rospy.Rate(50) # 50Hz
        while not rospy.is_shutdown():
            if not None in (self.current_velocity, self.dbw_enabled, self.target_linear_velocity, self.target_angular_velocity):
                self.throttle_cmd, self.brake_cmd, self.steer_cmd = self.controller.control(self.dbw_enabled,
                                                                                self.current_velocity,
                                                                                self.target_linear_velocity,
                                                                                self.target_angular_velocity)
                #rospy.loginfo('Current throttle cmd =  %s', self.throttle_cmd)
                #rospy.loginfo('Current brake cmd =  %s', self.brake_cmd)
                #rospy.loginfo('Current steer cmd =  %s', self.steer_cmd)
            if self.dbw_enabled:
                self.publish(self.throttle_cmd, self.brake_cmd, self.steer_cmd)
            rate.sleep()

    '''
    This method updates the current ego vehicle velocity
    '''
    def velocity_cb(self, data):
        self.current_velocity = data.twist.linear.x

    '''
    This method updates the dbw enabled status
    '''
    def dbw_enabled_cb(self, data):
        self.dbw_enabled = data

    '''
    This method updates the target velocity
    '''
    def twist_cb(self, data):
        self.target_linear_velocity = data.twist.linear.x
        self.target_angular_velocity = data.twist.angular.z
        #rospy.loginfo('Target linear vel %s', self.target_linear_velocity)
        #rospy.loginfo('Target angular vel %s', self.target_angular_velocity)

    def publish(self, throttle, brake, steer):
        tcmd = ThrottleCmd()
        tcmd.enable = True
        tcmd.pedal_cmd_type = ThrottleCmd.CMD_PERCENT
        tcmd.pedal_cmd = throttle
        self.throttle_pub.publish(tcmd)

        scmd = SteeringCmd()
        scmd.enable = True
        scmd.steering_wheel_angle_cmd = steer
        self.steer_pub.publish(scmd)

        bcmd = BrakeCmd()
        bcmd.enable = True
        bcmd.pedal_cmd_type = BrakeCmd.CMD_TORQUE
        bcmd.pedal_cmd = brake
        self.brake_pub.publish(bcmd)


if __name__ == '__main__':
    DBWNode()
