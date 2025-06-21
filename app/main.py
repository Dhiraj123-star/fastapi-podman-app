from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .routes import user, task

# Initialize DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="📋 Task Manager API",
    description="A simple JWT-authenticated task management API using FastAPI + PostgreSQL + Redis + Podman",
    version="1.0.0"
)

# CORS config (allow all for testing/demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user.router)
app.include_router(task.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + Podman Task Manager!"}
