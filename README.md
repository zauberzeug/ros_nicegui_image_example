## What it does
The sender sends two images on two different topics every 1 second.

The receiver starts a NiceGUI Ui on localhost:8080 and displays the topics it sees.
By default, it will display the first topic.
If the button is pressed, it will display the next picture on the second topic and vice versa.


## How to use

Terminal1 :
```
python3 receiver.py
```
In this version of this tutorial, we start the script directly with python. 
In ROS2, you can run nodes directly with python3 because the ROS2 initialization uses standard Python APIs, but you must source your ROS2 distribution beforehand to ensure the environment is correctly set.

Terminal2 :
```
ros2 run image_sender sender
```


<img src="image_switcher.gif" width="500">
