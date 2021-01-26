import csv
import os
from collections import defaultdict
from contextlib import suppress
from decimal import Decimal as D

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("gcr", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

fields = ("amount", "date", "number")


def load_template(name: str = "default.template") -> Environment:
    return env.get_template(name)


def rename_columns(row):
    mapping = (("Amount Num.", "amount"), ("Date", "date"), ("Number", "number"))
    for before, after in mapping:
        row[after] = row[before]
    return row


def main():
    prepare_environment()
    people = defaultdict(dict)
    with open("20-checking.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if is_giving_row(r):
                r = rename_columns(r)
                total = people[r["Description"]].get("total", D("0"))
                total += D(r["amount"].replace(",", ""))
                people[r["Description"]]["total"] = total
                try:
                    people[r["Description"]]["instances"].append(
                        {f: r[f] for f in r if f in fields}
                    )
                except KeyError:
                    people[r["Description"]]["instances"] = []
                    people[r["Description"]]["instances"].append(
                        {f: r[f] for f in r if f in fields}
                    )

    temp = load_template()
    for person, values in people.items():
        output = temp.render(
            name=person, instances=values["instances"], total=values["total"]
        )
        with open(f'output/{person.replace(" ", "_")}.html', "w") as f:
            f.write(output)


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


def prepare_environment():
    with suppress(FileExistsError):
        os.mkdir("output")


if __name__ == "__main__":
    main()
