# Week 1: Discovering a Robot Through ROS 2

## Student

- Name: Angelina Kovalchuk
- Email: angelina.kovalchuk06@stu-mail.hunter.cuny.edu

## final.architecture_evidence

The node is reactive because it makes a decision about the output velocity based only on the current sensor readings (lidar measurements)

## final.course_reflection

1. This activity showed me that developing robotics software is a complicated task, and many edge cases and nuances have to be considered well before the actual implementation
2. I enjoyed it, I like the "creativity" part (In this lab, we just had to follow instructions, but I like the idea of creating your own design and trying to consider all nuances)
3. Robots have to operate in human-populated environments, therefore ethical preferences and social norms have to be considered. For example, many people feel uncomfortable if a robot gets too close, so when designing we need to take that into account
4. The interface and simulation were my favorite parts. I like how you can actually see what each components is doing
5. -

## final.hardware_next

I would probably test the time delay and see how it affects the robot's performance (important for crowded areas)

## final.middleware_debugging

The ROS 2 graph shows only the nodes that are currently active (publishing and/or subscribing). If a command never reaches the robot, that means something in the chain is not working (some data wasn't published), and I can use this graph to see whether all components are at least alive

## final.system_synthesis

Designing robotics software is difficult for many reasons, one of which is the imperfection of sensors. The robot has to work with noisy data and make decisions based on it. During planning, you have to take into consideration all such imperfections and inconsistencies and implement safety checks and guards. For example, in this particular case from the lab, some of the lidar measurements were “nan” – if we ignore them, our robot could collide with an object that, for some reason, was not detected, and crash. Therefore, when we account for this edge case, we send a velocity of 0, making the robot stop.
Another very important issue that significantly complicates robotics software development is time desynchronization. Processing data takes time, so if there are many nodes connected consecutively to each other, there will be a delay between the moment the data is detected by the lidar and sent to the /scan topic, and the moment it reaches the velocity guard check and gets publish to /cmd_vel. Someone could appear right in front of the robot, but the robot might not have enough time to process it. In this lab, ROS 2 middleware connected at least 4 components: 
1) the lidar measures distances and sends them to /scan
2) we take these readings and find the minimum distance
3) based on that distance, we determine a velocity
4) the guard check takes this velocity and performs a safety check
5) the velocity is sent to the robot and the robot performs the action.
That is why, one of the main trade-offs to consider is the time/safety trade-off. Implementing additional checks for invalid data increases processing time (the robot will take more time to make a decision), which can lead to collisions or crashes. If we prioritize speed and disregard all checks, the robot will make decisions faster, but if it receives invalid data, it can also crash.

## final.timing_evidence

Some of the Lidar measurements was nan (not many though)

## mission_1.command_path_explanation

A proposed command (from /student_cmd_vel) travels on course_cmd_vel_guard node that does the guard check. The guard checks if the proposed velocity is within the safe speed limits (for example, if it is not too fast). Then, if it passed guard check it gets published to the cmd_vel.

## mission_1.graph_explanation

A ROS 2 graph shows the nodes that are currently running, and how they are connected to each other. For example, in this simulation course_cmd_vel_guard subscribes to student_cmd_vel and publishes cmd_vel (also parameter_events and rosout). It shows to this node takes the info (geometry messages) from student_cmd_vel channel, processes it, and outputs the results to the cmd_vel channel.

## mission_1.guided_checks

{'bridge_info': True, 'command_topics': True, 'guard_info': True, 'node_list': True, 'scan_info': True, 'scan_message': True}

## mission_1.scan_observation

I found inf. values  inside the ranges array, which represent that in these particular directions robot didn't detect any object

## mission_1.tools_explanation

Gazebo is responsible for simulation (simulation of world, obstacles, robot, sensor and etc) while RViz is responsible for data visualization (it visualizes that data that are coming from topics) 

## mission_2.measurement_explanation

These two parameters measure different things. Estimated traveled path measures the distance that robot has traveled (for curved trial it is a length of the curve). The start-to-end distance is the distance between starting point and where the robot stopped, which is a straight line (like a shortest distance between start and end points). The curve has a bigger length than a straight line, therefore estimated traveled path has a higher value (0.587 > 0.529 for the 3rd trial).

## mission_2.modified_settings

{'linear_x': 0.22, 'angular_z': -0.1, 'duration': 4.0}

## mission_2.motion_comparison

First trial. Commanded path length matches my prediction (I predicted that the robot would move forward in a straight line for 0.45 m). The estimated traveled path value is also close to the commanded (and predictions) with 0.013m difference, which I'm assuming is due to the noise

## mission_2.prediction_locks

{'curve': '2026-09-04T18:47:58.376362+00:00', 'curve_modified': '2026-09-04T18:53:16.377110+00:00', 'rotation': '2026-09-04T18:41:23.564312+00:00', 'straight': '2026-09-04T18:37:50.093390+00:00'}

## mission_2.predictions

{'curve': 'I predict the robot will be moving to the right in an arc because forward speed is not 0, which means that robot is moving forward (+0.15) and turning speed is also not 0 (-0.4 -> turning right approximately 23 degrees per second)', 'curve_modified': 'This curve should be wider because the forward speed is higher than in the previous example and the turning speed is lower. The robot is still turning right but slower', 'rotation': 'I predict its position will stay the same (forward speed is 0) while its direction will change - the robot will turn left by 1.5 radians (0.5*3)', 'straight': "I predict the robot will finish 0.45m away from it's starting point (0.15*3)"}

## mission_2.safety_explanation

The command guard checks whether the speed is too high for a robot. If it is too high, for example, 20m/s, while we allow 0.3m/s at maximum, it "bans" this proposed command and simply does not send it to the robot (the robot will never receive it)
The final zero command stops the motion by sending new commands that have 0 motion speed and 0 turning speed, which means that the robot is not moving forward and not turning.
The timeout is needed if the robot, for some reason, stops receiving new commands while it's moving (communication stopped), and for safety reasons the guard in this case sends a stop command

## mission_3.data_to_command

The first function returns the distance in meters to the nearest object that is in front of the robot (it takes all recorded distances, checks only the valid distances (not 0 and not inf) that are directly in front of the robot, and returns the  minimum if one exists)
The second function takes that distance and, based on that, assigns a velocity (if the object is too close (<=stop_distance), it stops (velocity is 0.0), if the distance is valid and doesn't exceed the stop_distance threshold, the function returns a velocity between 0 and 0.18)

## mission_3.missing_data_safety

For safety reasons. If there is no valid front measurement, it doesn't necessarily mean that there is no object in front of the robot (it could be sensor noise). Therefore, when the robot "is not sure", we prefer it to stop until it gets a valid information

## mission_3.system_layers

The ROS 2 node subscribes to sensor data (distances from lidar) -> node calls front_distance which takes these distances and returns the distance to the nearest object -> decide_velocity takes this distance and, based on it, returns an allowed velocity -> this allowed velocity is published to /student_cmd_vel -> command_guard then checks this velocity (safety check), and if it passes, the velocity is published to /cmd_vel

## part_1.activity

{'sensor': {'normal': True, 'changed': True}, 'timing': {'normal': True, 'changed': True}, 'hardware': {'normal': True, 'changed': True}}

## part_2.activity

{'reactive': {'normal': True, 'changed': True}, 'behavior': {'normal': True, 'changed': True}, 'deliberative': {'normal': True, 'changed': True}, 'hybrid': {'normal': True, 'changed': True}, 'safety': {'normal': True, 'changed': True}}

## part_3.activity

{'middleware': {'single': True, 'multiple': True}, 'communication': {'topic': True, 'service': True}, 'failure': {'healthy': True, 'sensor': True, 'type': True, 'visualization': True}, 'inspection': {'nodes': True, 'node_info': True, 'topics': True, 'topic_info': True, 'echo': True, 'services': True, 'broken': True}}
