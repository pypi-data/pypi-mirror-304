import pandas as pd

def customer_stat(input_csv, output_txt):
    df = pd.read_csv(input_csv)
    city_counts = df['city'].value_counts().reset_index()
    city_counts.columns = ['City', 'Number of Clients']

    bins = [17, 25, 35, 45, 60]
    labels = ['18-25', '26-35', '36-45', '46-60']
    df['age_category'] = pd.cut(df['age'], bins=bins, labels=labels)

    age_category_counts = df['age_category'].value_counts().reset_index()
    age_category_counts.columns = ['Age Category', 'Number of Clients']

    age_category_counts=age_category_counts.to_dict()
    city_counts = city_counts.to_dict()

    with open(output_txt, 'w') as f:
        f.write(f'Общее количество клиентов: {df["city"].count()}\n')
        f.write('\n')
        f.write("Количество клиентов по возрастным группам:\n")
        for i in range(len(age_category_counts['Age Category'])):
            f.write(f'{age_category_counts["Age Category"][i]}: {age_category_counts["Number of Clients"][i]}\n')
        f.write('\n')
        f.write("Распределение клиентов по городам:\n")
        for i in range(len(city_counts['City'])):
            f.write(f'{city_counts["City"][i]}: {city_counts["Number of Clients"][i]}\n')




