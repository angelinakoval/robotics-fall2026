# mission_1 Submission

- Name: Angelina Kovalchuk
- Section: (not provided)

## Explanations

### prediction

With too little Kp, I expect the arm to move slowly and settle below the target.
With too little kd, I expect the arm to reach the target quickly. It will overshoot and oscillate around the target before settling

### tuning_analysis

I predicted that with too little kd the arm would move fast and overshoot, and that's exactly what happened with kd = 0 (the arm swung past the target and oscillated before settling). I also predicted that too little kp would make the arm slow and weak. That was confirmed too - with kp =0 the arm moved very slowly and couldn't reach the target (it wasn't strong enough to overcome gravity).
To tune it, I increased both kp and kd parameters (kp=13.0 and kd = 4.0). The higher kp gave the arm enough strength to reach the target, and higher kd slowed down the motion, so it settled with little overshoot.
With gravity compensation off, the arm settled close to the target nut not exactly on it. With compensation on, it settled perfectly on the target.