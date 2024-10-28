import csv

def otchet(csv_path_from, csv_path_to):
    with open(csv_path_from, 'r') as csv_file_from:
        data = {}
        for i in csv.DictReader(csv_file_from):
            if i['category'] in data:
                data[i['category']]['sales'] += int(i['sales'])
                data[i['category']]['quantity'] += int(i['quantity'])
            else:
                data[i['category']] = {'category': i['category'], 'sales': int(i['sales']), 'quantity': int(i['quantity'])}

    with open(csv_path_to, 'w', newline='') as csv_file_to:
        writer = csv.DictWriter(csv_file_to, ['category', 'sales', 'quantity'])
        writer.writeheader()
        writer.writerows(data.values())
