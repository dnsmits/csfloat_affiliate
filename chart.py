import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3

# Read from database
conn = sqlite3.connect("transactions.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, created_at, type, balance_offset FROM transactions WHERE type='affiliate'")
rows = cursor.fetchall()
transactions = [dict(row) for row in rows]

conn.commit()
conn.close()

# --- Weekly Aggregation ---
weekly_totals = defaultdict(int)
weekly_transactions = defaultdict(int)

for entry in transactions:
    dt = datetime.fromisoformat(entry['created_at'][:-1])
    week_start = dt - timedelta(days=dt.weekday())
    week_label = week_start.strftime('%Y-%m-%d')
    weekly_totals[week_label] += entry['balance_offset'] / 100
    weekly_transactions[week_label] += 1

weeks = sorted(weekly_totals.keys())
weekly_values = [weekly_totals[week] for week in weeks]
weekly_counts = [weekly_transactions[week] for week in weeks]

# --- Monthly Aggregation ---
monthly_totals = defaultdict(int)
monthly_transactions = defaultdict(int)

for entry in transactions:
    month = datetime.fromisoformat(entry['created_at'][:-1]).strftime('%Y-%m')
    monthly_totals[month] += entry['balance_offset'] / 100
    monthly_transactions[month] += 1

months = sorted(monthly_totals.keys())
monthly_values = [monthly_totals[month] for month in months]
monthly_counts = [monthly_transactions[month] for month in months]

# --- Plot Weekly ---
plt.figure("Weekly Totals and Transactions", figsize=(10, 6))
plt.plot(weeks, weekly_values, marker='o', label='Total Funds ($)', color='blue')
plt.plot(weeks, weekly_counts, marker='o', label='Number of Transactions', color='green')

for i, week in enumerate(weeks):
    plt.text(i, -75, f"${weekly_values[i]:.2f}", ha='center', va='top', fontsize=8, color='blue')
    plt.text(i, -100, f"{weekly_counts[i]}", ha='center', va='top', fontsize=8, color='green')

plt.title('Weekly Totals and Transactions')
plt.ylabel('Value')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(range(len(weeks)), weeks, rotation=45)
plt.ylim(-5, max(max(weekly_values), max(weekly_counts)) + 5)
plt.tight_layout()

# --- Plot Monthly ---
plt.figure("Monthly Totals and Transactions", figsize=(10, 6))
plt.plot(months, monthly_values, marker='o', label='Total Funds ($)', color='blue')
plt.plot(months, monthly_counts, marker='o', label='Number of Transactions', color='green')

for i, month in enumerate(months):
    plt.text(i, -50, f"${monthly_values[i]:.2f}", ha='center', va='top', fontsize=8, color='blue')
    plt.text(i, -75, f"{monthly_counts[i]}", ha='center', va='top', fontsize=8, color='green')

plt.title('Monthly Totals and Transactions')
plt.ylabel('Value')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(range(len(months)), months, rotation=45)
plt.ylim(-5, max(max(monthly_values), max(monthly_counts)) + 5)
plt.tight_layout()

plt.show()
