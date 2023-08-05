import os
import re
import argparse
import subprocess
import csv
from collections import Counter, defaultdict
from tabulate import tabulate


def check_type_annotations(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    type_annotation_pattern = re.compile(r'(?<=:)\s*([a-zA-Z_][a-zA-Z0-9_]*|\s*List\s*\[[a-zA-Z0-9_, ]+\])\s*')
    match = type_annotation_pattern.search(content)
    return bool(match)


def analyze_file(directory, file_path, table_data):
    print(f"Analyzing the file: {file_path}\n")

    # Check Type Annotations
    type_annotations_present = check_type_annotations(file_path)

    # Run Pylint
    process = subprocess.run(["pylint", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True, check=False)
    pylint_output = process.stdout

    alert_count = Counter()
    alert_details = defaultdict(list)

    alert_pattern = re.compile(r'([CRWEF]\d{4})')

    alert_type_names = {
        'C': 'Convention',
        'R': 'Refactor',
        'W': 'Warning',
        'E': 'Error',
        'F': 'Fatal'
    }

    for line in pylint_output.split("\n"):
        match = alert_pattern.search(line)
        if match:
            alert_code = match.group(0)
            alert_type = alert_code[0]
            alert_count[alert_type] += 1
            alert_details[alert_type].append(alert_code)

    total_alerts = sum(alert_count.values())
    # Update the table data structure
    table_row = [file_path, total_alerts]
    for alert_type in alert_type_names.keys():
        table_row.append(alert_count[alert_type])

    table_row.append(", ".join(sorted(set(alert_code for alert_codes in alert_details.values() for alert_code in alert_codes))))
    table_row.append("Yes" if type_annotations_present else "No")  # Adds the "Adopt Type Annotations?" field

    # Run Mypy
    mypy_process = subprocess.run(["mypy", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  universal_newlines=True, check=False)
    mypy_output = mypy_process.stdout

    mypy_output_no_newline = mypy_output.replace('\n', ' | ')
    table_row.append(mypy_output_no_newline if type_annotations_present else "None")  # Adds the "Type Annotations Description" field
    table_data.append(table_row)

    return total_alerts

def export_to_csv(table_data, headers, csv_output):
    with open(csv_output, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        for row in table_data:
            csv_writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Analyze Python files in the specified directory.")
    parser.add_argument("directory", help="The directory path containing the Python files to analyze.")
    parser.add_argument("-o", "--output", help="The path and file name for the CSV output.", type=str)

    args = parser.parse_args()
    root_directory = args.directory
    csv_output = args.output

    table_data = []
    total_alerts_directory = 0

    for root, dirs, files in os.walk(root_directory):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                total_alerts_directory += analyze_file(root, file_path, table_data)

    print(f"\nTotal alerts found in the directory: {total_alerts_directory}\n")
    headers = ["File", "Total Alerts", "Convention", "Refactor", "Warning", "Error", "Fatal", "Alert Codes",
               "Adopt Type Annotations?", "Type Annotations Description"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    if csv_output:
        export_to_csv(table_data, headers, csv_output)
        print(f"CSV file exported to: {csv_output}")

if __name__ == "__main__":
    main()



