from fastapi import FastAPI
from config.env import settings
from config.logger import setup_logging
from controllers.exoplanet_controller import router as exoplanet_router

setup_logging()

app = FastAPI()

# Include routers
app.include_router(exoplanet_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": f"app is up and running on port {settings.port}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
