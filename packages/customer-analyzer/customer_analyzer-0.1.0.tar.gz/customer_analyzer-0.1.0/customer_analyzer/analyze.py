import pandas as pd

def analyze_customers(input_file: str, output_file: str):
    data = pd.read_csv(input_file)

    total_customers = len(data)

    bins = [18, 25, 35, 45, 60, 100]
    labels = ['18-25', '26-35', '36-45', '46-60', '61+']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

    age_groups = data['age_group'].value_counts().sort_index()

    cities = data['city'].value_counts()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Общее количество клиентов: {total_customers}\n\n")
        f.write("Количество клиентов по возрастным группам:\n")
        for group, count in age_groups.items():
            f.write(f"{group}: {count}\n")
        f.write("\nРаспределение клиентов по городам:\n")
        for city, count in cities.items():
            f.write(f"{city}: {count}\n")
