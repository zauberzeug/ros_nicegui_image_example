## What it does
The sender sends two images on two different topics every 1 second.

The receiver starts a NiceGUI Ui on localhost:8080 and displays the topics it sees. By default, it will display the first topic. If the button is pressed, it will display the next picture on the second topic and vice versa.


## How to use

Terminal1 :
```
ros2 run ros_nicegui_image_receiver receiver
```

Terminal2 :
```
ros2 run image_sender sender
```
