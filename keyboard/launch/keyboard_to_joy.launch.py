#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import launch_ros
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import (DeclareLaunchArgument, OpaqueFunction,
        SetLaunchConfiguration)

def generate_launch_description():
    # launch configuration variables
    this_pkg_directory = get_package_share_directory('keyboard')

    # declare launch arguments
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=TextSubstitution(text =  os.path.join(this_pkg_directory, 'config', 'example_config.yaml')),
        description='Absolute path to configuration file including .yaml extension'
        )

    # return the path to the keyboard config file
    def config_path(context):
        file = context.launch_configurations['config_file']
        return [SetLaunchConfiguration('config_path', file)]

    config_path_fn = OpaqueFunction(function = config_path)

    launch_kbd = Node(
            package='keyboard',
            executable='keyboard',
            name="keyboard"
            )

    launch_kbd2joy = Node(
            package='keyboard',
            executable='keyboard_to_joy.py',
            name="keyboard_to_joy",
            parameters=[
                { "config_file_name": [LaunchConfiguration('config_path')] }
            ]
            )  

    # create the launch description and populate
    ld = LaunchDescription()

    # arguments
    ld.add_action(config_file_arg)

    # opaque functions
    ld.add_action(config_path_fn)

    # actions
    ld.add_action(launch_kbd)
    ld.add_action(launch_kbd2joy)

    return ld
