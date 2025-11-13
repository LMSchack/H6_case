from fastapi import APIRouter
from fastapi import Request
from controllers.config_compliance_controller import (
    controller_get_live_config,
    controller_get_config_data,
    controller_update_config_data,
    controller_get_uncompliant_config
)

router = APIRouter()

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
    """Get Live config from a device using ip"""
    
    return {"data": controller_get_config_data()}

@router.put("/update_config_data_{ip}")
async def update_config_data(
    request: Request, ip: str
) -> dict:
    """Get Live config from a device using ip"""
    
    return {ip: controller_update_config_data(ip)}

@router.get("/get_uncompliant_config")
async def get_uncompliant_config(
    request: Request
) -> dict:
    """Get Live config from a device using ip"""
    
    return {"data": controller_get_uncompliant_config()}