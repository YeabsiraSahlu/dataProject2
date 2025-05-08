from flask import Flask, request, jsonify
from dateutil import parser
from fuzzywuzzy import process
from ticker_map import ticker_map
app = Flask(__name__)


# Function that retrieves stock data for a specific date
def get_stock_price_by_data(date):
    # Connects to (or creates if not exists) the SQLite database file in the db folder
    connection = sqlite3.connect('db/finance_data.db')
    # Creates a cursor (messenger) to send SQL commands to the connected database
    cursor = connection.cursor()
    # Uses the cursor to execute a SQL SELECT query with a placeholder for the date
    cursor.execute("SELECT * FROM stock_data WHERE Date = ?", (date,))
    # Fetches all matching rows returned by the query and stores them in result
    result = cursor.fetchall()
    # Closes the connection to the database 
    connection.close()
    # Returns the list of retrieved stock data rows
    return result


def extract_ticker(user_input):
    user_input = user_input.lower()
    best_match, score = process.extractOne(user_input, ticker_map.keys())

    if score > 80:
        ticker = ticker_map[best_match]
        info = yf.Ticker(ticker).info
        if "regularMarketPrice" in info:
            return ticker
    return None


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Step 1: Extract ticker from user message
    ticker = extract_ticker(user_input)
    if not ticker:
        return jsonify({"error": "Could not identify a valid stock. Try something like 'Apple' or 'AAPL'."})

    # Step 2: Check if asking for 'today' or 'now'
    if "now" in user_input.lower() or "today" in user_input.lower():
        try:
            live_info = yf.Ticker(ticker).info
            return jsonify({
                "Ticker": ticker,
                "Price": live_info.get("regularMarketPrice", "N/A"),
                "Currency": live_info.get("currency", "USD"),
                "Exchange": live_info.get("exchange", "N/A"),
                "Source": "Live API"
            })
        except Exception as e:
            return jsonify({"error": f"Live price fetch failed: {str(e)}"})

    # Step 3: Try to extract a specific date
    try:
        parsed_date = parser.parse(user_input, fuzzy=True).date()
        date = parsed_date.strftime("%Y-%m-%d")

        # If AAPL, use local DB
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
        
        # If any other ticker, fallback to live API
        else:
            live_info = yf.Ticker(ticker).history(start=date, end=date)
            if not live_info.empty:
                row = live_info.iloc[0]
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
                return jsonify({"error": f"No data found for {ticker} on {date} from API."})

    except Exception as e:
        return jsonify({"error": "Could not understand the date. Use formats like 'August 1, 2023' or '2023-08-01'."})
