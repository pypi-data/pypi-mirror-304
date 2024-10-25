import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.nvidia as nvidia
import lumeo.scripts.gateway.docker as docker

def install_common_dependencies():
    
    display.output_message("Installing common dependencies...", status='info')
        
    hostutils.check_os()
    
    hostutils.check_disk_space()
    
    # Setup Nvidia DGPU drivers
    nvidia.check_nvidia_dgpu_driver()
    
    nvidia.check_disable_nvidia_driver_updates()
    
    # Setup Jetson specific components
    nvidia.enable_jetson_clocks()
    
    jetson_model_name = nvidia.get_jetson_model_name()
    if jetson_model_name:
        nvidia.setup_jetson_gpio()    
    nvidia.install_jetson_extras()
    
    # Setup Docker and NVIDIA toolkit
    docker.install_docker_and_nvidia_toolkit()
    
    docker.check_set_docker_data_dir()
    
    docker.set_docker_logs_configuration()
    
    docker.fix_nvidia_nvml_init_issue()
    
    # Disable X server
    hostutils.prompt_disable_x_server()
    
    # Start watchtower
    docker.start_watchtower()
    
    return

    
def update_common_dependencies():
    
    docker.fix_nvidia_nvml_init_issue()
    
    nvidia.enable_jetson_clocks()

    docker.set_docker_logs_configuration()
    
    docker.migrate_watchtower()
    
    return
    