# teleparser
# Telegram Web Monitor Bot

An asynchronous Python Telegram bot that monitors websites for custom products, items, or vacancies using multiple keywords, and sends instant alerts when matches or price changes are detected.

## Features
* **Multi-Keyword Support:** Users can input multiple keywords separated by commas (e.g., `laptop, ram, ssd`).
* **Asynchronous Engine:** Built on `aiogram` and `asyncio` for high performance.
* **Duplicate Prevention:** Uses an `sqlite3` database via `aiosqlite` to ensure notifications for the same item price are only sent once.
* **FSM (Finite State Machine):** Clean, step-by-step user onboarding flow.

## Tech Stack
* **Language:** Python 3.10+
* **Framework:** `aiogram` (v3.x)
* **Parser:** `BeautifulSoup4` + `requests`
* **Database:** `sqlite3` (`aiosqlite`)
* **Environment:** `python-dotenv`

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/azizs10/teleparser.git](https://github.com/azizs10/teleparser.git)
   cd teleparser
## Run the main.py file:
   ```bash
   python main.py
