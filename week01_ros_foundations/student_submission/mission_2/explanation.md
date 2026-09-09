# Mission 2

## Predictions

{'straight': "I predict the robot will finish 0.45m away from it's starting point (0.15*3)", 'rotation': 'I predict its position will stay the same (forward speed is 0) while its direction will change - the robot will turn left by 1.5 radians (0.5*3)', 'curve': 'I predict the robot will be moving to the right in an arc because forward speed is not 0, which means that robot is moving forward (+0.15) and turning speed is also not 0 (-0.4 -> turning right approximately 23 degrees per second)', 'curve_modified': 'This curve should be wider because the forward speed is higher than in the previous example and the turning speed is lower. The robot is still turning right but slower'}

## Prediction Locks

{'straight': '2026-09-04T18:37:50.093390+00:00', 'rotation': '2026-09-04T18:41:23.564312+00:00', 'curve': '2026-09-04T18:47:58.376362+00:00', 'curve_modified': '2026-09-04T18:53:16.377110+00:00'}

## Motion Comparison

First trial. Commanded path length matches my prediction (I predicted that the robot would move forward in a straight line for 0.45 m). The estimated traveled path value is also close to the commanded (and predictions) with 0.013m difference, which I'm assuming is due to the noise

## Measurement Explanation

These two parameters measure different things. Estimated traveled path measures the distance that robot has traveled (for curved trial it is a length of the curve). The start-to-end distance is the distance between starting point and where the robot stopped, which is a straight line (like a shortest distance between start and end points). The curve has a bigger length than a straight line, therefore estimated traveled path has a higher value (0.587 > 0.529 for the 3rd trial).

## Safety Explanation

The command guard checks whether the speed is too high for a robot. If it is too high, for example, 20m/s, while we allow 0.3m/s at maximum, it "bans" this proposed command and simply does not send it to the robot (the robot will never receive it)
The final zero command stops the motion by sending new commands that have 0 motion speed and 0 turning speed, which means that the robot is not moving forward and not turning.
The timeout is needed if the robot, for some reason, stops receiving new commands while it's moving (communication stopped), and for safety reasons the guard in this case sends a stop command

## Modified Settings

{'linear_x': 0.22, 'angular_z': -0.1, 'duration': 4.0}
