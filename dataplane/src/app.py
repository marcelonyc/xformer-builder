from contextlib import asynccontextmanager
from typing import AsyncGenerator

# import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from config.app_config import settings
from database import database
from auth.router import router as auth_router
from xformers.router import router as xformers_router
from filemanager.router import router as filemanager_router
from filexchange.router import router as filexchange_router
import os


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown
    await database.disconnect()


app = FastAPI(title="Xformer Builder API", lifespan=lifespan)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# app.include_router(services_router, prefix="/services", tags=["Services"])
app.include_router(auth_router, tags=["App token Login endpoint"])

app.include_router(xformers_router, tags=["Xformer manager"])

app.include_router(filemanager_router, tags=["File manager"])

# WARNING - These routes are not protected by the auth service
app.include_router(filexchange_router, tags=["File Xchange"])
