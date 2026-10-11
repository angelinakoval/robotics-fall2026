# Mission 2

## comparison

For the moving average with weight 0.25, increasing the window (3-7-11) made the rmse and max error worse (rmse: 0.1485-0.1601-0.1698, max error: 1.1701-1.2695-1.2791). Mae and response delay stayed about the same (Mae: 0.7, delay 1,1).
Larger windows slightly smoothed the noise.  In the matched pair (window size: 3, weight: 0.25) the median had a slightly lower rmse (0.1479-0.1485) and mae (0.0747 - 0.0766) that the moving average. However, it had a higher max error (1.2934 - 1.1701) and a longer delay (1.3-1.1)

## fusion_choice

With median window 3:
- weight 0.25 gave rmse 0.1479m, max error 1.29m and delay 1.3s
- weight 0.5 gave rmse 0.1378m, max error 1.42m and delay 1.1s
- weight 0.75 gave rmse 0.1485m, max error 1.55m and delay 0.7s
I selected weight  0.5 because it had the lowest rmse. More weight on sensor A shortened the delay (1.3 -> 0.7) but increased the max error (1.29->1.55), so sensor A respond quickly but noisy. More weight on sensor B gave smaller errors but a longer delay, so sensor B is less noisy but slower. Weight 0.5 balances these limitations.

## manual_average

4.1667

## manual_fusion

2.25

## manual_median

2.3

## prediction_draft

A larger window should reduce noise because more readings are averaged, but it will increase the response delay. A median filter should have the same delay as a moving average with the same window size, but lower error, because it ignores outliers. Increasing the weight on sensor A increases the noise but it may respond faster.

## responsiveness

More smoothing makes the estimate less noisy but slower to react. The delays ranged from 0.7s (weight 0.75)  to 1.3s. (weight 0.25). Larger windows did not reduce error, because the extra lag after the sudden drop outweighed the smoothing. 
For a nearby person the delay means that if someone suddenly steps in front of the robot, the robot keeps acting as if they are still far away for 1.1 s.

## selected

4
