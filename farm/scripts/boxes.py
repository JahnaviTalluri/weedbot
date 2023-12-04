import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class frontcam_data:
    def __init__(self):
        sub_topic_name = "/agribot/front_camera/image_raw"
        self.number_subscriber = rospy.Subscriber(sub_topic_name, Image, self.camera_callback)
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

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around the contours
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame with bounding boxes
        cv2.imshow('Frame with Bounding Boxes', resized_frame)

        cv2.waitKey(100)

if __name__ == '__main__':
    node_name = "sensor_front_cam"
    rospy.init_node(node_name)
    frontcam_data()
    rospy.spin()


