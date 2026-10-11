# Mission 3

## Assistive.prediction_draft

I predict the most challenging scenarios will be a sudden approach and missing sensor readings. Compared with attempt 1, which used the same settings with missing readings set to stop, I expect the false-safe rate to stay at 0, because the stop boundary is above the safety distance. I expect the unnecessary-stop rate to drop, because the robot will abstain during dropouts instead of stopping. Detection delay should stay about the same.

## Warehouse.prediction_draft

I predict that the most challenging scenarios will be a sudden approach, missing sensor readings, and noisy estimates near the stopping boundary. If the estimate lags, the robot may still MOVE or SLOW after the obstacle is within the safety distance, causing false-safe events and detection delay. A larger margin would stop earlier but cause more unnecessary stops.

## context_comparison

Attempt 7 and 8 both had a false-safe rate of 0, but attempt 7 had an unnecessary stop rate of 0.0338 while attempt 8 had 0. The main difference is the missing-data rule: attempting 7 stops when both readings are missing, while attempt 8 uses insufficient evidence. Attempt 1, which matches attempt 8 except for using Stop, also had 0.0338, so the missing-data rule caused all of the unnecessary stops. Attempt 7 also used a larger margin (0.3 vs 0.2 m) and 2 confirmations instead of 1, but compared with attempt 1 these did not change either rate. They make the robot stop earlier but wait longer to confirm, so they mainly affect delay. For people with limited mobility, attempt 8 is better: it keeps them just as safe while avoiding unnecessary stops that would reduce their access and trust in the robot.

## error_costs

In the warehouse, false-safe errors can damage equipment and endanger workers, while unnecessary stops delay work. Raising the margin from 0.1 to 0.2 m reduced false-safes from 0.0062 to 0, but unnecessary stops stayed at 0.0408 because missing readings were set to Stop. In the assistive setting, false-safe errors can injure people with limited mobility, and unnecessary stops reduce their access.

## limitations

The tests show how each policy performs in the same seven simulated scenarios, so policies can be compared fairly. They do not show real-world performance with different people, speeds or sensor failures, and dangerous-command events are only a risk proxy, not real collisions. Before deployment, I would consult people with limited mobility who would use the robot, such as wheelchair users, and run a supervised real-world trial with people approaching at different speeds.
