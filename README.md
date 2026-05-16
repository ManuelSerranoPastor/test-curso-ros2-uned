# 🚜 Rover Agrícola Autónomo con ROS 2 Humble y MVSim

Este repositorio contiene el proyecto final de robótica móvil, consistente en una Prueba de Concepto (PoC) para la navegación autónoma de un rover agrícola. El sistema simula un entorno de huerto o invernadero utilizando modelos 3D y texturas realistas, sobre el cual el robot es capaz de localizarse y calcular trayectorias libres de colisiones.

---

## ✨ Características Principales

* **Entorno 3D Agrícola Optimizado:** Integración de modelos `.dae` (plantas de tomate) utilizando el sistema de clases (`<block:class>`) de MVSim para optimizar el consumo de memoria, con colisiones calculadas dinámicamente (`<shape_from_visual/>`).
* **Mapeo Láser (SLAM):** Generación de la topología 2D del terreno acotado mediante teleoperación y escaneo con sensor LiDAR simulado de 270º.
* **Navegación Autónoma y Evasión:** Implementación del stack de Nav2 para el cálculo de trayectorias globales y locales, permitiendo al rover ir del punto A al punto B esquivando las plantas y ajustándose a los límites del cultivo.
* **Cinemática Diferencial:** Control del rover basado en el modelo de tracción diferencial clásico, publicando odometría y transformadas (`/tf`) en tiempo real.

## 📂 Estructura del Proyecto

A continuación se muestra la organización de los archivos principales del paquete `rover_agricola_pkg`:

```text

.
├── curso_pgk_init
│   ├── curso_pgk_init
│   │   ├── __init__.py
│   │   ├── my_node.py
│   │   └── __pycache__
│   │       ├── __init__.cpython-310.pyc
│   │       └── my_node.cpython-310.pyc
│   ├── package.xml
│   ├── resource
│   │   └── curso_pgk_init
│   ├── setup.cfg
│   ├── setup.py
│   └── test
│       ├── test_copyright.py
│       ├── test_flake8.py
│       └── test_pep257.py
├── LICENSE
├── README.md
└── rover_agricola_pkg
    ├── CMakeLists.txt
    ├── config
    │   ├── mvsim_world_1.xml
    │   ├── mvsim_world.xml
    │   ├── nav2_params.yaml
    │   ├── tree
    │   ├── tree.dae
    │   ├── tree.obj
    │   └── tree.zip
    ├── include
    │   └── rover_agricola_pkg
    ├── launch
    │   ├── navegacion.launch.py
    │   ├── rover_sim.launch.py
    │   └── ver_robot.launch.py
    ├── maps
    │   ├── campo_map.pgm
    │   └── campo_map.yaml
    ├── package.xml
    ├── rviz
    ├── src
    └── urdf
        └── rover.urdf.xacro
```

---

# 📋 Requisitos del Sistema

Para ejecutar este proyecto, es necesario disponer del siguiente entorno:

- **Sistema Operativo:** Ubuntu 22.04 LTS
- **Framework:** ROS 2 Humble Hawksbill
- **Simulador:** Paquete `mvsim` (Mobile Vehicle Simulator)
- **Navegación:** Paquete `Nav2` y algoritmos de mapeo SLAM

---

# 🛠️ Instrucciones de Compilación

Abre una terminal y sitúate en la raíz de tu espacio de trabajo de ROS 2. A continuación, compila el paquete del rover agrícola e inicializa el entorno:

```bash
cd ~/curso_ros2_ws
colcon build --packages-select rover_agricola_pkg --symlink-install
source install/setup.bash
```

---

# 🚀 Instrucciones de Ejecución

Para evaluar el funcionamiento del rover y la navegación autónoma, se requieren dos terminales. Es fundamental haber ejecutado `source install/setup.bash` en ambas antes de lanzar los comandos.

## Terminal 1: Lanzamiento del Entorno Simulado (MVSim y RViz)

Este comando inicializa el motor de físicas, carga los modelos 3D agrícolas, los muros perimetrales y abre la interfaz gráfica de RViz2.

```bash
ros2 launch rover_agricola_pkg rover_sim.launch.py
```

## Terminal 2: Lanzamiento de la Inteligencia de Navegación (Nav2)

Este comando carga el mapa estático pregenerado y arranca los nodos de localización (AMCL), planificación de rutas y evasión de obstáculos.

```bash
ros2 launch rover_agricola_pkg navegacion.launch.py
```

---

# ⚙️ Configuración Visual en RViz2

Antes de enviar comandos de navegación, es necesario configurar las herramientas de visualización en la interfaz de RViz2.

## 🗺️ Añadir el Mapa

1. Haz clic en el botón **Add** (abajo a la izquierda) y selecciona **Map**.
2. En el panel de propiedades, despliega **Topic**, haz clic en el recuadro de texto y escribe:

```bash
/map
```

3. Dentro de ese mismo apartado **Topic**, cambia la propiedad **Durability Policy** de:

```text
Volatile → Transient Local
```

> ⚠️ Este paso es obligatorio; de lo contrario, el mapa estático pregenerado no se mostrará correctamente.

---

## 🤖 Añadir el Robot

1. Haz clic nuevamente en **Add** y selecciona **RobotModel**.
2. En sus propiedades, busca **Description Topic** y escribe:

```bash
/robot_description
```

Con esto, el modelo 3D del chasis del rover será visible en RViz2.

---

# 🖥️ Uso de la Interfaz (RViz)

- Utiliza la herramienta **2D Pose Estimate** en la barra superior de RViz para indicarle a AMCL la posición y orientación inicial aproximada del robot dentro del mapa.

- Utiliza la herramienta **2D Goal Pose** para seleccionar el destino deseado. El robot trazará automáticamente la ruta óptima y los controladores cinemáticos lo guiarán sorteando las plantas.

---

# 🗺️ Metodología de Mapeo (Fase SLAM)

El mapa estático proporcionado en este repositorio fue generado previamente mediante técnicas de SLAM (*Simultaneous Localization and Mapping*). El proceso técnico consistió en:

1. Lanzar el simulador MVSim.
2. Iniciar el nodo de mapeo SLAM (`slam_toolbox` o `Cartographer`).
3. Teleoperar manualmente el rover a través de las calles de cultivo mediante el nodo `teleop_twist_keyboard`, escaneando los muros perimetrales y los obstáculos centrales con el sensor LiDAR simulado de 270°.
4. Guardar la topología del entorno utilizando la herramienta estándar de ROS 2:

```bash
ros2 run nav2_map_server map_saver_cli -f mapa_agricola
```

---


## 🎥 Demostración en Vídeo

A continuación se muestra la demostración completa del sistema en funcionamiento, donde se puede observar la sincronización entre la planificación de rutas en RViz y la ejecución física del rover en MVSim:

