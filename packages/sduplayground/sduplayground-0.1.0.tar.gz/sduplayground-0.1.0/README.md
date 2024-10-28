# My Library

A Python library for automating tasks using Playwright.

## Installation

```bash
pip install my_library


from my_library.main import schedule_task, login_task
import datetime

# Login and save cookies
login_task('username', 'password', 'cookies.json')

# Schedule a task
schedule_task('cookies.json', 10, datetime.time(12, 29, 55))



### 4. `my_library/__init__.py`

```python
# This file can be empty or contain package-level docstring