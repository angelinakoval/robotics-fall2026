# Week 5: Sensors, Noise, and Uncertainty

- course_id: 24493606
- email: angelina.kovalchuk06@login.cuny.edu
- name: Angelina Kovalchuk

## concepts.observation

Increasing bias leads to increasing of mean and median values.
Increasing noise leads to increasing of variance and standard deviation.

## final.course_reflection

Robotics involves a lot of math and computation, and the different parts affect each other, so it is hard to track the influence of each parameter.
This activity showed that the same technical mistake can affect people in different ways, so it has to be considered who might get hurt when certain technical choices are made.
Mission 3 was confusing, especially the prediction part and what  the 7 scenarios should look like. I thought I needed to write a general prediction for 2 scenarios,  but I guess I needed to compare each new run with the previous one.

## final.synthesis

In Mission 1, the sensor was noisy rather than biased: its bias was only  -0.0003 m, but its standard deviation was about 0.22 m, with 3 outliers and 5 dropouts.
Mission 2 showed that estimation choices trade accuracy against responsiveness. Larger moving-average windows lagged after sudden changes, raising rmse from 0.1485 to 0.1698 m. Weight 0.75 on Sensor A cut the delay to 0.7 s but raised the max error to 1.55 m, while weight 0.50 gave the lowest rmse (0.1378 m).
Mission 3 showed that decisions depend on deployment context. Dropouts drove most errors: missing readings set to STOP caused unnecessary stops (0.0408 warehouse, 0.0338 assistive), MOVE raised assistive false-safes to 0.0924, and Insufficient evidence gave 0 for both. In the warehouse, raising the margin from 0.10 to 0.20 m removed false-safes. The assistive robot needed a higher threshold (0.95 m), because people with limited mobility bear the cost of both injuries and repeated stops.

## mission_1.bias

-0.000255

## mission_1.bias_vs_variance

Mostly matched. I predicted that with noisy readings the mean would be around 2m (it is 1.9997) and the bias would be  very small (-0.000255). 
Bias and variance describe different failures because bias measures how far the mean of the readings is from the true value, and variance measures how widely the readings are spread around the mean

## mission_1.dropouts

5

## mission_1.mean

1.9997

## mission_1.median

1.99

## mission_1.more_samples

Not quite. More samples will make the average (mean) more accurate, because random errors cancel each other out (positive and negative). Right now the standard error of the mean is SD/(n)^(1/2) = 0.2238/(235)^(1/2)=0.0146. If we have 10 times more readings, it will be 0.2238/(2350)^(1/2)=0.00462, which is much lower. However, more samples do not make each individual reading less noisy (standard deviation stays the same)

## mission_1.outliers

3

## mission_1.prediction

Biased readings: the mean will be different from 2m, and the readings will cluster on the left or right side of 2m (clustering around a wrong value).
Noisy readings: the standard deviation will be large, but the mean will be around 2m -> data will be widely spread

## mission_1.prediction_draft

Biased readings: the mean will be different from 2m, and the readings will cluster on the left or right side of 2m (clustering around a wrong value).
Noisy readings: the standard deviation will be large, but the mean will be around 2m -> data will be widely spread

## mission_1.profile

noisy

## mission_1.robot_consequence

Robot uses these readings to decide when to stop. Because the readings are noisy, the robot can detect that an obstacle is about 2.77m away (one of the outliers), while it is actually 2m away. The robot thinks it has more room, but it does not. This error can lead to a collision.

## mission_1.variance

0.05

## mission_2.comparison

For the moving average with weight 0.25, increasing the window (3-7-11) made the rmse and max error worse (rmse: 0.1485-0.1601-0.1698, max error: 1.1701-1.2695-1.2791). Mae and response delay stayed about the same (Mae: 0.7, delay 1,1).
Larger windows slightly smoothed the noise.  In the matched pair (window size: 3, weight: 0.25) the median had a slightly lower rmse (0.1479-0.1485) and mae (0.0747 - 0.0766) that the moving average. However, it had a higher max error (1.2934 - 1.1701) and a longer delay (1.3-1.1)

## mission_2.fusion_choice

With median window 3:
- weight 0.25 gave rmse 0.1479m, max error 1.29m and delay 1.3s
- weight 0.5 gave rmse 0.1378m, max error 1.42m and delay 1.1s
- weight 0.75 gave rmse 0.1485m, max error 1.55m and delay 0.7s
I selected weight  0.5 because it had the lowest rmse. More weight on sensor A shortened the delay (1.3 -> 0.7) but increased the max error (1.29->1.55), so sensor A respond quickly but noisy. More weight on sensor B gave smaller errors but a longer delay, so sensor B is less noisy but slower. Weight 0.5 balances these limitations.

## mission_2.manual_average

4.1667

## mission_2.manual_fusion

2.25

## mission_2.manual_median

2.3

## mission_2.prediction_draft

A larger window should reduce noise because more readings are averaged, but it will increase the response delay. A median filter should have the same delay as a moving average with the same window size, but lower error, because it ignores outliers. Increasing the weight on sensor A increases the noise but it may respond faster.

## mission_2.responsiveness

More smoothing makes the estimate less noisy but slower to react. The delays ranged from 0.7s (weight 0.75)  to 1.3s. (weight 0.25). Larger windows did not reduce error, because the extra lag after the sudden drop outweighed the smoothing. 
For a nearby person the delay means that if someone suddenly steps in front of the robot, the robot keeps acting as if they are still far away for 1.1 s.

## mission_2.selected

4

## mission_3.Assistive.prediction_draft

I predict the most challenging scenarios will be a sudden approach and missing sensor readings. Compared with attempt 1, which used the same settings with missing readings set to stop, I expect the false-safe rate to stay at 0, because the stop boundary is above the safety distance. I expect the unnecessary-stop rate to drop, because the robot will abstain during dropouts instead of stopping. Detection delay should stay about the same.

## mission_3.Warehouse.prediction_draft

I predict that the most challenging scenarios will be a sudden approach, missing sensor readings, and noisy estimates near the stopping boundary. If the estimate lags, the robot may still MOVE or SLOW after the obstacle is within the safety distance, causing false-safe events and detection delay. A larger margin would stop earlier but cause more unnecessary stops.

## mission_3.context_comparison

Attempt 7 and 8 both had a false-safe rate of 0, but attempt 7 had an unnecessary stop rate of 0.0338 while attempt 8 had 0. The main difference is the missing-data rule: attempting 7 stops when both readings are missing, while attempt 8 uses insufficient evidence. Attempt 1, which matches attempt 8 except for using Stop, also had 0.0338, so the missing-data rule caused all of the unnecessary stops. Attempt 7 also used a larger margin (0.3 vs 0.2 m) and 2 confirmations instead of 1, but compared with attempt 1 these did not change either rate. They make the robot stop earlier but wait longer to confirm, so they mainly affect delay. For people with limited mobility, attempt 8 is better: it keeps them just as safe while avoiding unnecessary stops that would reduce their access and trust in the robot.

## mission_3.error_costs

In the warehouse, false-safe errors can damage equipment and endanger workers, while unnecessary stops delay work. Raising the margin from 0.1 to 0.2 m reduced false-safes from 0.0062 to 0, but unnecessary stops stayed at 0.0408 because missing readings were set to Stop. In the assistive setting, false-safe errors can injure people with limited mobility, and unnecessary stops reduce their access.

## mission_3.limitations

The tests show how each policy performs in the same seven simulated scenarios, so policies can be compared fairly. They do not show real-world performance with different people, speeds or sensor failures, and dangerous-command events are only a risk proxy, not real collisions. Before deployment, I would consult people with limited mobility who would use the robot, such as wheelchair users, and run a supervised real-world trial with people approaching at different speeds.
