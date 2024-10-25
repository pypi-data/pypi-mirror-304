import pandas as pd

def analyze_transactions(input_file: str, output_file: str):
    # Загружаем данные из CSV-файла
    data = pd.read_csv(input_file)

    # Группируем транзакции по категориям (Доход и Расход)
    income = data[data['category'] == 'Доход']['amount'].sum()
    expense = data[data['category'] == 'Расход']['amount'].sum()

    # Генерируем отчёт
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Доход: {income} руб.\n")
        f.write(f"Расход: {expense} руб.\n")
