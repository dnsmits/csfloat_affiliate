import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

session = ""

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

page = 0
url = f"https://csfloat.com/api/v1/me/transactions?page={page}&limit=100&order=desc"

response = requests.get(url, cookies=cookies, headers=headers).json()

count = response["count"]
current = 0

transactions = []

while current <= count:
    url = f"https://csfloat.com/api/v1/me/transactions?page={page}&limit=100&order=desc"
    response = requests.get(url, cookies=cookies, headers=headers).json()

    for transaction in response["transactions"]:
        if transaction["type"] == "affiliate":
            transactions.append(transaction)

    page += 1
    current += 100

balance = 0
for transaction in transactions:
    balance += transaction["balance_offset"]

weekly_totals = defaultdict(int)
weekly_transactions = defaultdict(int)

for entry in transactions:
    week_start = datetime.fromisoformat(entry['created_at'][:-1])
    week_start = week_start - timedelta(days=week_start.weekday())  # Get Monday of that week
    week_label = week_start.strftime('%Y-%m-%d')
    weekly_totals[week_label] += entry['balance_offset'] / 100
    weekly_transactions[week_label] += 1

weeks = sorted(weekly_totals.keys())
totals = [weekly_totals[week] for week in weeks]
transactions = [weekly_transactions[week] for week in weeks]

plt.figure(figsize=(10, 6))
plt.plot(weeks, totals, marker='o', label='Total Funds ($)', color='blue')
plt.plot(weeks, transactions, marker='o', label='Number of Transactions', color='green')

for i, week in enumerate(weeks):
    plt.text(i, -75, f"${totals[i]:.2f}", ha='center', va='top', fontsize=8, color='blue', transform=plt.gca().transData)
    plt.text(i, -100, f"{transactions[i]}", ha='center', va='top', fontsize=8, color='green', transform=plt.gca().transData)

plt.title('Weekly Totals and Transactions')
plt.ylabel('Value')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(range(len(weeks)), weeks, rotation=45)
plt.ylim(-5, max(max(totals), max(transactions)) + 5)
plt.tight_layout()

plt.show()
