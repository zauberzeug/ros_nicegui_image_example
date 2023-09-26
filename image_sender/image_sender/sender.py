import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from pathlib import Path

class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')
        self.publisher1 = self.create_publisher(Image, 'sender/im1', 10)
        self.publisher2 = self.create_publisher(Image, 'sender/im2', 10)
        self.timer = self.create_timer(1.0, self.publish_images)
        self.cv_bridge = CvBridge()

    def publish_images(self):
        image_dir = str(Path(__file__).parent.resolve())

        image1 = cv2.imread(image_dir + '/1.png')
        image2 = cv2.imread(image_dir + '/2.png')

        if image1 is not None and image2 is not None:
            msg1 = self.cv_bridge.cv2_to_imgmsg(image1, encoding='bgr8')
            msg2 = self.cv_bridge.cv2_to_imgmsg(image2, encoding='bgr8')
            self.publisher1.publish(msg1)
            self.publisher2.publish(msg2)
            self.get_logger().info('Images published.')
        else:
            self.get_logger().error('Failed to load images.')

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisherNode()
    rclpy.spin(image_publisher)

if __name__ == '__main__':
    main()