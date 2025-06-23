# 🚀 FastAPI + Podman App

A professional-grade, containerized **FastAPI** application built with modern Python practices, leveraging **Podman** for secure, rootless development and orchestration.

---

## 🌟 Core Features

### 🔐 Secure User Authentication (JWT)
- User registration and login with password hashing (`bcrypt`)
- OAuth2-compliant access via JWT tokens
- Protected endpoints for authenticated users

### ✅ Task Management System
- Full CRUD support for managing personal tasks
- Supports task title, description, and completion status
- Ensures task ownership and user-level data separation
- Clean schema validation using **Pydantic v2**

### ⚡ Redis-Based Caching
- Per-user task listing is cached for performance
- Automatic cache invalidation on task creation, update, or deletion
- Logging to indicate whether data is served from cache or database

---

## 🛠️ Technical Highlights

- Built with **Python 3.11** and **FastAPI**
- Modular and testable API structure
- Uses **Podman** and `podman-compose` for rootless container orchestration
- CI/CD ready: integrates with GitHub Actions and Docker Hub for image publishing
- **Kubernetes-Ready**: Production-grade `Deployment` and `Service` files for **Minikube**
  - FastAPI, PostgreSQL, and Redis deployed as independent services
  - Environment variables managed via Kubernetes `Secrets` and `ConfigMaps`
  - Resource limits defined for optimal scheduling and cluster health

---

## 💼 Why This Project Matters

This project demonstrates hands-on capabilities in:

- Designing secure, token-based API systems
- Implementing efficient caching layers using Redis
- Deploying containerized applications with modern, rootless tooling
- Writing clean, production-ready Python backend services
- **Running full-stack microservices locally using Minikube and Kubernetes**
