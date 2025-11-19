from netmiko import ConnectHandler
import config_data as config_data
import difflib

#User login should moved to a cache or env
user = {
    'username': 'admin',      # Replace with your router's username
    'password': 'Lucasersej123',   # Replace with your router's password
    'secret': 'Lucasersej123',       # Replace with your router's enable secret
}

def connect_to_device(device):
    # Establish a connection to the device
    net_connect = ConnectHandler(**device)
    return net_connect

def get_run(net_connect):
    # Enter enable mode
    net_connect.enable()

    # Send the run command to the device
    output = net_connect.send_command("show run | begin version")
    
    return output

def disconnect_from_device(net_connect):
    # Disconnect from the device
    net_connect.disconnect()

def create_host(host, devicetype, user):
    # Create the device dictionary
    device = {
        'device_type': devicetype,
        'host': host,
        'username': user['username'],
        'password': user['password'],
        'secret': user['secret'],
        'global_delay_factor': 2,
    }
    return device

def compare_config(output, config, name):
    # Compare the running configuration with the desired configuration
    diff = '\n' + '\n'.join(difflib.ndiff(config.splitlines(), output.splitlines()))

    return {name: diff}
            

def update_data(device_name, newconfig):
    # Read the current content of config_data.py
    with open('config_data.py', 'r') as file:
        lines = file.readlines()

    # Find the device configuration and update it
    device_found = False
    for i, line in enumerate(lines):
        if f'"devicename": "{device_name}"' in line:
            device_found = True
        
        if device_found:
        # Find the start and end of the config block
            start_index = i
            while not lines[start_index].strip().startswith('"config": """'):
                start_index += 1
            end_index = start_index
            while not lines[end_index].strip().endswith('end'):
                end_index += 1
            # Update the config block
            lines[start_index:end_index + 1] = [f'    "config": """{newconfig}']
            break

    if not device_found:
        print(f"Device {device_name} not found in config_data.py")
        return

    # Write the updated content back to config_data.py
    with open('config_data.py', 'w') as file:
        file.writelines(lines)

    print(f"Device {device_name} configuration updated successfully.")
