def analyze_customers(customers_data):
    total_customers = len(customers_data)

    age_groups = {
        '<18': 0,
        '18-25': 0,
        '26-35': 0,
        '36-45': 0,
        '46-60': 0,
        '60+': 0
    }
    for age in customers_data['age']:
        if age < 18:
            age_groups['<18'] += 1
        elif 18 <= age <= 25:
            age_groups['18-25'] += 1
        elif 26 <= age <= 35:
            age_groups['26-35'] += 1
        elif 36 <= age <= 45:
            age_groups['36-45'] += 1
        elif 46 <= age <= 60:
            age_groups['46-60'] += 1
        else:
            age_groups['60+'] += 1

    city_counts = customers_data['city'].value_counts()

    report = f"Общее количество клиентов: {total_customers}\n\n"
    report += "Количество клиентов по возрастным группам:\n"
    for age_group, count in age_groups.items():
        report += f"{age_group}: {count}\n"
    report += "\n"
    report += "Распределение клиентов по городам:\n"
    for city, count in city_counts.items():
        report += f"{city}: {count}\n"

    return report
