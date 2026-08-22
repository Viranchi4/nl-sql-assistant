# 🧠 Natural Language to SQL Assistant (MySQL)

A local Natural Language → SQL assistant that converts user questions into SQL queries and executes them on a MySQL database. Built with Python and a lightweight LLM-style mapping pipeline.

---

## 📌 Overview
This project allows users to ask questions like:

> "Show me all customers from France who purchased in 2023"

The system:
1. Converts the natural language question into a valid SQL query  
2. Executes the query on a local MySQL database  
3. Returns the results in a clean, readable format  

Everything runs locally — no cloud APIs, no external dependencies.

---

## ⚙️ Tech Stack
- Python 3.10+
- MySQL (local instance)
- SQLAlchemy + mysql-connector-python
- Lightweight NL→SQL mapping logic
- VS Code for development

---

## 🚀 Features
- Natural language → SQL conversion  
- Secure, parameterized SQL execution  
- Sample database with `customers`, `orders`, `products`  
- Modular Python code structure  
- Easy to extend with more tables or logic  

---

## 📂 Planned Project Structure
```text
nl-to-sql-assistant/
│
├── data/
│   └── schema.sql
│
├── src/
│   ├── nl_to_sql.py
│   ├── query_executor.py
│   └── app.py
│
├── tests/
│   └── test_queries.py
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run (will be updated as we build)
```bash
pip install -r requirements.txt
python src/app.py

##👤 Author
Viranchi Parikh  
Data Scientist | AI/ML Engineer
LinkedIn: https://www.linkedin.com/in/viranchi-parikh-3aba0019a/
