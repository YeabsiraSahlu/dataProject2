from flask import Flask, request, jsonify
from dateutil import parser
from fuzzywuzzy import process
import yfinance as yf
import sqlite3
from ticker_map import ticker_map
import datetime

app = Flask(__name__)

# Get stock data from SQLite for AAPL only
def get_stock_price_by_data(date):
    connection = sqlite3.connect('db/finance_data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stock_data WHERE Date = ?", (date,))
    result = cursor.fetchall()
    connection.close()
    return result

# Match user input to known company names using fuzzy match (no API call)
def extract_ticker(user_input):
    user_input = user_input.lower()
    best_match, score = process.extractOne(user_input, ticker_map.keys())
    if score > 80:
        return ticker_map[best_match]
    return None

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    ticker = extract_ticker(user_input)

    if not ticker:
        return jsonify({"error": "Could not identify a valid stock. Try 'Apple', 'Tesla', etc."})

    # Handle real-time requests like 'today' or 'now'
    if "now" in user_input.lower() or "today" in user_input.lower():
        try:
            today = datetime.datetime.today().strftime("%Y-%m-%d")
            live_data = yf.Ticker(ticker).history(start=today, end=today)

            if live_data.empty:
                return jsonify({"error": f"No data found for {ticker} today."})

            row = live_data.iloc[0]
            return jsonify({
                "Ticker": ticker,
                "Date": today,
                "Open": row["Open"],
                "High": row["High"],
                "Low": row["Low"],
                "Close": row["Close"],
                "Volume": row["Volume"],
                "Source": "Live API (via history)"
            })
        except Exception as e:
            return jsonify({"error": f"Live price fetch failed: {str(e)}"})

    # Handle historical queries
    try:
        parsed_date = parser.parse(user_input, fuzzy=True).date()
        date = parsed_date.strftime("%Y-%m-%d")

        if ticker == "AAPL":
            result = get_stock_price_by_data(date)
            if result:
                row = result[0]
                return jsonify({
                    "Ticker": "AAPL",
                    "Date": row[0],
                    "Open": row[1],
                    "High": row[2],
                    "Low": row[3],
                    "Close": row[4],
                    "Volume": row[5],
                    "Source": "Local SQLite DB"
                })
            else:
                return jsonify({"error": f"No historical data found for AAPL on {date}."})
        else:
            hist_data = yf.Ticker(ticker).history(start=date, end=date)
            if not hist_data.empty:
                row = hist_data.iloc[0]
                return jsonify({
                    "Ticker": ticker,
                    "Date": date,
                    "Open": row["Open"],
                    "High": row["High"],
                    "Low": row["Low"],
                    "Close": row["Close"],
                    "Volume": row["Volume"],
                    "Source": "Live API (Historical)"
                })
            else:
                return jsonify({"error": f"No data found for {ticker} on {date}."})

    except Exception as e:
        return jsonify({"error": "Could not understand the date. Try 'August 1, 2023' or '2023-08-01'."})

if __name__ == '__main__':
    app.run(debug=True)
