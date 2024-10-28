import csv

def otchet(csv_path, txt_path):
    with open(csv_path, 'r') as csv_file:
        data = [i for i in csv.DictReader(csv_file)]

    with open(txt_path, 'w', newline='') as txt_file:
        txt_file.write(f'Общее количество клиентов: {len(data)}\n\n')
        txt_file.write('Количество клиентов по возрастным группам:\n')
        txt_file.write(f'18-25: {sum(1 for i in data if 18 <= int(i['age']) <= 25)}\n')
        txt_file.write(f'26-35: {sum(1 for i in data if 26 <= int(i['age']) <= 35)}\n')
        txt_file.write(f'36-45: {sum(1 for i in data if 36 <= int(i['age']) <= 45)}\n')
        txt_file.write(f'46-60: {sum(1 for i in data if 46 <= int(i['age']) <= 60)}\n\n')
        txt_file.write('Распределение клиентов по городам:\n')

        cities = {}
        for i in data:
            if i['city'] in cities:
                cities[i['city']] += 1
            else:
                cities[i['city']] = 0

        for key, value in cities:
            txt_file.write(f'{key}: {value}\n')