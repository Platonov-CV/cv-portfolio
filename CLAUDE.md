# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a portfolio project that aggregates multiple ML/AI sub-projects under a single FastAPI backend. The project is in the early planning/scaffolding stage.

## Planned Architecture

- **Aggregator backend**: A single FastAPI application that acts as an entry point to all sub-projects
- **Sub-projects as git submodules**: Each ML project is its own repository, included here via `git submodules`
- **Containerized services**: Each sub-project gets a lightweight FastAPI wrapper and is containerized (Docker). Inference requests are routed to the appropriate container
- **Frontend**: A fullstack web UI served alongside or separately from the FastAPI backend

## Portfolio Projects

### 1. FPV Trick Detection
Detects and classifies FPV drone tricks from video. Uses the custom CNN-GRU model (lightweight, CPU-friendly).

### 2. Real-time Box Size Measurement
Measures physical box dimensions in real time using a webcam feed. Uses YOLO (runs on client/edge) and DepthAnything metric depth estimation. A working inference server (CNN-GRU based) is already implemented.

### ML Models in scope

| Model | Used in | Notes |
|---|---|---|
| YOLO | Box measurement | Runs on client/edge device |
| DepthAnything (metric) | Box measurement | Heavy — CPU inference may be slow |
| Custom CNN-GRU | FPV trick detection | Lightweight, fine on CPU |

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000
```

## Docker

```bash
# build and run just the portfolio frontend
docker compose up --build

# when project containers are ready, add them to docker-compose.yml
# under `services:` and link them to the portfolio service via environment variables
```

## Key Decisions

- **Hosting target**: Evaluate whether all projects can run on a plain CPU server, or whether GPU is required. Test locally with Ollama + Qwen 8B as a benchmark.
- **Inter-service communication**: Containers expose HTTP (FastAPI), and the aggregator calls them via internal requests.
- **Submodule workflow**: Add sub-projects with `git submodule add <url>`. Initialize with `git submodule update --init --recursive`.
