#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageToVideoConverter:
    def __init__(self):
        rospy.init_node('image_to_video_converter', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/carla/base_link/rgb_view/image", Image, self.image_callback)
        self.video_writer = None
        self.frame_width = 1280  # Adjust according to your image size
        self.frame_height = 720  # Adjust according to your image size
        self.fps = 15  # Adjust according to your preference
        id=1
        self.video_filename = "videos/output_ros"+str(id)+".avi"
        while os.path.exists(self.video_filename):
            id+=1
            self.video_filename = "videos/output_ros"+str(id)+".avi"

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except Exception as e:
            print(e)
        else:
            if self.video_writer is None:
                self.initialize_video_writer(cv_image.shape[1], cv_image.shape[0])
            self.video_writer.write(cv_image)

    def initialize_video_writer(self, width, height):
        self.frame_width = width
        self.frame_height = height
        self.video_writer = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (self.frame_width, self.frame_height), True)
        rospy.loginfo("Video writer initialized")

    def run(self):
        rospy.loginfo("Image to Video Converter node started")
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        finally:
            if self.video_writer is not None:
                self.video_writer.release()

if __name__ == '__main__':
    image_to_video_converter = ImageToVideoConverter()
    image_to_video_converter.run()