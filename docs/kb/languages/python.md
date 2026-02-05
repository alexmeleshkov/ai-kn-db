# Python

**Version**: 3.8+
**Website**: https://www.python.org/
**Documentation**: https://docs.python.org/3/

---

## Overview

Python is a high-level, interpreted programming language known for its simplicity and readability. Widely used for web development, data science, automation, and scripting.

---

## Key Features

**Readable Syntax**: English-like syntax, minimal punctuation
**Dynamic Typing**: No type declarations required (optional with type hints)
**Rich Standard Library**: Batteries included for common tasks
**Package Ecosystem**: PyPI with 400k+ packages
**Multi-paradigm**: Object-oriented, functional, procedural
**Cross-platform**: Windows, macOS, Linux

---

## Common Use Cases

- **Web Development**: Django, Flask, FastAPI
- **Data Science**: pandas, NumPy, scikit-learn
- **Machine Learning**: TensorFlow, PyTorch
- **Automation**: Scripts, task automation
- **APIs**: REST, GraphQL backends
- **DevOps**: Ansible, infrastructure scripts

---

## Installation

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS (Homebrew)**:
```bash
brew install python3
```

**Windows**:
- Download from python.org
- Or use Windows Store

**Verify**:
```bash
python3 --version
pip3 --version
```

---

## Virtual Environments

**venv (built-in)**:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install package-name
pip freeze > requirements.txt
```

**Install from requirements**:
```bash
pip install -r requirements.txt
```

---

## Naming Conventions

**Variables and Functions**: `snake_case`
```python
user_name = "Alice"
def calculate_total(items):
    pass
```

**Classes**: `PascalCase`
```python
class UserProfile:
    pass
```

**Constants**: `UPPER_SNAKE_CASE`
```python
MAX_CONNECTIONS = 100
DATABASE_URL = "postgresql://..."
```

**Private**: Prefix with `_`
```python
def _internal_helper():
    pass

class MyClass:
    def __init__(self):
        self._private_var = 42
```

---

## Type Hints (Python 3.5+)

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[int]) -> int:
    return sum(items)

from typing import Optional, Dict, List

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    return {"name": "Alice", "email": "alice@example.com"}
```

---

## Common Libraries by Domain

**Web Frameworks**:
- FastAPI - Modern, async, auto documentation
- Flask - Lightweight, flexible
- Django - Full-featured, batteries included

**Databases**:
- SQLAlchemy - ORM for SQL databases
- psycopg2 - PostgreSQL driver
- pymongo - MongoDB driver

**HTTP Clients**:
- requests - Simple HTTP library
- httpx - Async HTTP client
- aiohttp - Async HTTP server/client

**Testing**:
- pytest - Testing framework
- unittest - Built-in testing
- mock - Mocking library

**Data Science**:
- pandas - Data manipulation
- NumPy - Numerical computing
- matplotlib - Plotting

**Async**:
- asyncio - Built-in async framework
- aiofiles - Async file I/O
- aiohttp - Async web framework

---

## Code Style

**PEP 8** (official style guide):
- 4 spaces for indentation (not tabs)
- Max line length: 79 characters
- 2 blank lines between top-level functions/classes
- 1 blank line between methods

**Imports**:
```python
# Standard library
import os
import sys

# Third-party
import requests
from fastapi import FastAPI

# Local
from .models import User
from .services import auth
```

**Docstrings**:
```python
def calculate_total(items: list[float]) -> float:
    """
    Calculate the total sum of items.

    Args:
        items: List of numbers to sum

    Returns:
        Total sum of all items
    """
    return sum(items)
```

---

## Best Practices

**DO**:
- Use virtual environments (venv)
- Follow PEP 8 style guide
- Write docstrings for functions/classes
- Use type hints in Python 3.8+
- Use f-strings for string formatting
- Handle exceptions explicitly

**DON'T**:
- Don't use `import *`
- Don't use mutable default arguments
- Don't use bare `except:` (catch specific exceptions)
- Don't mix tabs and spaces
- Don't ignore PEP 8 warnings

---

## Common Patterns

### Context Managers
```python
with open('file.txt', 'r') as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_connection():
    conn = connect_db()
    try:
        yield conn
    finally:
        conn.close()
```

### List Comprehensions
```python
# Instead of
squares = []
for x in range(10):
    squares.append(x ** 2)

# Use
squares = [x ** 2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
```

### Decorators
```python
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.2f}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
```

---

## Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

---

## Package Management

**pip**:
```bash
pip install package-name
pip install package-name==1.2.3
pip install -r requirements.txt
pip freeze > requirements.txt
```

**poetry** (modern alternative):
```bash
poetry init
poetry add fastapi
poetry install
poetry run python main.py
```

---

## Tools

**Linting**:
- pylint - Comprehensive linter
- flake8 - Style guide enforcement
- black - Opinionated formatter

**Type Checking**:
- mypy - Static type checker
- pyright - Microsoft's type checker

**Testing**:
- pytest - Testing framework
- coverage - Code coverage

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Code snippets**: See `languages/python/snippets/`
**Technologies often used with**: [[fastapi]], [[postgresql]], [[sqlalchemy]]
