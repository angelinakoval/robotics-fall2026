# Mission 3

## Data To Command

The first function returns the distance in meters to the nearest object that is in front of the robot (it takes all recorded distances, checks only the valid distances (not 0 and not inf) that are directly in front of the robot, and returns the  minimum if one exists)
The second function takes that distance and, based on that, assigns a velocity (if the object is too close (<=stop_distance), it stops (velocity is 0.0), if the distance is valid and doesn't exceed the stop_distance threshold, the function returns a velocity between 0 and 0.18)

## Missing Data Safety

For safety reasons. If there is no valid front measurement, it doesn't necessarily mean that there is no object in front of the robot (it could be sensor noise). Therefore, when the robot "is not sure", we prefer it to stop until it gets a valid information

## System Layers

The ROS 2 node subscribes to sensor data (distances from lidar) -> node calls front_distance which takes these distances and returns the distance to the nearest object -> decide_velocity takes this distance and, based on it, returns an allowed velocity -> this allowed velocity is published to /student_cmd_vel -> command_guard then checks this velocity (safety check), and if it passes, the velocity is published to /cmd_vel
