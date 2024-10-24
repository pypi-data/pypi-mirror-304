import pandas as pd


def load_transactions(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except pd.errors.EmptyDataError:
        raise ValueError("Файл пуст.")
    except pd.errors.ParserError:
        raise ValueError("Ошибка при парсинге CSV-файла.")


def group_transactions(df):
    if 'category' not in df.columns or 'sales' not in df.columns or 'quantity' not in df.columns:
        raise ValueError("CSV-файл должен содержать столбцы: 'category', 'sales', 'quantity'.")

    grouped = df.groupby('category').agg({'sales': 'sum', 'quantity': 'sum'}).reset_index()
    grouped['expense'] = grouped['quantity']

    total_income = grouped['sales'].sum()
    total_expense = grouped['expense'].sum()

    return {
        'Доход': total_income,
        'Расход': total_expense
    }


def generate_report(report_data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for key, value in report_data.items():
                if key == 'ROI':
                    f.write(f"{key}: {value:.2f}%\n")
                else:
                    f.write(f"{key}: {value} руб.\n")
    except IOError as e:
        raise IOError(f"Не удалось записать файл {output_file}: {e}")
