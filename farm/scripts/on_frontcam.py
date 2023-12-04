#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class frontcam_data:

    def __init__(self):
        sub_topic_name ="/agribot/front_camera/image_raw"
        self.number_subscriber = rospy.Subscriber(sub_topic_name, Image, self.camera_callback)
        #self.out = cv2.VideoWriter('/root/project_ws/output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (300,250))
        self.bridge = CvBridge()

    def camera_callback(self, data):
        frame = self.bridge.imgmsg_to_cv2(data)

        # Resize the color frame to 300x250
        resized_frame = cv2.resize(frame, (300, 250))

        # Convert the resized frame to grayscale
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

	

        # Apply adaptive thresholding to highlight objects
        _, thresh = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
        
        thresh = cv2.bitwise_not(thresh)

        # Convert the thresholded image to a 3-channel image
        thresh_colored = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        # Darken the background by subtracting the thresholded image from the original frame
        result = cv2.subtract(gray_frame,thresh)	

        # Display the resized color frame
        cv2.imshow('Original Frame', resized_frame)

        # Display the grayscale frame
        cv2.imshow('Grayscale Frame', result)

        cv2.waitKey(100)
 	


if __name__ == '__main__':
    node_name ="sensor_front_cam"
    rospy.init_node(node_name)
    frontcam_data()
    rospy.spin()
