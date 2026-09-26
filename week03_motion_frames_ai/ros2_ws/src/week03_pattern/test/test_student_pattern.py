import os
import math
import unittest
from week03_pattern.pattern import build_pattern
 
RADIUS = 0.30                 # m, from the specification
SWEEP = math.pi / 4           # rad, 45 deg per arc
ARC_LENGTH = RADIUS * SWEEP   # 0.236 m
EXPECTED_SIGNS = [+1, -1, +1, -1]   # left, right, left, right
END_X, END_Y = 0.85, 0.35     # ideal end pose, m


class MyPatternTests(unittest.TestCase):
    def test_my_pattern_geometry(self):
        segments = build_pattern(os.environ["WEEK03_ASSIGNED_PATTERN"])
        # Add assertions for your assigned pattern.
        self.assertEqual(len(segments), 4)
 
        x = y = heading = 0.0
        for i, seg in enumerate(segments):
            with self.subTest(segment=i):
                # speed x duration = arc length; angular speed x duration = angle
                self.assertAlmostEqual(seg.linear_x * seg.duration, ARC_LENGTH, delta=0.02)
                self.assertAlmostEqual(abs(seg.angular_z) * seg.duration, SWEEP, delta=0.04)
                self.assertAlmostEqual(abs(seg.linear_x / seg.angular_z), RADIUS, delta=0.02)
 
            # Integrate the arc to track the ideal pose.
            r = seg.linear_x / seg.angular_z
            turn = seg.angular_z * seg.duration
            x += r * (math.sin(heading + turn) - math.sin(heading))
            y += r * (math.cos(heading) - math.cos(heading + turn))
            heading += turn
 
        # Ends facing the start direction, at about (0.85, 0.35).
        self.assertAlmostEqual(heading, 0.0, delta=0.04)
        self.assertAlmostEqual(x, END_X, delta=0.02)
        self.assertAlmostEqual(y, END_Y, delta=0.02)

    def test_my_pattern_order(self):
        # Check another property with a known expected result.
        segments = build_pattern(os.environ["WEEK03_ASSIGNED_PATTERN"])
 
        # Every arc moves forward, and the turns go left, right, left, right.
        for i, (seg, sign) in enumerate(zip(segments, EXPECTED_SIGNS)):
            with self.subTest(segment=i):
                self.assertGreater(seg.linear_x, 0.0)
                self.assertEqual(math.copysign(1, seg.angular_z), sign)
 
        # Unknown names are rejected.
        with self.assertRaises(ValueError):
            build_pattern("not_a_pattern")

if __name__ == "__main__":
    unittest.main()