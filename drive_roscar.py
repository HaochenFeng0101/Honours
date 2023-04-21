#!/usr/bin/env python

import rospy
import time
from ackermann_msgs.msg import AckermannDriveStamped
def car_controller(drive_duration, stop_duration, reverse_duration):
    # Initialize the ROS node
    rospy.init_node('car_controller', anonymous=True)

    # Create a publisher for the /carlie/ackermann_cmd topic
    pub = rospy.Publisher('/carlie/ackermann_cmd', AckermannDriveStamped, queue_size=10)

    # Drive forward for 30 seconds
    drive_forward = AckermannDriveStamped()
    drive_forward.drive.speed = 1.0  # Move forward at 1 m/s
    drive_forward.drive.steering_angle = 0.0  # No steering angle

    for _ in range(int(drive_duration * 10)):  # 10 Hz rate
        pub.publish(drive_forward)
        time.sleep(0.1)

    # Stop for 5 seconds
    stop = AckermannDriveStamped()
    stop.drive.speed = 0.0  # Stop
    stop.drive.steering_angle = 0.0  # No steering angle

    for _ in range(int(stop_duration * 10)):  # 10 Hz rate
        pub.publish(stop)
        time.sleep(0.1)

    # Drive in reverse for 30 seconds
    drive_reverse = AckermannDriveStamped()
    drive_reverse.drive.speed = -1.0  # Move in reverse at 1 m/s
    drive_reverse.drive.steering_angle = 0.0  # No steering angle

    for _ in range(int(reverse_duration * 10)):  # 10 Hz rate
        pub.publish(drive_reverse)
        time.sleep(0.1)

    # Stop the car
    for _ in range(10):  # Publish stop command 10 times to ensure it stops
        pub.publish(stop)
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        drive_duration = 8.0  # Drive forward for 30 seconds
        stop_duration = 5.0  # Stop for 5 seconds
        reverse_duration = 8.0  # Drive in reverse for 30 seconds
        car_controller(drive_duration, stop_duration, reverse_duration)
    except rospy.ROSInterruptException:
        pass
