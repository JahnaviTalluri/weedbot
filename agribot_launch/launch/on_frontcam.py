#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class frontcam_data:

    def __init__(self):
        sub_topic_name ="/agribot/front_camera/image_raw"
        self.number_subscriber = rospy.Subscriber(sub_topic_name, Image, self.camera_callback)
        self.out = cv2.VideoWriter('/root/project_ws', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
        self.bridge = CvBridge()

    def camera_callback(self, data):
        frame = self.bridge.imgmsg_to_cv2(data)
        self.out.write(frame)
        cv2.imshow('output', frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    node_name ="sensor_front_cam"
    rospy.init_node(node_name)
    frontcam_data()
    rospy.spin()
