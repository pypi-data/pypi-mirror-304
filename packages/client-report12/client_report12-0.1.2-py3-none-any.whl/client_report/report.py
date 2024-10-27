import pandas as pd

def load_data(input_file):

    return pd.read_csv(input_file)

def generate_age_groups(df):

    age_bins = [18, 26, 36, 46, 61]
    age_labels = ['18-25', '26-35', '36-45', '46-60']
    df['age_group'] = pd.cut(df['Возраст'], bins=age_bins, labels=age_labels, right=False)
    return df['age_group'].value_counts()

def generate_city_distribution(df):

    return df['Город'].value_counts()

def generate_report(df):

    total_clients = len(df)
    age_distribution = generate_age_groups(df)
    city_distribution = generate_city_distribution(df)

    report = [f"Общее количество клиентов: {total_clients}\n"]
    report.append("Количество клиентов по возрастным группам:\n")
    for age_group, count in age_distribution.items():
        report.append(f"{age_group}: {count}\n")

    report.append("\nРаспределение клиентов по городам:\n")
    for city, count in city_distribution.items():
        report.append(f"{city}: {count}\n")

    return ''.join(report)

def save_report(output_file, report):

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
