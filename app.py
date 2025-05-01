from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_stock_price_by_data(date):
    conn = sqlite3.connect('db/finance_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_data WHERE Date = ?", (date,))
    result = cursor.fetchall()
    conn.close()
    return result



