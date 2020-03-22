This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

### Team Members
Luca Profumo - profumo.luca@gmail.com

Andrea Ortalda - andrea.ortalda@fcagroup.com

### The Project
In this project, the software for the Udacity self-driving car is implemented using ROS.

ROS nodes for the functionality integration as well as core algorithms for self-driving were implemented.

These are the main building blocks of the project that we implemented:
* Motion planning: Waypoint updater
* Control: Drive-by-wire controller
* Perception: Traffic light detector and classifier

#### Testing
The software was tested and tuned mainly on the Udacity simulator test track which contains both straight and curved road segments and several traffic lights.

Reprocessing tests with real bag files were also performed for the traffic light detection and classification.

Thanks to the tests performed in simulation and reprocessing, the software is ready for testing with test vehicle Carla by Udacity engineers.

#### Waypoint updater
The waypoint updater ROS node subscribes to the vehicle current pose, the base waypoints loaded from the map and the waypoints from the traffic light detector.

It publishes a set of final waypoints that the ego vehicle has to follow.

The core algorithm calculates the next waypoints to follow based on the vehicle current pose and updates their velocity to be able to stop at a stop line with red traffic light.

##### Code guidelines
See the waypoint_loader.py ROS node.

#### Drive-by-wire controller
The drive-by-wire controller node subscribes to the current vehicle velocity, the dbw enabled switch command and the twist command coming from the waypoint follower which contains target linear and angular velocity for the ego vehicle.

It publishes three commands for the vehicle: throttle percentage, brake torque and steering angle.
The throttle/brake decision is based on the difference between current velocity and target linear velocity. In case braking is needed, the braking torque is calculated from the target deceleration using vehicle characteristics (mass and wheel radius).

Controllers already implemented and tuned by Udacity engineers for throttle (PID) and steering angle (yaw controller) were used.

##### Code guidelines
* dbw_node.py is the ROS node for control
* twist_controller.py has the control algorithm code
* pid.py and yaw_controller.py are the actual controllers

#### Traffic light detector and classifier
The traffic light detector node subscribes to the current vehicle pose, the base waypoints, the waypoints of stop lines for each traffic lights from the map and the vehicle camera image stream.

It publishes the traffic waypoints containing the stop line waypoints when a red traffic light is detected.

The traffic waypoints are calculated searching the next stop line waypoints with respect to the ego vehicle current pose and they are published when a red traffic light is detected.

For detection and classification the traffic light classifier Class is used, which is using two different neural networks, one for traffic light box detection and extraction and the other for the traffic light state classification (red/yellow/green).

##### Machine learning algorithms
The core algorithm consists of both traffic light detection and classification which were developed in Python with Jupyter notebook using Machine Learning techniques.
...

##### Code guidelines
* tl_detector.py is the ROS node
* tl_classifier.py is the Class for traffic light detection and classification
* Traffic_Light_detector.ipynb is the Jupyter notebook for the machine learning algorithms training and testing

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|               | Simulator |  Carla  |
| :-----------: | :-------: | :-----: |
| Nvidia driver |  384.130  | 384.130 |
|     CUDA      |  8.0.61   | 8.0.61  |
|     cuDNN     |  6.0.21   | 6.0.21  |
|   TensorRT    |    N/A    |   N/A   |
|    OpenCV     | 3.2.0-dev |  2.4.8  |
|    OpenMP     |    N/A    |   N/A   |

We are working on a fix to line up the OpenCV versions between the two.
