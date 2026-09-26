# Mission 2

## Snapshot

{'source': 'reference', 'captured_at': '2026-09-25T22:14:25.302262+00:00', 'description': 'Instructor-defined frame geometry. No live ROS transforms were measured.', 'frames': ['odom', 'base_link', 'base_scan', 'rear_camera_link', 'hall_camera'], 'transforms': {'base_scan_to_base_link': {'translation': {'x': 0.2, 'y': 0.0, 'z': 0.14}, 'yaw': 0.0}, 'rear_camera_to_base_link': {'translation': {'x': -0.18, 'y': 0.0, 'z': 0.22}, 'yaw': 3.141592653589793}, 'hall_camera_to_base_link': {'translation': {'x': -1.5, 'y': 0.5, 'z': 1.2}, 'yaw': -1.5707963267948966}}}

## Frame Context

The rear camera transform stays fixed because the rear camera is attached to the robot, it moves with the robot, and its position relative to the robot doesn't change.
The hallway-camera-to-base_link transform changes as the robot moves because the hallway camera is not attached to the robot. It stays in the same place in the environment, so when robot moves, the distance and direction between the robot and that camera change.

## Initial Prompt

Write ROS 2 Python code that converts a point detected by the hallway camera into the robot's base_link frame.

## Initial Output

The node subscribes to PointStamped detections, uses tf2 to transform each one into base_link at the detection's timestamp, and republishes the result. It needs tf2_ros and tf2_geometry_msgs (sudo apt install ros-$ROS_DISTRO-tf2-geometry-msgs).
Because a hallway camera is fixed in the building rather than mounted on the robot, the transform has to pass through the world frame: camera → map → odom → base_link. Localization (e.g. AMCL/Nav2) and odometry usually provide the last two links. You need to supply the camera's pose in the map yourself, for example:
bash
ros2 run tf2_ros static_transform_publisher \
  --x 5.2 --y 1.0 --z 2.5 --roll 0 --pitch 0.6 --yaw 3.14 \
  --frame-id map --child-frame-id hallway_camera_optical_frame
To run it:
bash
python3 hallway_point_to_base_link.py --ros-args -p target_frame:=base_link

A few notes on the design:
- Timestamp handling. The node first transforms using the detection's own timestamp, because the robot keeps moving after the image is captured. If that timestamp falls outside the TF cache, which often happens when the camera's clock isn't synced, it falls back to the latest transform and logs a warning.
- Configuration. The topic and frame names are ROS parameters, so you can match them to your detector without editing the code.
- Accuracy. The result can only be as accurate as the robot's localization in map, plus your calibration of the camera's pose.

## Initial Source

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

## Initial Analysis

Assumptions and omissions:
1) Hallway camera is fixed and doesn't move
2) Frames' names (Claude assumed they are hallway_camera_optical_frame, base_link and etc.)
3) Hallway's camera is synchronized with the robot's
4) Hardcoded values: throttle_duration_sec = 2.0 and 5.0, TF cache_ time is 10 sec
5) Detections whose transform isn't available are dropped

## Improved Changes

1) It specified the ROS 2 distribution (there are many and they have their own difference)
2) The function name, signature and frame names are provided
3) It specifies how to handle edge cases:  if the frame transform isn't available -> return None, if the point's header.frame_id is not hall_camera -> raise ValueError
4) Prevent offset hardcoding, so all geometry must come from the TF tree
5) It requires preserving and using the point's timestamp, so the transform matches the robot's pose at the moment of observation (no fallback to the latest transform)

## Live Pending

False

## Synthesis

The original prompt contained no frame names and no description of how to handle edge cases, so AI had to invent them.
The improved prompt provided the exact frames, and described the failure behavior. It required a ValueError for any other frame, required the point's own timestamp, and required None when the transform is unavailable. The new prompt also didn't allow any latest-transform fallback. This is  important in a human-populated environment, because a transform from the wrong moment places a person where they no longer are, which can eventually lead to a collision.

## Live Issue


