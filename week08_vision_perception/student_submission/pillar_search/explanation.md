# pillar_search

## diagnosis
In attempt 20261030T233744-e7b51c9f, the blue pillar was centered successfully. While searching, the robot turned left in place. At about 30s the blue pillar entered the camera image at the left edge. The mask showed it as one white region, and the centroid error was about -0.95

I didn't change any settings, I used provided values, and it ran successfully.

## evidence
All 4 colors were centered: red (error: -0.015), green (-0.058), turquoise (-0.049) and blue (-0.005)
The state timeline shows the same pattern for each color: search (turning left at 0.35 with no target), center (the pillar appears at the left edge and the robot turns left), confirm and hold, then next.
A centered colored region and a stable hold do not prove identity, because the controller only checks whether pixels fall in a color range.
