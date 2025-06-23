# 🚀 FastAPI + Podman App

A professional-grade, containerized **FastAPI** application leveraging **Podman** for secure, rootless development and deployment.

---

## 🌟 Key Features

- 🔐 **User Authentication with JWT**
  - Secure user registration and login
  - Token-based access to protected endpoints

- ✅ **Task Management System**
  - Authenticated CRUD operations for managing personal tasks
  - Supports creation, update (including status), and deletion
  - Clean schema validation with Pydantic v2

- ⚡ **Redis Caching for Task Listing**
  - Per-user task list is cached for high performance
  - Cache auto-invalidates on task create/update/delete
  - Built-in logging to trace whether data came from Redis or the database

- 🐍 Built with Python 3.11 and FastAPI
- 📦 Containerized using **Podman** (rootless alternative to Docker)
- 🧩 Orchestrated via `podman-compose`
- 🧪 Easily testable with `curl` or Postman

---

## 💼 Why This Project Matters

This project demonstrates hands-on expertise in:

- Designing and building RESTful APIs using FastAPI
- Implementing secure authentication and token-based access
- Integrating caching strategies using Redis
- Working with asynchronous, containerized environments using **Podman**
- Writing production-ready Python code with modern tooling


