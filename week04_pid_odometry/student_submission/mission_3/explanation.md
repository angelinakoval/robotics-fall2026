# mission_3 Submission

- Name: Angelina Kovalchuk
- Section: (not provided)

## Explanations

### technical_analysis

I predicted that higher speed would increase tracking error and reduce clearance. At high speed, the robot's true path swung wide at every corner (especially at WP2 and WP3) and after WP3 it came very close to a pedestrian's safety zone. 
The robot looks at where it is and where next route point is, and decides which direction to face. PID uses the difference between the direction it wants to head and the direction it is actually facing (heading error) to steer.
If the wheel radius were wrong, the robot would think it was somewhere it isn't, so even with good steering it would follow the wrong real path.

### human_centered_analysis

The consequential failure is the robot entering a pedestrian's safety zone. When the speed was high in the simulation, the robot came very close to such a zone (after WP3) because it swung wide at the corners.
To make the robot safer, I would make it drive slower new pedestrians and keep extra space from every safety zone. However, this will make the robot take more time to finish the trip
Trade-off: increase speed -> less safety, less time
decrease speed -> more safety, more time
Engineers are responsible for verifying this decision before deployment. They mush consider all edge cases before it is used around people.