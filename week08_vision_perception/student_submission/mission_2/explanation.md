# mission_2

## comparison
At first, I set the detector threshold to 0.7, and it didn't accept any box in normal, dim, or occluded (2 missed in each), so I lowered it to 0.3. In normal, both detectors (learned and classical) found both mugs (2 correct, 0 false, 0 missed). In dim, both found 1 mug and missed 1 mug, but the classical detector also produces 1 false box. In occluded, both missed both mugs, and the classical detector produced 2 false boxes.
The difference the matters for locating the mug is the false boxes. Both detectors missed the same mug, but when classical detector failed, it pointed to the wrong place. For example, in dim 1 the classical detector selected the shadow next to the mug, and the learned detector gave no box at all.

## choice
I recommend the learned detector with an acceptance threshold of 0.3 for further testing. In normal and dim it found as many mugs as the classical detector, but it didn't produced false boxes (classical did).
For normal 1: IoU = 0.562, Dice = 0.72. The mask covers the mug body, but it also covers part of the keyboard and desk. The foreground model has no cup label, so it marks any object that stands out, not specifically the requested mug.
Limitation: the results may not hold for a different mug and background.
