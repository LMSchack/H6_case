from fastapi import APIRouter
from fastapi import Request
from controllers.config_compliance_controller import (
    controller_get_live_config,
    controller_get_config_data,
    controller_update_config_data,
    controller_get_uncompliant_config
)
#This tells fastapi that this is a route and what to do with it
router = APIRouter()

#This loads every endpoint and what it should do when its run
#and what it should return

@router.get("/get_live_config_{ip}")
async def get_live_config(
    request: Request, ip: str
) -> dict:
    """Get Live config from a device using ip"""
    
    return {ip: controller_get_live_config(ip)}

@router.get("/get_config_data")
async def get_config_data(
    request: Request
) -> dict:
    """Gets the data stored in the config data file"""
    
    return {"data": controller_get_config_data()}

@router.put("/update_config_data_{ip}")
async def update_config_data(
    request: Request, ip: str
) -> dict:
    """Updates the stored config with the live config"""
    
    return {ip: controller_update_config_data(ip)}

@router.get("/get_uncompliant_config")
async def get_uncompliant_config(
    request: Request
) -> dict:
    """Gets both stored and live config and compares and give the differens back"""
    
    return {"data": controller_get_uncompliant_config()}