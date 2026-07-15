# Online School Backend

This repository contains the backend foundation for an online school platform built with Python and FastAPI. The project is structured as a serious, domain-driven application, but it is not yet fully implemented. At this stage, it should be viewed as an architectural foundation and an evolving work in progress rather than a complete product.

## Project Overview

The goal of this project is to provide a scalable and maintainable backend for managing educational content such as courses, modules, lectures, and sections. The design emphasizes clear separation of concerns, business rules encapsulated in the domain layer, and use-case-driven application logic.

## Current Status

The codebase already includes several important building blocks:

- a FastAPI application entry point
- domain entities for core educational concepts
- use cases for course creation, retrieval, and update flows
- repository abstractions for persistence boundaries
- structured error handling and validation

However, the project is still incomplete in several important areas:

- API routes and request/response schemas are not yet fully wired up
- persistence and database integration are still being developed
- authentication and authorization are not implemented yet
- full end-to-end business flows remain to be completed
- tests and deployment automation are still in progress

## Architecture

The project follows a layered structure:

- Application layer: use cases, DTOs, repository interfaces, and application-specific exceptions
- Domain layer: business entities and validation rules
- Infrastructure layer: configuration, database integration, and persistence implementations
- Presentation layer: API schemas and exception handlers

This structure is intended to make the system easier to evolve as the platform grows.

## Technology Stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- SQLite for local development

## Project Structure

```text
app/
  application/     # use cases, interfaces, DTOs, application exceptions
  domain/          # business entities and domain rules
  infrastructure/  # config, database access, persistence-related code
  presentation/   # API schemas and handlers
  main.py          # FastAPI application entry point
```

## Getting Started

### Prerequisites

- Python 3.11 or newer
- pip

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Configuration

The application uses environment variables for configuration. A typical development setup may include values such as:

```bash
export APP_ENV=development
export APP_TITLE="FastAPI Education"
export APP_DEBUG=true
export API_PREFIX=/api
export DATABASE_URL="sqlite+aiosqlite:///./fastapi_education.db"
export DATABASE_ECHO=false
```

If these variables are not provided, the application uses default values defined in the configuration module.

### Running the Application

```bash
uvicorn app.main:app --reload
```

## Roadmap

Planned next steps include:

- completing the API layer for courses, modules, lectures, and sections
- implementing repository-backed persistence and database migrations
- adding authentication and user management
- expanding validation and domain rules
- adding automated tests and CI/CD workflows

## Note

This repository represents a strong architectural starting point for a serious education platform, but it is still a work in progress. The current implementation should be treated as an early foundation that will continue to evolve.
