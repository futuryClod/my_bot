import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'my_bot' 

    # 1. Include the robot_state_publisher launch file
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2. Modern Gazebo Launch configuration (Replaced gazebo_ros with ros_gz_sim)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
        )]),
        # This tells Gazebo to load up a standard blank world
        launch_arguments={'gz_args': 'empty.sdf'}.items()
    )

    # 3. Modern Spawner Node configuration (Replaced spawn_entity.py with create)
    spawn_entity = Node(
        package='ros_gz_sim', 
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_bot' # Changed -entity to -name
        ],
        output='screen'
    )

    # 4. CRITICAL: You must return the LaunchDescription object at the end!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])



    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])