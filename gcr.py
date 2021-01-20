import csv
from collections import defaultdict
from decimal import Decimal as D


fields = ('Amount Num.', 'Date')

def print_report():
    people = defaultdict(dict)
    with open("20-checking.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if is_giving_row(r):
                print(f"{r['Date']}\t {r['Description']}\t {r['Amount Num.']}")
                total = people[r['Description']].get('total', D('0'))
                total += D(r['Amount Num.'].replace(',', ''))
                people[r['Description']]['total'] = total
                try:
                    people[r['Description']]['instances'].append({
                        f: r[f] for f in r if f in fields
                    })
                except KeyError:
                    people[r['Description']]['instances'] = []
                    people[r['Description']]['instances'].append({
                        f: r[f] for f in r if f in fields
                    })
    from pprint import pprint
    pprint(people)



def get_names():
    pass


def is_giving_row(row):
    if (
        row["Description"]
        and row["Action"] == "Payment"
        and "Checking Account" in row["Account Name"]
        and not "Expense" in row["Description"]
    ):
        return True
    return False


if __name__ == "__main__":
    print_report()
