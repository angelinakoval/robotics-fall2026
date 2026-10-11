# Mission 1

## bias

-0.000255

## bias_vs_variance

Mostly matched. I predicted that with noisy readings the mean would be around 2m (it is 1.9997) and the bias would be  very small (-0.000255). 
Bias and variance describe different failures because bias measures how far the mean of the readings is from the true value, and variance measures how widely the readings are spread around the mean

## dropouts

5

## mean

1.9997

## median

1.99

## more_samples

Not quite. More samples will make the average (mean) more accurate, because random errors cancel each other out (positive and negative). Right now the standard error of the mean is SD/(n)^(1/2) = 0.2238/(235)^(1/2)=0.0146. If we have 10 times more readings, it will be 0.2238/(2350)^(1/2)=0.00462, which is much lower. However, more samples do not make each individual reading less noisy (standard deviation stays the same)

## outliers

3

## prediction

Biased readings: the mean will be different from 2m, and the readings will cluster on the left or right side of 2m (clustering around a wrong value).
Noisy readings: the standard deviation will be large, but the mean will be around 2m -> data will be widely spread

## prediction_draft

Biased readings: the mean will be different from 2m, and the readings will cluster on the left or right side of 2m (clustering around a wrong value).
Noisy readings: the standard deviation will be large, but the mean will be around 2m -> data will be widely spread

## profile

noisy

## robot_consequence

Robot uses these readings to decide when to stop. Because the readings are noisy, the robot can detect that an obstacle is about 2.77m away (one of the outliers), while it is actually 2m away. The robot thinks it has more room, but it does not. This error can lead to a collision.

## variance

0.05
