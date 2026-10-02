# mission_2 Submission

- Name: Angelina Kovalchuk
- Section: (not provided)

## Explanations

### prediction

The estimated forward distance will be too large because each tick is converted into more distance than the robot actually travelled while sideways distance will be too small because each strafe tick counts as less distance than it really is.

### calibration_analysis

I predicted that a forward scale that was too large would make the estimate overshoot in x, and a strafe scale that was too small would make it undershoot in y. It was confirmed by simulation. To tune it, I decreased the forward scale (to 0.5) and increased the strafe scale (to 0.5)
The sideways pod is necessary because the forward pod's wheel doesn't turn when the robot slides sideways.
Some drift can remain after calibration because even tiny errors can add up over time.