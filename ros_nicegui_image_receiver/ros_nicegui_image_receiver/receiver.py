import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

from nicegui import app, Client, ui
import threading
from pathlib import Path
from rclpy.executors import ExternalShutdownException
import base64

class ImageReceiverNode(Node):
    def __init__(self) -> None:
        super().__init__('image_receiver_node')
        # Create two subscriptions for the two images
        self.subscription1 = self.create_subscription(Image, 'sender/im1', self.image_callback1, 10)
        self.subscription2 = self.create_subscription(Image, 'sender/im2', self.image_callback2, 10)
        # Adding CV bridge for image processing
        self.cv_bridge = CvBridge()
        # Control variable to switch between the two images
        self.show_img1 = True

        # Add NiceGUI elements
        with Client.auto_index_client:
            # Create a row with a width of 40%
            with ui.row().style('width: 40%;'):
                # Create an empty interactive_image element
                self.sub_image = ui.interactive_image()
                # Create a button to switch between the images, it calls the switch_image function
                ui.button("Switch image", on_click=lambda: self.switch_image())

    def switch_image(self) -> None:
        # A simple function to trigger the control variable for the image
        self.show_img1 = not self.show_img1
        return

    def image_callback1(self, msg) -> None:
        # Check if the first image should be shown
        if self.show_img1:
            # Convert the image to a cv::Mat
            image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # Encode the image to base64
            base64_image = self.encode_image_to_base64(image)
            # Set the image source to the base64 string to display it
            self.sub_image.set_source(f'data:image/png;base64,{base64_image}')
        return

    def image_callback2(self, msg) -> None:
        #check if the second image should be shown
        if not self.show_img1:
            #convert the image to a cv::Mat
            image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            #encode the image to base64
            base64_image = self.encode_image_to_base64(image)
            #set the image source to the base64 string to display it
            self.sub_image.set_source(f'data:image/png;base64,{base64_image}')
        return
    
    def encode_image_to_base64(self, image) -> str:
        # Convert image to binary format
        _, image_data = cv2.imencode('.png', image)  
        # Encode the binary image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        # Return the base64 string
        return base64_image

def ros_main() -> None:
    # Standard ROS2 node initialization
    print('Starting ROS2...', flush=True)
    rclpy.init()
    image_receiver = ImageReceiverNode()

    try:
        rclpy.spin(image_receiver)
    except ExternalShutdownException:
        pass
    finally:
        image_receiver.destroy_node()
        rclpy.shutdown()

# Starting the ros node in a thread managed by nicegui. It will restarted with "on_startup" after a reload.
# It has to be in a thread, since NiceGUI wants the main thread for itself.
app.on_startup(lambda: threading.Thread(target=ros_main).start())

# We add reload dirs to just watch changes in our package
ui.run(title='Img show with NiceGUI', uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
