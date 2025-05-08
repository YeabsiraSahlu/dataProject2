import yfinance as yf
import pandas as pd
import sqlite3

#Extract 
def extract_data(ticker="AAPL", period="1y", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    return data

#Transform
def transform_data(df):
    df = df.reset_index()
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    return df

#load
def load_to_sqlite(df, db_path="db/finance_data.db"):
    connection = sqlite3.connect(db_path)
    df.to_sql("stock_data", connection, if_exists="replace", index=False)
    connection.close()

if __name__ == "__main__":
    raw = extract_data()
    cleaned = transform_data(raw)
    load_to_sqlite(cleaned)
    print("ETL pipline complete.")

