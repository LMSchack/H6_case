from fastapi import FastAPI
from routes.config_compliance_route import router as config_compliance_router

app = FastAPI(
    title = "Config Compliance API",
    version = "1.0.0",
    docs_url = "/docs"
)

app.include_router(config_compliance_router, prefix="/config_compliance_route", tags=["config_compliance"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)