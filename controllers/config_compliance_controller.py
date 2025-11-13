from helpers.config_helper import (
    connect_to_device, get_run, 
    disconnect_from_device, create_host, 
    compare_config, user,
    update_data
    )
from config_data import config_data

def controller_get_live_config(ip: str) -> dict:
    """Gets Live config data"""
    for device in config_data:
        if device["host"] == ip:
            device_connection = create_host(ip, device["devicetype"], user)
            connection = connect_to_device(device_connection)
            config = get_run(connection)
            disconnect_from_device(connection)
            return config
    
    
def controller_get_config_data() -> list:
    """Gets config from stored data"""
    return config_data

def controller_update_config_data(ip: str) -> dict:
    """Updates the stored config"""
    for device in config_data:
        if device["host"] == ip:
            device_connection = create_host(ip, device["devicetype"], user)
            connection = connect_to_device(device_connection)
            config = get_run(connection)
            update_data(device["devicename"], config)
            
    
def controller_get_uncompliant_config() -> dict:
    """Gets the uncompliant config by comparing live with desired"""
    diffs = []
    for device in config_data:
        device_connection = create_host(device["host"], device["devicetype"], user)
        connection = connect_to_device(device_connection)
        config = get_run(connection)
        diffs.append(compare_config(config, device["config"], device["devicename"]))
    return diffs
        