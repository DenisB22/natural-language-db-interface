# Natural Language Database Interface

This repository contains an educational prototype of a Natural Language Interface (NLI) for querying a relational database using a Large Language Model (LLM).

The system allows users to ask questions in natural language, which are automatically translated into safe SQL `SELECT` queries and executed against an SQLite database. The project demonstrates how modern LLMs can be integrated into a traditional client–server architecture while preserving control, predictability, and data safety.

---

## Project Goals

The main objectives of this project are:
- to explore the use of Large Language Models for natural language interaction with structured data;
- to design a controlled and secure architecture for SQL query generation;
- to demonstrate a practical prototype suitable for small and medium-sized applications;
- to analyze limitations related to scalability and cost.

---

## System Overview

The system follows a classic client–server architecture and consists of the following main components:

- **Web Client**  
  A lightweight web interface that allows users to enter questions in natural language and view the generated SQL queries and results.

- **Backend Service (FastAPI)**  
  Handles user requests, prepares prompts for the LLM, validates generated SQL queries, executes them against the database, and returns structured results.

- **LLM Integration Module**  
  Uses an external API to generate SQL queries based on the database schema and the user’s question.

- **SQL Validation Layer**  
  Ensures that only safe `SELECT` queries are executed and blocks potentially dangerous operations.

- **SQLite Database**  
  Stores synthetic sample data used for demonstration and testing purposes.

---

## Key Features

- Natural language to SQL query generation
- Deterministic query generation (`temperature = 0`)
- Strict SQL validation (SELECT-only)
- REST API backend implemented with FastAPI
- Web-based frontend
- SQLite database with synthetic data
- Reproducible database setup via seed script

---

## Project Structure

```
natural-language-db-interface/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── llm.py
│   │   ├── validator.py
│   │   ├── llm_debug/            # optional LLM request/response dumps (git-ignored)
│   │   └── ...
│   ├── data/
│   │   └── ecommerce.db          # generated locally
│   ├── scripts/
│   │   └── seed_db.py            # database creation and seeding
│   └── ...
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Database Setup

The SQLite database is **not included** in the repository.  
It must be generated locally using the provided seed script.

### Step 1: Create and seed the database

From the project root directory, run:

```bash
python backend/scripts/seed_db.py
```

This script will:
- create the SQLite database file;
- create all required tables;
- populate the tables with synthetic sample data.

After execution, the database file will be located at:

```
backend/data/ecommerce.db
```

---

## Running the Application

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start the backend service

```bash
uvicorn backend.app.main:app --reload
```

The backend API will be available at:

```
http://127.0.0.1:8000
```

### Step 4: Open the web interface

Open the frontend in your browser (depending on setup), for example:

```
frontend/index.html
```

You can now enter natural language questions and view the generated SQL queries and results.

---

## LLM Configuration

The system uses an external Large Language Model accessed via API.  
The model is configured to:

- generate only valid JSON output;
- produce a single SQL `SELECT` query per request;
- avoid any data-modifying SQL operations;
- operate with `temperature = 0` to ensure deterministic and reproducible results.

All domain-specific information is provided dynamically through the prompt, without fine-tuning the model.

---

## Notes on Scalability

The presented approach is well suited for prototypes and small to medium-sized systems.  
As the complexity of the database schema grows, the size of the prompt and the frequency of LLM calls may increase operational costs and latency. In large-scale systems, additional optimization strategies would be required.

---

## Disclaimer

- API keys and environment variables are **not included** in the repository.
- Debug files and generated artifacts are excluded via `.gitignore`.
- The project is intended for **educational and experimental purposes**.

---

## License

This project is provided for academic use and experimentation.
