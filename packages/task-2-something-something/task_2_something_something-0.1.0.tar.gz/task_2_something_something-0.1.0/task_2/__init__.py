import csv

def to_txt(csv_path, txt_path):
    with open(csv_path, 'r') as csv_file:
        data = [i for i in csv.DictReader(csv_file)]

    with open(txt_path, 'w') as txt_file:
        txt_file.write('\n'.join(f"{i['category']}: {i['amount']} руб." for i in data))
