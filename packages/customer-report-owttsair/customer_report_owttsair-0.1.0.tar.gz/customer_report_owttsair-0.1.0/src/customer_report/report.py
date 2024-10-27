import pandas as pd
def load_data(input_file):
    return pd.read_csv(input_file)
def generate_report(data):
    total_clients = len(data)
    age_groups = pd.cut(
        data['age'],
        bins=[18, 25, 35, 45, 60, 100],
        labels=["18-25", "26-35", "36-45", "46-60", "60+"]
    ).value_counts().sort_index()
    city_distribution = data['city'].value_counts()
    report_lines = [
        f"Общее количество клиентов: {total_clients}\n\n",
        "Количество клиентов по возрастным группам:\n"
    ]
    report_lines += [f"{age_group}: {count}\n" for age_group, count in age_groups.items()]

    report_lines.append("\nРаспределение клиентов по городам:\n")
    report_lines += [f"{city}: {count}\n" for city, count in city_distribution.items()]

    return ''.join(report_lines)
def save_report(report_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(report_content)
