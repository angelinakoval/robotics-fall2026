# Mission 3

## Specification

Sequence: Robot drives four forward arcs, each of radius 0.3m in the specific order: +45 degrees (left), -45 degrees (right), +45 degrees (left), -45 degrees (right). Nah arc is 45 degrees (or 0.785 rad - theta - turning angle) and 0.3*0.785 =0.236 m long. The robot ends facing its initial direction
Speed:  linear.x must stay within 0.22 m/s and  angular.z must stay within 0.8 rad/s. (chosen speed 0.15m/s and 0.5 rad/s - in the middle)
Stopping behavior: after the last arc the robot pushes a zero velocity command and stops
Success criteria: ideal pose relative to the start: +45-45+45-45 = 0 -> robot is facing its start direction; 
Total path = 4*0.236 =0.944 
Arch length = r*theta = 0.3*0.785=0.236 
t = 0.785/0.5=1.57 
Each arch moves the robot by: dx = 0.3 *sin(45) = 0.212m; dy = 0.3*(1-cos(45)) =0.088m
4 arcs: x = 4*0.212 =0.848; y = 4*0.088 =0.352, so ideal pose is (0.85, 0.35, 0)


## Saved Specification

Sequence: Robot drives four forward arcs, each of radius 0.3m in the specific order: +45 degrees (left), -45 degrees (right), +45 degrees (left), -45 degrees (right). Nah arc is 45 degrees (or 0.785 rad - theta - turning angle) and 0.3*0.785 =0.236 m long. The robot ends facing its initial direction
Speed:  linear.x must stay within 0.22 m/s and  angular.z must stay within 0.8 rad/s. (chosen speed 0.15m/s and 0.5 rad/s - in the middle)
Stopping behavior: after the last arc the robot pushes a zero velocity command and stops
Success criteria: ideal pose relative to the start: +45-45+45-45 = 0 -> robot is facing its start direction; 
Total path = 4*0.236 =0.944 
Arch length = r*theta = 0.3*0.785=0.236 
t = 0.785/0.5=1.57 
Each arch moves the robot by: dx = 0.3 *sin(45) = 0.212m; dy = 0.3*(1-cos(45)) =0.088m
4 arcs: x = 4*0.212 =0.848; y = 4*0.088 =0.352, so ideal pose is (0.85, 0.35, 0)


## Assigned Pattern

alternating_arcs

## Original Prompt

This is a ROS 2 Jazzy Python package. Implement only build_pattern(pattern_name: str) -> list[Segment] for 'alternating_arcs' in the existing pattern.py.

Existing Segment Class (do not change it)
"""AI-assisted motion pattern implementation.

Preserve the original AI response in Streamlit. Review it, then implement a safe
version here. The node accepts only segments returned by ``build_pattern``.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    linear_x: float
    angular_z: float
    duration: float

def build_pattern(pattern_name: str) -> list[Segment]:
    """Return ordered, bounded motion segments for the assigned pattern.

    Supported assignments are ``rounded_rectangle``, ``l_path``, and
    ``alternating_arcs``. Do not include the final stop; the ROS wrapper always
    publishes it and the evaluator verifies it.
    """
    raise NotImplementedError("Mission 3: review the AI output and implement your assigned pattern")


Pattern 'alternating_arcs': four forward arch in this order, each of radius 0.3m: +45 degrees (left), -45 degrees (right), +45 degrees (left), -45 degrees (right). The robot must finish facing its initial direction.

Conventions: robot body frame, +x forward, positive angular_z turns left.
The course-provided pattern_node.py calls this function, publishes the returned segments repeatedly through /student_cmd_vel, and sends the final zero command.

Use the existing Segment class with linear_x = 0.15 (m/s), angular_z = +0.5(rad/s) for the left arch and -0.5(rad/s) for the right arch, and duration = 1.57 (s).

Return the ordered segments for the assigned specification and raise ValueError for an unknown pattern name.
Stay within 0.22 m/s, 0.80 rad/s, 30 seconds per segment, and 60 seconds total.
Do not replace the wrapper or course checks. Explain assumptions and propose tests.

## Original Output

build_pattern("alternating_arcs") now returns four segments in the order left, right, left, right. Each one is (0.15, ±0.5, 1.57). The Segment class, the module docstring and the wrapper are unchanged. All 20 tests pass locally.
Checking the numbers
Radius: v/ω = 0.15/0.5 = 0.30 m.
Turn per arc: ω·t = 0.5 × 1.57 = 0.785 rad. A true 45° is π/4 = 0.7854 rad, so each arc is short by about 0.02°.
Final heading: the left and right turns are exactly equal and opposite, so the robot ends facing exactly its starting direction.
Time and limits: total time is 6.28 s. Every value is well inside the 0.22 m/s, 0.80 rad/s, 30 s per segment and 60 s total limits.
Assumptions and design choices
Only one pattern is supported. Any name other than "alternating_arcs" raises ValueError. That includes rounded_rectangle and l_path, because they weren't assigned to you. It also includes case or whitespace variants and non-string input. If your course expects NotImplementedError for the two unassigned patterns instead, it's a two-line change.
There is an extra safety check. A _validate() step runs before anything is returned. It rejects values that are infinite, NaN or not numbers, speeds over the limits, segment times that are zero, negative or over 30 s, and a total time over 60 s. It adds to the course checks rather than replacing them.
No stop segment is added. As the docstring says, the wrapper publishes the final zero command.
The robot ends up offset to the left. Each left-then-right pair moves the robot forward 2r·sin θ and also shifts it left by 2r(1−cos θ). With two pairs, it ends about 0.85 m ahead and 0.35 m to the left of where it started. The spec only constrains heading, so this is expected, but don't be surprised by the sideways offset when you test it in simulation or on the real robot.
Real-robot drift isn't modelled. Acceleration limits and publish-rate timing will make the real path differ slightly from the ideal one. Those effects belong to the wrapper and the evaluator.

## Original Source

"""AI-assisted motion pattern implementation.

Preserve the original AI response in Streamlit. Review it, then implement a safe
version here. The node accepts only segments returned by ``build_pattern``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Safety envelope from the assignment. The course wrapper and evaluator still
# apply their own checks; this is an extra guard, not a replacement.
MAX_LINEAR_X = 0.22        # m/s
MAX_ANGULAR_Z = 0.80       # rad/s
MAX_SEGMENT_DURATION = 30.0  # s
MAX_TOTAL_DURATION = 60.0    # s

# alternating_arcs parameters (given by the specification):
#   radius = v / w = 0.15 / 0.5  = 0.30 m
#   sweep  = w * t = 0.5 * 1.57  = 0.785 rad (~45 deg, pi/4 = 0.7854)
_ARC_LINEAR_X = 0.15
_ARC_ANGULAR_Z = 0.5
_ARC_DURATION = 1.57


@dataclass(frozen=True)
class Segment:
    linear_x: float
    angular_z: float
    duration: float


def _alternating_arcs() -> list[Segment]:
    """Four forward arcs: left, right, left, right (each 0.3 m radius, ~45 deg).

    Left and right sweeps are equal and opposite, so the net heading change is
    exactly zero and the robot ends facing its initial direction.
    """
    left = Segment(linear_x=_ARC_LINEAR_X, angular_z=+_ARC_ANGULAR_Z, duration=_ARC_DURATION)
    right = Segment(linear_x=_ARC_LINEAR_X, angular_z=-_ARC_ANGULAR_Z, duration=_ARC_DURATION)
    return [left, right, left, right]


# Only the assigned pattern is implemented. Any other name is rejected.
_PATTERNS = {
    "alternating_arcs": _alternating_arcs,
}


def _validate(segments: list[Segment]) -> None:
    """Raise ValueError if any segment falls outside the safety envelope."""
    if not segments:
        raise ValueError("pattern produced no segments")

    total = 0.0
    for i, seg in enumerate(segments):
        values = (seg.linear_x, seg.angular_z, seg.duration)
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in values):
            raise ValueError(f"segment {i} has a non-finite or non-numeric value: {seg}")
        if abs(seg.linear_x) > MAX_LINEAR_X:
            raise ValueError(f"segment {i} linear_x {seg.linear_x} exceeds {MAX_LINEAR_X} m/s")
        if abs(seg.angular_z) > MAX_ANGULAR_Z:
            raise ValueError(f"segment {i} angular_z {seg.angular_z} exceeds {MAX_ANGULAR_Z} rad/s")
        if not 0.0 < seg.duration <= MAX_SEGMENT_DURATION:
            raise ValueError(
                f"segment {i} duration {seg.duration} not in (0, {MAX_SEGMENT_DURATION}] s"
            )
        total += seg.duration

    if total > MAX_TOTAL_DURATION:
        raise ValueError(f"total duration {total} s exceeds {MAX_TOTAL_DURATION} s")


def build_pattern(pattern_name: str) -> list[Segment]:
    """Return ordered, bounded motion segments for the assigned pattern.

    Supported assignments are ``rounded_rectangle``, ``l_path``, and
    ``alternating_arcs``. Do not include the final stop; the ROS wrapper always
    publishes it and the evaluator verifies it.

    Only ``alternating_arcs`` is implemented here; every other name (including
    the two patterns not assigned to this student) raises ``ValueError``.
    """
    builder = _PATTERNS.get(pattern_name) if isinstance(pattern_name, str) else None
    if builder is None:
        raise ValueError(
            f"unknown or unassigned pattern {pattern_name!r}; "
            f"supported: {sorted(_PATTERNS)}"
        )

    segments = builder()
    _validate(segments)
    return segments

## Assumptions

Motion: 4 forward arcs in the order left, right, left, right, with no pauses and no stop segment
Units: linear_x in m/s, angular_z in rad/s, duration in seconds
Frame: robot body frame , +x forward, positive angular_z turns left
Timing: open-loop (each segments is held for its duration)

## Problems

1.57 s for duration is hardcoded and rounded, therefore some computations are not precise

## Test Plan

behavior-test: call build_pattern('alternating_arcs'). Expected: 4 segments with angular_z signs +,-,+,-; each radius = 0.30 m (within 0.02), angle = 0.785 rad (within 0.04), length = 0.236 m (within 0.02); sum of angular_z*duration = 0. Integrating the segments from (0,0) gives end pose (0.85, 0.35) m, heading 0. build_pattern('unknown') raises ValueError
velocity-limit test: every segment has linear velocity <=0.22m/s and angular velocity <=0.8rad/s
Stop test: the last message should be linear.x = 0, angular.z = 0

## Modifications

removed suggested extra helper functions - _validate and _alternating_arcs()

## Live Pending

False

## Evidence Analysis

The important tests are test_linear_limits, test_angular_limits and test_positive_durations, which passed (7 of 7) and established that every command stays within 0.22m/s and 0.0 rad/s with valid durations.
My tests - test_my_pattern_geometry establishes that each of four arch is 0.236 m, 0.785 rad and 0.3m in radius, and that the ideal pose is (0.85, 0.35, 0). test_my_pattern_order establishes that every arc moves forward, the turns go left, right, left, right, and an unknown name raises ValueError.
Additional test: live run -  test that checks that the last command on /student_cmd_vel is zero.

## Ai Disclosure

I used Claude as an assistant throughout the mission. I used it to explain geometry, to review and improve my prompts, and for debugging (I had some errors during testing)
