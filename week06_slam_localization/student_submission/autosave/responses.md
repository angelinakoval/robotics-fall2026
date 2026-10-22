# Week 6: SLAM and Mapping

- name: Angelina Kovalchuk
- email: angelina.kovalchuk06@stu-mail.hunter.cuny.edu

## final.course_reflection

I liked this activity more than the previous ones, since there were fewer computations and formulas, and driving the robot was fun, although it took me some time to get use to it. 
I had some issues ,though. When you restart for mission 2, you also need to restart rviz, because otherwise it produces errors. At one point, my robot collided with something and kept spinning around for quite some time, and I didn't know how to stop it.

## final.synthesis

The robot builds its map by combining odometry with output from the lidar, so it knows only what the lidar has reported, and only as accurately as it knew its own position. Both maps show a similar layout: the long wall beside the start, the left rooms, the corridor, and the bottom-right room. In Mission 1, the top middle room and the bottom area stayed unexplored, because walls blocked the view (the robot can see only what the lidar reports) and the robot never went to these areas. 
Motion-estimate error explains the difference in quality: both routes took 7 min, and Mission 2 covered more space (but it has lower quality because walls and parts of the layout overlap). I think revisiting known places can help with this issue, because the robot can locate itself better.
Both maps have limits. They count labeled cells rather than correct ones, and nothing compares this information with a ground truth. 
For a later task, I would trust the map that was obtained during Mission 1. It is missing some areas (middle top room and bottom area), however, it has less noise and overlaps: walls are straight, angles are right, and it matches the house plan. Mission 2 map covers more area, but it has overlapping areas.

## mission_1.drift_and_revisit

When I returned to the corridor near the start, the long horizontal wall looked mostly straight, but part of it left of the doorway appears thicker, like two lines, which may mean that an old wall shifted slightly

## mission_1.limitations

The top middle room stayed completely unknown. Its only opening is in the top-right corner, and the robot never drove through it, so the LiDAR could not see inside from the corridor below or the room to the right because the walls blocked its line of sight. The large area at the bottom of the map is also mostly unknown, because the robot only drove along the wall and that area is open.

## mission_1.route.original_prediction

Route: drive forward to x =1, turn left through the gap, then turn left again and explore the left side of the map (top-left room, then bottom-left room). The robot will enter rooms through doorways. Return back to corridor (x  = 0, y = 0). Then explore the right side. Go straight until x = 6, turn right and explore bottom-right room, go back. Drive straight, turn left, and explore top-middle room.
Place to revisit: the narrow corridor (x=1, y=0.2). The robot passes it near start and it has some features that can help recognize it (doorway below, wall above, open corridor to the left and right)

## mission_1.route.prediction_draft

Route: drive forward to x =1, turn left through the gap, then turn left again and explore the left side of the map (top-left room, then bottom-left room). The robot will enter rooms through doorways. Return back to corridor (x  = 0, y = 0). Then explore the right side. Go straight until x = 6, turn right and explore bottom-right room, go back. Drive straight, turn left, and explore top-middle room.
Place to revisit: the narrow corridor (x=1, y=0.2). The robot passes it near start and it has some features that can help recognize it (doorway below, wall above, open corridor to the left and right) 

## mission_2.comparison

Mission 2 mapped more space (95.54 VS 64.56). However, its known fraction dropped from 42.29% to 36.09% and its quality score fell from 63.3 to 60.7. My prediction wasn't supported, since I predicted a higher quality score and a clearer map, but Mission 2 covered more, and was less clean, so Mission 1 gave more useful coverage
Tradeoff: covering more ground in the same time leads to less careful scanning (more noise and errors) -> lower quality

## mission_2.map_choice

I would trust map from Mission 1 more, because it has a higher quality, it is cleaner (straight walls, right angles, match the house layout), even though bottom area and top middle room are unexplored. Mission 2 Map has overlapping house layout (overlapping rectangles, duplicated walls)

## mission_2.strategy.original_prediction

My robot will explore the open area at the bottom of the start, and I will drive into the top middle room instead of skipping it.
I predict this will produce cleaner and more complete map

## mission_2.strategy.prediction_draft

My robot will explore the open area at the bottom of the start, and I will drive into the top middle room instead of skipping it.
I predict this will produce cleaner and more complete map
