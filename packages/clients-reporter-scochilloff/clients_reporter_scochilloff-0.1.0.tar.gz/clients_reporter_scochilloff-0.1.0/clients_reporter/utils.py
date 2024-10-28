import pandas as pd


def load_clients(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def get_age_data(clients: pd.DataFrame) -> pd.Series:
    age_bins = [18, 25, 35, 45, 60, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-60', '61+']
    clients['age_group'] = pd.cut(clients['age'], bins=age_bins, labels=age_labels, right=False)
    return clients.groupby("age_group", observed=False)["age"].count()


def get_city_data(clients: pd.DataFrame) -> pd.Series:
    return clients.groupby("city", observed=False)["city"].count()


def write_report(clients: pd.DataFrame, filename: str) -> None:
    report = get_report(clients)
    with open(filename, "w", encoding="utf-8")  as file:
        file.write(report)


def get_report(clients: pd.DataFrame) -> str:
    age_data = get_age_data(clients)
    city_data = get_city_data(clients)
    report_lines = []
    report_lines.append(f"Общее количество клиентов: {len(clients)}\n")
    report_lines.append(f"Количество клиентов по возрастным группам:")
    for group, count in age_data.items():
        report_lines.append(f"{group}: {count}")
    report_lines.append("")
    report_lines.append("Распределение клиентов по городам:")
    for group, count in city_data.items():
        report_lines.append(f"{group}: {count}")
    return "\n".join(report_lines)
