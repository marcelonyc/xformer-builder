import os

os.environ["RUN_MODE"] = "dev"

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app import app
import os


@pytest.mark.asyncio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_auth_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth")  # Adjust the endpoint as necessary
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_xformers_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/xformers"
        )  # Adjust the endpoint as necessary
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_filemanager_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/filemanager"
        )  # Adjust the endpoint as necessary
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_event_trigger_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/eventmanager"
        )  # Adjust the endpoint as necessary
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_filexchange_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/filexchange"
        )  # Adjust the endpoint as necessary
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_system_router():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/platform"
        )  # Adjust the endpoint as necessary
    assert response.status_code == 200
