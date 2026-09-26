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
    if pattern_name != "alternating_arcs":
        raise ValueError(f"unknown pattern: {pattern_name!r}")
 
    # radius = 0.15 / 0.5 = 0.3 m; sweep = 0.5 * 1.57 = 0.785 rad (~45 deg)
    return [
        Segment(linear_x=0.15, angular_z=0.5, duration=1.57),   # left
        Segment(linear_x=0.15, angular_z=-0.5, duration=1.57),  # right
        Segment(linear_x=0.15, angular_z=0.5, duration=1.57),   # left
        Segment(linear_x=0.15, angular_z=-0.5, duration=1.57),  # right
    ]

