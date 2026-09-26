#!/usr/bin/env python3
"""
Transform points detected by a fixed hallway camera into the robot's base_link frame.

Subscribes:  /hallway_camera/detected_point  (geometry_msgs/PointStamped)
             header.frame_id should be the camera frame, e.g. "hallway_camera_optical_frame"
Publishes:   /hallway_camera/detected_point_base_link  (geometry_msgs/PointStamped)

TF requirements (typical setup for a camera mounted in the environment):
    map -> hallway_camera_link -> hallway_camera_optical_frame   (static, you provide)
    map -> odom                                                  (localization, e.g. AMCL / Nav2)
    odom -> base_link                                            (odometry)
"""

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.time import Time

from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import tf2_geometry_msgs  # noqa: F401  registers PointStamped with tf2's do_transform


class HallwayPointTransformer(Node):
    def __init__(self):
        super().__init__('hallway_point_transformer')

        self.declare_parameter('input_topic', '/hallway_camera/detected_point')
        self.declare_parameter('output_topic', '/hallway_camera/detected_point_base_link')
        self.declare_parameter('target_frame', 'base_link')
        self.declare_parameter('camera_frame', 'hallway_camera_optical_frame')
        self.declare_parameter('tf_timeout_sec', 0.1)
        # If the exact-timestamp transform is unavailable, fall back to the latest one.
        self.declare_parameter('allow_latest_fallback', True)

        self.target_frame = self.get_parameter('target_frame').value
        self.camera_frame = self.get_parameter('camera_frame').value
        self.tf_timeout = Duration(seconds=self.get_parameter('tf_timeout_sec').value)
        self.allow_fallback = self.get_parameter('allow_latest_fallback').value

        self.tf_buffer = Buffer(cache_time=Duration(seconds=10.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.sub = self.create_subscription(
            PointStamped, self.get_parameter('input_topic').value, self.on_point, 10)
        self.pub = self.create_publisher(
            PointStamped, self.get_parameter('output_topic').value, 10)

        self.get_logger().info(
            f'Transforming points into "{self.target_frame}" frame')

    def on_point(self, msg: PointStamped):
        # Fill in the frame if the detector left it empty.
        if not msg.header.frame_id:
            msg.header.frame_id = self.camera_frame

        result = self.transform_point(msg)
        if result is None:
            return

        self.pub.publish(result)
        p = result.point
        self.get_logger().debug(
            f'{self.target_frame}: x={p.x:.3f} y={p.y:.3f} z={p.z:.3f}')

    def transform_point(self, msg: PointStamped):
        """Transform using the detection's timestamp; optionally fall back to latest TF."""
        try:
            return self.tf_buffer.transform(msg, self.target_frame, timeout=self.tf_timeout)
        except ExtrapolationException as e:
            if not self.allow_fallback:
                self.get_logger().warn(f'TF extrapolation error: {e}')
                return None
            # Timestamp is outside the TF cache (e.g. camera clock skew): use latest data.
            latest = PointStamped()
            latest.header.frame_id = msg.header.frame_id
            latest.header.stamp = Time().to_msg()  # time 0 = latest available
            latest.point = msg.point
            try:
                out = self.tf_buffer.transform(latest, self.target_frame, timeout=self.tf_timeout)
                out.header.stamp = msg.header.stamp  # keep the original detection time
                self.get_logger().warn(
                    'Used latest TF instead of detection timestamp', throttle_duration_sec=5.0)
                return out
            except (LookupException, ConnectivityException, ExtrapolationException) as e2:
                self.get_logger().warn(f'TF fallback failed: {e2}', throttle_duration_sec=2.0)
                return None
        except (LookupException, ConnectivityException) as e:
            self.get_logger().warn(
                f'Cannot transform {msg.header.frame_id} -> {self.target_frame}: {e}',
                throttle_duration_sec=2.0)
            return None


def main(args=None):
    rclpy.init(args=args)
    node = HallwayPointTransformer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()