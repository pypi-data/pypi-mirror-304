import csv

def summarize_csv(path):
    income = 0
    costs = 0
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "Доход":
                income += int(row[2])
            elif row[1] == 'Расход':
                costs += int(row[2])
    return income, costs

