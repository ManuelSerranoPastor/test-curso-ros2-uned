import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('rover_agricola_pkg')

    # Rutas a los archivos que hemos ido creando
    xacro_file = os.path.join(pkg_path, 'urdf', 'rover.urdf.xacro')
    world_file = os.path.join(pkg_path, 'config', 'mvsim_world.xml')

    # 1. Nodo del Dibujo (El que hicimos en el Paso 2)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': Command(['xacro ', xacro_file])},
            {'use_sim_time': False} # CRÍTICO: Sincroniza el tiempo del dibujo con el simulador
        ]
    )

    # 2. Nodo de Físicas (MVSIM)
    mvsim_node = Node(
        package='mvsim',
        executable='mvsim_node',
        name='mvsim',
        output='screen',
        parameters=[
            {'world_file': world_file},
            {'use_sim_time': False}
        ]
    )

    # 3. El Visualizador RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        mvsim_node,
        rviz_node
    ])