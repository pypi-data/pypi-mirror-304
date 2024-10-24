import os
import platform

import lumeo.scripts.gateway.hostutils as hostutils
import lumeo.scripts.gateway.common as common
import lumeo.scripts.gateway.display as display
import lumeo.scripts.gateway.updater as updater
import lumeo.scripts.gateway.docker as dockerutils

def get_wgm_status():
    """Get the status of the Lumeo Web Gateway Manager."""
    status = "not_installed"
    status_str = "Web Gateway Manager: "
    containers = dockerutils.DOCKER_CLIENT.containers.list(all=True, filters={"name": "lumeo_wgm"})
    if containers:
        status = containers[0].status
        container_info = containers[0].attrs        
        status_str += f"{container_info['Name']} ({container_info['Config']['Image']})"
        if status == "running":
            status_str += f" [bold green]{status.capitalize()}[/bold green]"
        else:
            status_str += f" [bold red]{status.capitalize()}[/bold red]"
    else:
        status_str += "[orange]Not Installed[/orange]"
    return status, status_str


def install_wgm():
    """Install Lumeo Web Gateway Manager."""   
    
    display.output_message("Installing Lumeo Web Gateway Manager...", status='info')    
     
    arch_type = platform.machine()
    
    wgm_status, _ = get_wgm_status()
    
    if wgm_status == 'not_installed':
        common.install_common_dependencies()
            
        # Create shared volume directory
        os.makedirs("/opt/lumeo/wgm", exist_ok=True)    
        
        # Install WGM container
        wgm_container = "lumeo/wgm-x64:latest" if arch_type == "x86_64" else "lumeo/wgm-arm:latest"

        # Remove existing lumeo_wgm container
        if hostutils.run_command("docker ps -a -q -f name=lumeo_wgm", sudo=True, check=False):
            hostutils.run_command("docker stop lumeo_wgm", sudo=True)
            hostutils.run_command("docker rm lumeo_wgm", sudo=True)
            hostutils.run_command("rm -rf /opt/lumeo/wgm", sudo=True)

        # Pull and run new container
        #run_command(f"docker pull {wgm_container}", sudo=True)
        dockerutils.docker_download_image(wgm_container)
        hostutils.run_command(f"docker run -d -v /opt/lumeo/wgm/:/lumeo_wgm/ --name lumeo_wgm --restart=always --network host {wgm_container}", sudo=True)

        # Install and start lumeo-wgm-pipe
        hostutils.run_command("install -m u=rw,g=r,o=r /opt/lumeo/wgm/scripts/lumeo-wgm-pipe.service /etc/systemd/system/", sudo=True)
        hostutils.run_command("systemctl enable --now lumeo-wgm-pipe", sudo=True)

        # Restart container
        hostutils.run_command("docker restart lumeo_wgm", sudo=True)

        # Install update cron job
        updater.install_update_gateway_updater()

        display.output_message("Lumeo Web Gateway Manager has been installed. Access by visiting https://<device-ip-address>", status='info')
    else:
        display.output_message("Lumeo Web Gateway Manager is already installed.", status='info')
    
    return


def update_wgm():
    """Update Lumeo Web Gateway Manager."""        
    
    display.output_message("Updating Lumeo Web Gateway Manager...", status='info')
    
    # Determine the appropriate container based on architecture
    arch_type = platform.machine()
    wgm_container = "lumeo/wgm-x64:latest" if arch_type == "x86_64" else "lumeo/wgm-arm:latest"

    # Get the Image ID of the currently running container
    running_image_id = hostutils.run_command("docker inspect --format='{{.Image}}' lumeo_wgm", sudo=True)

    if running_image_id:
        # Pull the latest image
        #run_command(f"docker pull {wgm_container}", sudo=True)
        dockerutils.docker_download_image(wgm_container)

        # Get the Image ID of the latest image
        latest_image_id = hostutils.run_command(f"docker inspect --format='{{{{.Id}}}}' {wgm_container}", sudo=True)

        # Compare the IDs. If they are different, stop, remove and run the new container
        if running_image_id != latest_image_id:
            hostutils.run_command("docker stop lumeo_wgm && docker rm -f lumeo_wgm", sudo=True)

            # Host network needed for bonjour broadcast
            hostutils.run_command(f"docker run -d -v /opt/lumeo/wgm/:/lumeo_wgm/ --name lumeo_wgm --restart=always --network host {wgm_container}", sudo=True)
            hostutils.run_command("systemctl restart lumeo-wgm-pipe", sudo=True)
            
            # Remove the old image
            hostutils.run_command(f"docker image rm -f {running_image_id}", sudo=True)
            display.output_message("Updated and started new WGM container successfully.", status='info')
        else:
            display.output_message("Running WGM container is up-to-date.", status='info')
            
        updater.install_update_gateway_updater()
    else:
        display.output_message("Lumeo Web Gateway Manager container not found.", status='error')
    
    return

def remove_wgm():
    """Remove Lumeo Web Gateway Manager."""
    wgm_status, _ = get_wgm_status()
    display.output_message("Removing Lumeo Web Gateway Manager...", status='info')
    
    if wgm_status != 'not_installed':
        # Stop and remove container
        hostutils.run_command("docker stop lumeo_wgm && docker rm -f lumeo_wgm", sudo=True)
        # Remove MediaMTX container if it exists
        hostutils.run_command("docker stop mediamtx && docker rm -f mediamtx", sudo=True)
        # Remove lumeo-wgm-pipe service
        hostutils.run_command("systemctl stop lumeo-wgm-pipe", sudo=True)
        hostutils.run_command("systemctl disable lumeo-wgm-pipe", sudo=True)
        hostutils.run_command("rm /etc/systemd/system/lumeo-wgm-pipe.service", sudo=True)
        hostutils.run_command("systemctl daemon-reload", sudo=True)
        # Remove shared volume directory
        hostutils.run_command("rm -rf /opt/lumeo/wgm", sudo=True)
        display.output_message("Lumeo Web Gateway Manager has been removed.", status='info')
    else:
        display.output_message("Lumeo Web Gateway Manager is not installed.", status='info')
    
    return

def reset_wgm(silent=False):
    """Reset the password for the Lumeo Web Gateway Manager."""    
    reset = True
    
    if not silent:
        display.print_header("Lumeo Web Gateway Manager Password Reset")
        display.output_message("Resetting the web password will require you to create a new device account via the web interface. "
                       "You should do so immediately, since once reset, anyone can create a new device account.")
        reset = display.prompt_yes_no("Would you like to reset the web password for this device?", "n")
    
    if reset:
        hostutils.run_command("rm -f /opt/lumeo/wgm/db.sqlite", sudo=True)
        hostutils.run_command("docker restart lumeo_wgm", sudo=True)
        display.output_message("Device account reset complete", status='info')

