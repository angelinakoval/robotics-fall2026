# Lab 7 saved answers

## mission_1.diagnosis
normal_1: the box is on the mug, but slightly shifted to the right and extended downward.  In the raw threshold mask, the mug body and its shadow on the table were merged into one white region, due to the similarity in colors (mug and its shadow on the table)
dim_1: the box is not on the mug at all. It covers the shadow of the mug and a small area of the mug's bottom part. In dim image is darker -> many mug pixels were below 45 (minimum value)

## mission_1.limitations
I changed hue and dropped it from 35 to 12. This reduced the size of the box, because the rule now includes less of the orange shades (mostly reddish-brown shades remain), and therefore includes less of the table area.
Limitation:the rule works only for the specific colors in this image. If the color of the cup or the background (table) changes, the results will be different

## mission_2.comparison
At first, I set the detector threshold to 0.7, and it didn't accept any box in normal, dim, or occluded (2 missed in each), so I lowered it to 0.3. In normal, both detectors (learned and classical) found both mugs (2 correct, 0 false, 0 missed). In dim, both found 1 mug and missed 1 mug, but the classical detector also produces 1 false box. In occluded, both missed both mugs, and the classical detector produced 2 false boxes.
The difference the matters for locating the mug is the false boxes. Both detectors missed the same mug, but when classical detector failed, it pointed to the wrong place. For example, in dim 1 the classical detector selected the shadow next to the mug, and the learned detector gave no box at all.

## mission_2.choice
I recommend the learned detector with an acceptance threshold of 0.3 for further testing. In normal and dim it found as many mugs as the classical detector, but it didn't produced false boxes (classical did).
For normal 1: IoU = 0.562, Dice = 0.72. The mask covers the mug body, but it also covers part of the keyboard and desk. The foreground model has no cup label, so it marks any object that stands out, not specifically the requested mug.
Limitation: the results may not hold for a different mug and background.

## pillar_search.diagnosis
In attempt 20261030T233744-e7b51c9f, the blue pillar was centered successfully. While searching, the robot turned left in place. At about 30s the blue pillar entered the camera image at the left edge. The mask showed it as one white region, and the centroid error was about -0.95

I didn't change any settings, I used provided values, and it ran successfully.

## pillar_search.evidence
All 4 colors were centered: red (error: -0.015), green (-0.058), turquoise (-0.049) and blue (-0.005)
The state timeline shows the same pattern for each color: search (turning left at 0.35 with no target), center (the pillar appears at the left edge and the robot turns left), confirm and hold, then next.
A centered colored region and a stable hold do not prove identity, because the controller only checks whether pixels fall in a color range.

## line_following.comparison
In both attempts (gain = 0.08 and gain = 0.5), the mask showed the magenta line as white and the yellow floor as black. On the straight practice line with gain = 0.08, the robot corrected the initial error slowly, crossed the line after 4.3 s, overshot and kept swinging slowly (mean error = 0.062). With gain = 0.5, it crossed the line after 1.4s, also overshot but less, and then stayed near 0 (mean error = 0.013).
Curved segment: the track images show the magenta line curving to the right. With gain = 0.08, the line was pushed to the right side and centroid was far right of center. The robot turned slowly, so mean error was high (0.44). With gain = 0.5, the line stayed across the middle of the image, the centroid was only slightly right of center (mean error = 0.11)
Raising the gain made the robot correct faster and stay closer to the line.

## line_following.limits
In the gain = 0.08 track attempt, the robot fell behind on the right bend, but the mask still detected the line (slow turns, large error). Therefore, this failure began in control.
A real delivery robot around people would need lidar to detect the distance to people and obstacles, and an emergency stop.

## final.synthesis
The three missions taught me that turning visual evidence into reliable robot behavior depend on finding the right object and also reacting to it in the right way.
In Mission 1: I compared a classical color detector with a learned detector. The classical detector found the mug in normal images, but in dim_1 it struggles a little and put its box on the shadow next to the mug, or didn't put it anywhere.  With the learned detector at a threshold of 0.3, both detectors found the same mugs in normal, dim and occluded images. However, the classical detector made 3 false boxes (1 in dim, 2 in occluded), while the learned detector made none.
In Mission 2: the robot centered all four pillars in order (red, green, turquoise, blue) with a gain of 1.2. Every final error was inside the 0.10 tolerance.
In Mission 3:  with a gain of 0.08, the robot turned too slowly and fell behind on the bend (error up to 0.81, mean error 0.44). With a gain of 0.5, it followed the same bend much more closely (mean error 0.11)

## final.course_reflection
This assignment was a bit hard for me because there were many parameters to take care of. I also had some technical issues with the simulation. It was glitching from time to time, and the old world (from mission 2) kept running in the background, so the data for mission 3 looked confusing.
This is a very time-consuming process that requires perseverance and attention, because you need to test several options and change only one setting at a time (or its influence will be confused with something else).

