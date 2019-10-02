# px4 controllers



## Components
1. [mRo Pixhawk Barebones](https://store.mrobotics.io/Genuine-PixHawk-1-Barebones-p/mro-pixhawk1-bb-mr.htm)
2. [TF mini](https://www.sparkfun.com/products/14588)
3. [PX4 Flow No SONAR](https://www.amazon.com/Hobbypower-PX4FLOW-Optical-PIXHAWK-Control/dp/B01FJVF1QM/ref=asc_df_B01FJVF1QM/?tag=hyprod-20&linkCode=df0&hvadid=309839945011&hvpos=1o5&hvnetw=g&hvrand=3874390054812292320&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9007733&hvtargid=pla-568554353016&psc=1&tag=&ref=&adgrpid=61059095029&hvpone=&hvptwo=&hvadid=309839945011&hvpos=1o5&hvnetw=g&hvrand=3874390054812292320&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9007733&hvtargid=pla-568554353016)
4. [Power Module (Optional)](https://www.amazon.com/Hobbypower-Module-APM2-8-Pixhawk-Controller/dp/B00JWMLWIG/ref=asc_df_B00JWMLWIG/?tag=hyprod-20&linkCode=df0&hvadid=242017695311&hvpos=1o1&hvnetw=g&hvrand=14371582054129874327&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9007733&hvtargid=pla-697573061207&psc=1)
5. [Pixhawk Cables](https://www.amazon.com/Cylewet-Control-Specification-Position-Connector/dp/B01N4IRVQI/ref=sr_1_7?keywords=pixhawk+cables&qid=1569971607&sr=8-7)
6. [Spektrum Rx DSMX](https://www.amazon.com/Spektrum-DSMX-Quad-Receiver-Diversity/dp/B01ABV7K5A/ref=sr_1_3?keywords=spektrum+receiver&qid=1569971688&sr=8-3)
7. [Emax Motors RS2306](https://emaxmodel.com/emax-rs2306-racespec-motor-cooling-series-2400.html)
8. [Cobra 30A ESC](https://www.cobramotorsusa.com/multirotoresc-30amp.html)
9. [Cobra ESC Programmer](https://innov8tivedesigns.com/parts/speed-controllers-becs/cobra-usb-programmer)
10. [Matek PDB](https://www.amazon.com/HobbyKing-Matek-PDB-XT60-BEC-12V/dp/B01EFVD4YS)
11. [microSD Card](https://www.amazon.com/Sandisk-Ultra-Micro-UHS-I-Adapter/dp/B073K14CVB/ref=sr_1_3?keywords=micro+sd+card+8gb&qid=1569972491&sr=8-3)


## Hardware Setup
1. [ArduCopter Stack Flashing](http://ardupilot.org/copter/docs/common-loading-firmware-onto-pixhawk.html)
	1.1. [3.6.7 Pixhawk 1 Stable firmware](http://firmware.ardupilot.org/Copter/stable-3.6.7/Pixhawk1/arducopter.apj)
2. [Mounting the Flight Controller](http://ardupilot.org/copter/docs/common-mounting-the-flight-controller.html)
3. [TFmini setup on arducopter](http://ardupilot.org/copter/docs/common-benewake-tfmini-lidar.html)
4. [PX4Flow Setup](http://ardupilot.org/copter/docs/common-px4flow-overview.html)
5. [Mandatory Hardware Configuration](http://ardupilot.org/copter/docs/configuring-hardware.html)
6. [DISARM Switch Setup](http://ardupilot.org/copter/docs/tuning.html) Set CH7 
7. [Motor Configuration](http://ardupilot.org/copter/docs/connect-escs-and-motors.html) Use QuadX
8. Fly Manually

## Offboard Control Setup
1. [MavROS Binary Installation](https://dev.px4.io/v1.9.0/en/ros/mavros_installation.html)
2. Launch mavros
	2.1. roslaunch mavros px4.launch
	2.2. rosrun mavros mavsys rate --all 10
	2.3. rosrun mavros mavparam set SYSID_MYGCS 1
3. Run RCOveride node which publishes to the topic : '/mavros/rc/override'. RCOveride node should publihs message with same rc array size as 'mavros/rc/in'. If you publish 0, that channel will not be overidden, but if you publish any other positive value, it will be overidden. After override, echo 'mavros/rc/in' to confirm that the RC override is working.

This repository contains controllers which can be used in unison with mavros and the px4 stack in order to achieve minimum snap trajectory tracking.
The position feedback will be done using the vicon system.

**Authors**: Ashwin Varghese Kuruttukulam  
**Maintainer**: Ashwin Varghese Kuruttukulam
**Affiliation**: Perception and Robotics Group, Unversity of Maryland  

## Installation Instructions (Ubuntu)

1. Install the repository and its dependencies (with rosinstall):

```
sudo apt-get install ros-kinetic-mavros ros-kinetic-mavros-extras
```

2. Set up a catkin workspace (if not already done):

```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin init
cd src 
git clone https://github.com/ashwinvk94/px4_quad_controllers
catkin_make
```

## Notes
Always start mavros before using any of the functionalities of this repo. On the intel aero drone, this can be done by running the following command on a terminal:
```
rosrun mavros mavros_node _fcu_url:=tcp://127.0.0.1:5760 _system_id:=2
```
Also, you can ssh into the aero drone using the following command:
'''
ssh aero@192.168.8.1
'''
where "Aero" is the user_name of the computer


## Usage

To the run the attitude+thrust controller inbuilt in the px4 firmware simply launch attitude_thrust_controller using the command:
'''
roslaunch px4_quad_controllers attitude_thrust_controller.launch
'''

This will start publishing the the attitude and thrust setpoints to the the topic "/mavros/setpoint_raw/attitude"  
Now if you move the flight mode to "OFFBOARD" mode, then it will go that the attitudes and thrust set as per the rosparams. Default values are (0,0,0,0).
