# 🧠 Natural Language to SQL Assistant (MySQL)

A local LLM-powered Text-to-SQL application that converts natural-language questions into safe, executable MySQL queries.

The project uses locally hosted Qwen2.5-Coder models through Ollama, so no paid LLM API or cloud service is required.

---

## 📌 Overview

The application allows users to query a relational database using natural language.

For example:

> Show the top 5 customers by total spending.

The system dynamically inspects the database schema, provides relevant schema and database-value context to a local LLM, validates the generated SQL, and executes only safe read-only queries.

The pipeline is:

```text
Natural-language question
        |
        v
Database schema + value context
        |
        v
Local LLM (Ollama)
        |
        v
Generated SQL
        |
        v
SQL and schema validation
        |
        v
MySQL execution
        |
        v
Query results
```

If the generated SQL fails schema validation or database execution, the system can make bounded correction attempts using the original question, schema context, and error information.

---

## ⚙️ Tech Stack
- Python 3.10+
- MySQL 8 (local instance)
- Ollama
- Qwen2.5-Coder 3B and 7B
- mysql-connector-python
- SQLGlot
- python-dotenv
- pytest
- Git and GitHub
- VS Code for development

---

## 🚀 Features
- Local LLM-based Natural Language to SQL generation
- Qwen2.5-Coder models served through Ollama
- Configurable local LLM model through environment variables
- Dynamic MySQL schema inspection
- Database value grounding for categorical fields
- Foreign-key-aware join generation
- SQLGlot-based SQL parsing and validation
- Read-only query enforcement
- Table and column reference validation
- Bounded SQL correction and retry workflow
- CLI interface for interactive querying
- Automated Text-to-SQL evaluation using reference query results
- Holdout benchmark for testing generalization
- Reproducible model comparison between 3B and 7B models
- Unit tests for generation, validation and pipeline behaviour

---

## 📊 Evaluation and Model Comparison

The project includes an evaluation framework that executes generated SQL and compares the returned results against trusted reference queries.

This distinguishes between:

- **Execution success:** whether the generated SQL executes successfully.
- **Result accuracy:** whether the generated query returns the expected result.

A separate holdout dataset is used to test questions that were not used while refining the prompt.

### 📈 Holdout Benchmark Results

| Model | Questions | Execution Success | Result Accuracy |
|---|---:|---:|---:|
| Qwen2.5-Coder 3B | 5 | 80% | 80% |
| Qwen2.5-Coder 7B | 5 | 100% | 100% |

The 3B model successfully handled the easy and medium holdout questions but failed on a complex five-table join. The 7B model generated the correct query for all five holdout questions without requiring correction attempts.

These results apply specifically to the included 5-question holdout benchmark and sample database; they are not intended as a general Text-to-SQL accuracy claim.

Evaluation reports are stored in:

```text
evaluation/results/
├── holdout_questions__qwen2.5-coder_3b.json
└── holdout_questions__qwen2.5-coder_7b.json
```

## 📂 Project Structure

```text
nl-sql-assistant/
│
├── data/
│   ├── schema.sql
│   └── seed.sql
│
├── evaluation/
│   ├── questions.json
│   ├── holdout_questions.json
│   ├── evaluate.py
│   └── results/
│
├── src/
│   └── nl_sql_assistant/
│       ├── __init__.py
│       ├── cli.py
│       ├── database.py
│       ├── pipeline.py
│       ├── schema.py
│       │
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── ollama_client.py
│       │   └── prompts.py
│       │
│       └── sql/
│           ├── __init__.py
│           ├── executor.py
│           ├── generator.py
│           └── validator.py
│
├── tests/
│   ├── conftest.py
│   ├── test_generator.py
│   ├── test_pipeline.py
│   └── test_validator.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---
## ⚙️ Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install the project

```powershell
python -m pip install -e ".[dev]"
```

### 3. Configure the database connection

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Update .env with your local MySQL credentials:
SA_DB_HOST=127.0.0.1
SA_DB_PORT=3306
SA_DB_USER=root
SA_DB_PASSWORD=your_password
SA_DB_NAME=sales_analytics_db
SA_DB_POOL_SIZE=3

### 4. Create and seed the sample database

Open MySQL:

```powershell
mysql -u root -p
```

From the MySQL prompt, run:
SOURCE data/schema.sql;
SOURCE data/seed.sql;

This creates the sample sales analytics database with:
- customers
- categories
- products
- orders
- order_items

### 5. Install Ollama and download a model

Install Ollama for your operating system, then download a local model:

```powershell
ollama pull qwen2.5-coder:7b
```

The smaller model can also be used:

```powershell
ollama pull qwen2.5-coder:3b
```

The application defaults to the 3B model unless another model is configured

To use the 7B model in Powershell:

```powershell
$env:SA_OLLAMA_MODEL="qwen2.5-coder:7b"
```

---

## ▶️ Run the Assistant

Start the interactive CLI:

```powershell
python -m nl_sql_assistant.cli
```

Example:
Ask a question: Show the top 5 customers by total spending

Generated SQL:
SELECT ...

Results:
...

Type exit or quit to close the application.

---

## 🧪 Run Tests

```powershell
pytest -v
```

The current automated test suite contains 18 tests covering SQL generation, validation, schema checking, correction behaviour and pipeline execution.

---

## 📊 Run Evaluation

Run the standard benchmark:

```powershell
python evaluation/evaluate.py
```

Run the holdout benchmark:

```powershell
python evaluation/evaluate.py --dataset holdout_questions.json
```

To evaluate a specific Ollama model:

```powershell
$env:SA_OLLAMA_MODEL="qwen2.5-coder:7b"
python evaluation/evaluate.py --dataset holdout_questions.json
```

Evaluation reports are written to evaluation/results/

---

## ▶️ How to Run (will be updated as we build)
```bash
python src/app.py
```
---

## 👤 Author
Viranchi Parikh  
Data Scientist | AI/ML Engineer
LinkedIn: https://www.linkedin.com/in/viranchi-parikh-3aba0019a/
