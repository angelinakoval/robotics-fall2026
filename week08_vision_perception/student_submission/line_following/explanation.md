# line_following

## comparison
In both attempts (gain = 0.08 and gain = 0.5), the mask showed the magenta line as white and the yellow floor as black. On the straight practice line with gain = 0.08, the robot corrected the initial error slowly, crossed the line after 4.3 s, overshot and kept swinging slowly (mean error = 0.062). With gain = 0.5, it crossed the line after 1.4s, also overshot but less, and then stayed near 0 (mean error = 0.013).
Curved segment: the track images show the magenta line curving to the right. With gain = 0.08, the line was pushed to the right side and centroid was far right of center. The robot turned slowly, so mean error was high (0.44). With gain = 0.5, the line stayed across the middle of the image, the centroid was only slightly right of center (mean error = 0.11)
Raising the gain made the robot correct faster and stay closer to the line.

## limits
In the gain = 0.08 track attempt, the robot fell behind on the right bend, but the mask still detected the line (slow turns, large error). Therefore, this failure began in control.
A real delivery robot around people would need lidar to detect the distance to people and obstacles, and an emergency stop.
