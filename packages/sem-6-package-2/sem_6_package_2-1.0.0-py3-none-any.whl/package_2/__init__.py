def analyze_transactions(transactions):
    grouped_transactions = transactions.groupby('category')['amount'].sum()

    report = f"Доход: {grouped_transactions['Доход']} руб.\n"
    report += f"Расход: {grouped_transactions['Расход']} руб."

    return report