# Natural Language Database Interface

This repository contains an educational prototype of a Natural Language Interface (NLI) for querying a relational database using a Large Language Model (LLM).

The system allows users to ask questions in natural language, which are automatically translated into safe SQL SELECT queries and executed against an SQLite database.

## Overview

The project demonstrates how modern LLMs can be integrated into a traditional client–server architecture to provide a natural language interface to structured data, while preserving control, security, and predictability.

## Main Features

- Natural language to SQL query generation
- Safe query execution (SELECT-only validation)
- Backend REST API implemented with FastAPI
- Web-based client interface
- SQLite database with synthetic data
- External LLM integration via API

## Architecture

The system consists of:
- Web frontend (HTML, CSS, JavaScript)
- Backend service (FastAPI)
- LLM-based SQL generation module
- SQL validation and execution layer
- SQLite relational database

## Database Setup

The project uses an SQLite database with synthetic data for demonstration purposes.
The database file is not included in the repository and must be generated locally.

### Step 1: Create the database

From the project root, run the database initialization script:

```bash
python backend/scripts/seed_db.py

## Running the Project

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
