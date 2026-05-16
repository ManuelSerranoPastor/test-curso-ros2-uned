import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_path = get_package_share_directory('rover_agricola_pkg')
    nav2_bringup_path = get_package_share_directory('nav2_bringup')

    # Solo cargamos el mapa que guardaste
    map_file = os.path.join(pkg_path, 'maps', 'campo_map.yaml')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_path, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'True'
                # AL QUITAR EL params_file, NAV2 USA SU CONFIGURACIÓN COMPLETA DE FÁBRICA
            }.items()
        )
    ])