from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os
from starlette_exporter import PrometheusMiddleware, handle_metrics
from app.models import BaseSQL, engine
from app import routers
from starlette.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler

from app.services.user import process_subscriptions
from app.services.scheduler import scheduler

app = FastAPI(
    title="Crédit ESIEE",
    description="API de la meilleure banque de l'ESIEE",
    version="0.0.1",
)

app.include_router(routers.ConfigRouter)
app.include_router(routers.UserRouter)
app.include_router(routers.AdminRouter)
app.include_router(routers.AuthRouter)

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)


### Part added using ChatGPT. It's used to process the subscription, so the amount is automatically transfer between 2 accounts every minutes.

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(process_subscriptions, "interval", minutes=1)
    scheduler.start()  # Start the APScheduler on app startup

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)  # Gracefully shut down the scheduler
   
    
### Part added using ChatGPT. It's used to avoid error while deleting account, to make sure that the user have to reconnect and doesn't cause error.

invalidated_tokens = set()  # In-memory storage for invalidated tokens (use Redis/db in production)

@app.middleware("http")
async def check_cleared_token(request: Request, call_next):
    """
    Middleware to check if the token is invalidated.
    """
    # Extract the Authorization token
    token = request.headers.get("Authorization")

    # If the token is in the invalidated set, raise an HTTPException
    if token in invalidated_tokens:
        return JSONResponse(
            status_code=401,
            content={"detail": "Connection invalidated. Please reconnect."},
        )
    
    # Process the request and retrieve the response
    response = await call_next(request)

    # Check if the response includes the "Clear_token" header
    if response.headers.get("Clear_token") == "true":
        invalidated_tokens.add(token)  # Mark the token as invalidated

    return response