import sqlite3
import time
import random
import requests
import sys

session = input("token: ")

cookies = {
    "session": session
}

headers = {
    "device": "1",
    "platform": "2",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Safari/537.36 "
                  "OPR/93.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
}


conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        created_at TEXT,
        type TEXT,
        balance_offset REAL
    )
''')
conn.commit()

page = 0
url = f"https://csfloat.com/api/v1/me/transactions?page={page}&limit=100&order=desc"
response = requests.get(url, cookies=cookies, headers=headers).json()

count = response["count"]
current = 0

conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

while current <= count:
    url = f"https://csfloat.com/api/v1/me/transactions?page={page}&limit=100&order=desc"
    response = requests.get(url, cookies=cookies, headers=headers).json()

    for transaction in response["transactions"]:
        try:
            cursor.execute('''
                INSERT INTO transactions (id, created_at, type, balance_offset)
                VALUES (?, ?, ?, ?)
            ''', (
                transaction.get("id"),
                transaction.get("created_at"),
                transaction.get("type"),
                transaction.get("balance_offset")
            ))
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            sys.exit(1)

    page += 1
    current += 100
    quit()
    time.sleep(random.randint(2000, 3000) / 1000)

conn.close()
