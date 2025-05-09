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


Finance Chatbot Deployment Summary (2 Pages)

To deploy the Flask-based finance chatbot assistant, we used Google Cloud Platform (GCP), specifically its Compute Engine service, which allows users to run virtual machines on Google infrastructure. The primary goal of this deployment was to make the chatbot accessible from the public internet and ensure it meets the project requirements of responding to user queries using both live financial APIs and a local database populated via an ETL pipeline.

The deployment process began by creating a new Virtual Machine (VM) instance through the Compute Engine console. During setup, we selected a basic Ubuntu image and enabled both HTTP and HTTPS traffic so that the Flask application could later be reached through a web browser. After the VM instance was successfully launched, we connected to it using the SSH terminal provided by GCP.

Inside the virtual machine, we started by installing essential system dependencies. These included Python (to run the Flask app), Git (to pull down the project from GitHub), and pip (Python's package installer). Once those tools were installed, we cloned our chatbot project repository directly from GitHub to the VM using the git clone command. This ensured that the latest version of our codebase, including all modules and scripts, was available for execution on the remote server.

With the project files in place, we created a Python virtual environment using python3 -m venv venv to isolate dependencies from the system Python installation. After activating the virtual environment with source venv/bin/activate, we ran pip install -r requirements.txt to install all the necessary libraries, including Flask, yfinance, pandas, sqlite3, and any additional modules used by the chatbot.

The Flask application was then configured to run on 0.0.0.0, allowing it to listen on all available network interfaces, and specifically bound to port 5000. This setup is essential for exposing the app beyond localhost so that it can respond to requests from the public internet. To run the application persistently, we used either nohup or screen so the server would remain active even after exiting the SSH session.

After launching the Flask app, we visited the public IP address assigned to our VM followed by port 5000 (e.g., http://34.123.45.67:5000/chat) to test the chatbot in a browser and via Postman. We confirmed that the chatbot could process both real-time queries using the yfinance API (e.g., "price of Apple today") and historical queries against the SQLite database populated by the ETL script (e.g., "price of AAPL on 2023-08-01").

Once confirmed, we updated the README.md file in the GitHub repository to include the public URL of the deployed chatbot. This fulfills the accessibility requirement and makes the bot easily testable by others.

In conclusion, deploying this chatbot to GCP involved setting up a secure and functional cloud environment, installing the necessary software stack, configuring network settings for public access, and validating both API and local database functionality. The project is now successfully live, accessible online, and fully integrated with real-time and historical stock data sources.

