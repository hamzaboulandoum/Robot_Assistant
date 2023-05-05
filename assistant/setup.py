from setuptools import setup
import os
from glob import glob

package_name = 'assistant'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hamza Boulandoum',
    maintainer_email='hamzaboulandoum@gmail.com',
    description='Examples of minimal publisher/subscriber using rclpy',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'driver = assistant.driver:main',
        'broadcaster = assistant.broadcaster:main',
        'goal_listener = assistant.goal_listener:main',
        'teleop = assistant.teleop:main',
        'navigate = assistant.navigate:main',
        'follower = assistant.follower:main',
        'obstacles = assistant.obstacles:main',
        'pose_publisher = assistant.pose_publisher:main',
        'straight_line = assistant.straight_line:main',
        ],
    },
)
