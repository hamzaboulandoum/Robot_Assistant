import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
from sensor_msgs.msg import LaserScan

class PathFollowerObstacleNode(Node):
    def __init__(self):
        super().__init__('path_follower_obstacle')
        self.create_subscription(Path, '/path', self.path_callback, 10)
        self.create_subscription(Path, '/pose', self.pose_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.current_pose_ = None
        self.current_segment_ = 0
        self.path_ = None
        self.obstacle_threshold_ = 0.2  
    
    def scan_callback(self, msg):
        if msg.ranges:
            if min(msg.ranges) < self.obstacle_threshold_:
                twist = Twist()
                twist.linear.y = 0.0
                twist.angular.z = 0.0
                self.publisher_.publish(twist)

    def path_callback(self, msg):
        self.path_ = msg  
        self.current_segment_ = 0  

    def pose_callback(self, msg):
        self.current_pose_ = msg  
        if self.path_ is not None:
            self.follow_path()  

    def scan_callback(self, msg):
        
        if msg.ranges:
            if min(msg.ranges) < self.obstacle_threshold_:
                twist = Twist()
                twist.linear.y = 0.0
                twist.angular.z = 0.0
                self.publisher_.publish(twist)

    def follow_path(self):
       
        start_pose = self.current_pose_
        end_pose = self.path_.poses[self.current_segment_ + 1]
        segment = (start_pose.pose.position.x, start_pose.pose.position.y), (end_pose.pose.position.x, end_pose.pose.position.y)

        
        kv = 0.15  
        distance = ((segment[1][0] - segment[0][0])**2 + (segment[1][1] - segment[0][1])**2)**0.5
        velocity = kv * distance

        
      
        target_orientation = math.atan2(segment[1][1] - segment[0][1], segment[1][0] - segment[0][0])
        current_orientation = self.current_pose_.pose.orientation.z
        ka = 0.5 
        angular_velocity = ka * (target_orientation - current_orientation)

       
        twist = Twist()
        twist.linear.y = - velocity
        twist.angular.z = angular_velocity
        self.publisher_.publish(twist)


        if distance < 0.1:
            self.current_segment_ += 1

            
            if self.current_segment_ >= len(self.path_.poses) - 1:
                twist.linear.y= 0.0
                twist.angular.z = 0.0
                self.publisher_.publish(twist)
                self.path = None

