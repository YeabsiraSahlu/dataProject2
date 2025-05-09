Finance Chatbot Project
Created by: Miky Asmare, Soliyana Yohannes, Nathan Ressom, and Yeabsira Sahlu

Overview
This project demonstrates the development of a finance chatbot using Flask that integrates both local and live data sources to provide historical and real-time stock information. The project fulfills the requirements for combining data from an ETL pipeline and a live API and includes parsing logic, error handling, and deployment readiness.

Project Structure
Source 1 (Live API):
Real-time stock data is fetched using the yfinance library. This data includes the most current open, high, low, close, and volume values for the requested stock ticker. The chatbot intelligently routes to this source when the user asks about today’s or current prices, or if the ticker is not handled locally.

Source 2 (SQLite DB via ETL):
Historical stock data for AAPL is retrieved from Yahoo Finance through yfinance, cleaned, and inserted into a local SQLite database using a custom ETL script.

Transformation:
The raw data extracted via yfinance is cleaned by resetting the index, selecting relevant columns, and standardizing date formats to ensure compatibility with SQL storage and date parsing.

Loading:
Transformed data is written into a stock_data table inside finance_data.db using pandas.to_sql().

Ticker Mapping & Validation:
The chatbot uses a mapping dictionary (ticker_map.py) along with fuzzywuzzy string matching to extract and validate ticker names from user input. Validated tickers are checked using yfinance.Ticker().info.

Query Routing Logic:
The chatbot determines which data source to use based on user input. It defaults to the local DB for AAPL queries with a specific date, and falls back to the live API for other tickers or if data is not found locally.

Files
app.py – Flask app with the /chat route. Handles all user input parsing, routing, and responses.

etl/etl.py – Extracts AAPL historical data, transforms it, and loads it into a SQLite database.

db/finance_data.db – Local SQLite database storing AAPL historical stock data.

ticker_map.py – Dictionary that maps common company names to ticker symbols.

requirements.txt – Lists all Python packages used in the project.

.gitignore – Prevents .db and venv/ files from being tracked in version control.

Features
Handles fuzzy name matching (e.g., "apple", "tesla") and converts them to valid tickers.

Accepts natural language date formats (e.g., "August 1, 2023").

Supports both local historical and live API stock price queries.

Includes structured error handling for missing tickers, bad dates, or unavailable data.

Modular project structure ready for deployment and future expansion (e.g., Discord bot or Gemini LLM integration).

