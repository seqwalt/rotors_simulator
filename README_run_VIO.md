### Suggestions before getting started:
- Appropriately source the catkin workspace(s)
(for example ```source ~/catkin_ws/devel/setup.bash```), depending on your file system. ROS commands will not work otherwise. This should be the first thing you check if a command like ```rosrun my_package my_node``` is not working.
- For any given experiment below, use tmux with multiple panes in one window to keep everything quickly accessible. This is much faster that having multiple terminal tabs open, and is less computationally burdensome on your system. This guide may be helpful: [tmux intro](https://www.redhat.com/sysadmin/introduction-tmux-linux#:~:text=Get%20started%20with%20tmux,window%2C%20and%20attaches%20to%20it.&text=You%20can%20detach%20from%20your,pressing%20Ctrl%2BB%20then%20D.)

----------------------------------

# ROVIO Experiments

## Run ROVIO with quadcopter in RotorS simulator. Build the stereo ROVIO setup with ```catkin build -DROVIO_NCAM=2```

### Option 1: Lee Controller, without control panel gui
1. Launch gazebo world with quadcopter
```roslaunch rotors_gazebo vio_quadcopter_spawn.launch world_name:=PAMPC_full x_init:=-5```  
2. Launch controller with desired reference state for quadcopter
```roslaunch rotors_gazebo vio_quadcopter_control.launch odometry_topic:=/est_odometry```  
3. Publish /est_odometry using rovio transform node  
```rosrun rotors_rovio_tf est_odom_node``` (initially it just uses ground truth)
4. Start Rovio so /est_odometry starts publishing transformed rovio odometry.  Visualize and run ROVIO
```
roslaunch rovio rovio_rviz.launch (show ground truth and rovio)
roslaunch rovio rovio_node_RotorS.launch (run rovio)
```
5. Apply imu integration to compensate for lag of rovio, to produce final odometry estimation.  
```rosrun odom_predictor odom_predictor_node```

### Option 2 (currently unstable flight): MPC or PAMPC & autopilot, with control panel GUI.
Note the controller uses Gazebo ground truth as state estimation, not ROVIO due to stability issues. If you want to use ROVIO as the state info for the controller, set ```use_ground_truth:=false``` in step 1.1.

0. To enable/disable PAMPC, open .../rpg_mpc/parameters/default.yaml
and set Q_perception to 0 to disable PAMPC, or to 50 to enable PAMPC.
1. Launch the RotorS simulator:
  1. ```roslaunch rpg_rotors_interface vio_quadrotor_empty_world.launch use_mpc:=true x_init:=-5 use_ground_truth:=true```
  (set ```use_ground_truth``` to false if you want to use rovio to provide odometry for the controller)
  2. Optional (if doing PAMPC): Tab complete after typing "rostopic pub /hummingbird/mpc/point_of_interest", then fill-in what 3D point to keep in camera FOV. (use the origin for this example)
2. Start the node that can switch between ground truth and Rovio once Rovio is activated:  
```rosrun rotors_rovio_tf est_odom_node```
5. Apply imu integration to compensate for lag of rovio, to produce final odometry estimation.  
```rosrun odom_predictor odom_predictor_node```
3. In the gui press: Connect --> Arm Bridge --> Start. The quad will hover. Set z = 5, and press "Go To Pose"

4. Visualize and run ROVIO
```roslaunch rovio rovio_rviz.launch``` (show ground truth and rovio)  
```roslaunch rovio rovio_node_RotorS.launch``` (run rovio)
5. Two rovio windows should pop up, showing patches on the image scene. Using the GUI, send the quad to x=0, y=5, and the quad should face the point of interest as it moves (if using PAMPC).

### Useful Tips
- Reset quadcopter position if needed. Run the following in the terminal while Gazebo is running.
```
rosservice call /gazebo/set_model_state "model_state:
    model_name: 'hummingbird'
    pose:
        position:
          x: -5.0
          y: 0.0
          z: 5.0"
```
- After editing the est_odom_node.cpp file, re-build the relevant ros package
```
cd ../catkin_ws
catkin build rotors_rovio_tf
source devel/setup.bash
```

----------------------------------

# VINS-Fusion Experiments

## Run VINS-Fusion with quadcopter in RotorS simulator.
1) Launch the RotorS simulator as in the ROVIO RotorS section above:

2) Start the node that publishes the ground truth (GT) path, using the GT odometry as input:
2.1) >>> cd ~/ROS/catkin_ws/src (where ground_truth_odom2path.py is located)
2.2) >>> ./ground_truth_odom2path.py (run the node)

3) Start rviz and vins-fusion  
```roslaunch vins vins_rviz.launch```  
```rosrun vins vins_node ~/ROS/catkin_ws/src/VINS-Fusion/config/RotorS_sim/RotorS_stereo.yaml``` (for stereo only)  
```rosrun vins vins_node ~/ROS/catkin_ws/src/VINS-Fusion/config/RotorS_sim/RotorS_stereo.yaml``` (for stereo + imu)  

Note 1): ../VINS-Fusion/vins_estimator/src/rosNodeTest.cpp was changed to give the
initial position of (-5, 0, 5) and an initial rotation for the camera (starting on line 244). In order to change this,
need to go to workspace root, then ```catkin build vins```.

Note 2): Current the stereo + imu method drifts immediately (maybe caused by zeroed-out gravity in imu message?)
A similar problem can be seen in this github issue: https://github.com/HKUST-Aerial-Robotics/VINS-Fusion/issues/116

----------------------------------
