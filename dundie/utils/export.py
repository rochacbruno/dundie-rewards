import csv


def export_json(output: str, result: dict) -> bool:
    """Export json file based on input data"""
    # TODO: Solve decimal problem
    pass
    # try:
    #    with open(output, "w") as output_file:
    #        for item in result:
    #            if type(item) == decimal.Decimal:
    #                print("É decimal")
    #                item = str(item)

    #       output_file.write(json.dumps(result))

    # except NotADirectoryError as error:
    #    print(error)


def export_csv(output: str, result: dict) -> bool:
    """Export csv file based on input data"""

    try:
        with open(f"{output}.csv", "w", newline="") as csvfile:
            fieldnames = [key for key in result[0].keys()]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(person for person in result)

    except PermissionError as error:
        print(error)
