# Mission 1

## Command Path Explanation

A proposed command (from /student_cmd_vel) travels on course_cmd_vel_guard node that does the guard check. The guard checks if the proposed velocity is within the safe speed limits (for example, if it is not too fast). Then, if it passed guard check it gets published to the cmd_vel.

## Graph Explanation

A ROS 2 graph shows the nodes that are currently running, and how they are connected to each other. For example, in this simulation course_cmd_vel_guard subscribes to student_cmd_vel and publishes cmd_vel (also parameter_events and rosout). It shows to this node takes the info (geometry messages) from student_cmd_vel channel, processes it, and outputs the results to the cmd_vel channel.

## Guided Checks

{'bridge_info': True, 'command_topics': True, 'guard_info': True, 'node_list': True, 'scan_info': True, 'scan_message': True}

## Scan Observation

I found inf. values  inside the ranges array, which represent that in these particular directions robot didn't detect any object

## Tools Explanation

Gazebo is responsible for simulation (simulation of world, obstacles, robot, sensor and etc) while RViz is responsible for data visualization (it visualizes that data that are coming from topics) 
