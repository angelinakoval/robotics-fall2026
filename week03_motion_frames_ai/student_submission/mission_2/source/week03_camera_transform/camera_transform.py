"""Mission 2 student implementation.

Complete only ``transform_camera_point`` after preserving the initial AI output
in the guide. Course tests supply both real and simulated TF buffers.
"""
from __future__ import annotations

from geometry_msgs.msg import PointStamped
from rclpy.duration import Duration
import tf2_geometry_msgs  # noqa: F401  Registers PointStamped with tf2_ros.
from tf2_ros import TransformException

CAMERA_FRAME = 'hall_camera'
TARGET_FRAME = 'base_link'


def transform_camera_point(tf_buffer, point: PointStamped) -> PointStamped | None:
    """Return a hall_camera point expressed in base_link, or None if unavailable."""
    if not isinstance(point, PointStamped):
        raise ValueError('point must be a geometry_msgs.msg.PointStamped')

    if point.header.frame_id != CAMERA_FRAME:
        raise ValueError(
            f"Expected point in frame '{CAMERA_FRAME}', "
            f"got '{point.header.frame_id}'"
        )

    try:
        # Buffer.transform() looks up the transform at point.header.stamp
        # and applies it via tf2_geometry_msgs; the input is not modified.
        return tf_buffer.transform(
            point,
            TARGET_FRAME,
            timeout=Duration(seconds=0.0),
        )
    except TransformException:
        # Covers LookupException, ConnectivityException,
        # ExtrapolationException and InvalidArgumentException.
        return None