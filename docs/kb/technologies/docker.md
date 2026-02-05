# Docker

**Category**: Containerization / Deployment
**Website**: https://www.docker.com/
**Documentation**: https://docs.docker.com/

---

## Overview

Docker is a platform for developing, shipping, and running applications in containers. Containers package code and dependencies together, enabling consistent deployment across environments.

---

## Key Concepts

**Images**: Read-only templates for creating containers
**Containers**: Runnable instances of images
**Dockerfile**: Text file with instructions to build an image
**Docker Compose**: Tool for defining multi-container applications

---

## Common Use Cases

- **Development consistency**: Same environment for all developers
- **Microservices**: Each service in its own container
- **CI/CD**: Build once, deploy anywhere
- **Isolation**: Dependencies don't conflict with host system

---

## Prerequisites

**System Requirements**:
- Linux, macOS, or Windows with WSL2
- Minimum 4GB RAM
- 20GB disk space

**Installation**:
- Docker >= 24.0
- Docker Compose >= 2.0 (included with Docker Desktop)

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Code snippets**: See `snippets/*/docker/`
**Technologies often used with**: [[postgresql]], [[nginx]]
**People**: [[dima-efremov]]
