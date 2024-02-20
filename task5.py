"""
assignment 2
"""
from datetime import datetime
from csv import DictReader, DictWriter


def find_max_difference_pair(data):
    """
    Find the pair of hours with the maximum difference between the top and bottom prices.
    """
    max_diff = 0
    largest_value = None
    smallest_value_before_largest = None

    for i in range(1, len(data)):
        current_diff = data[i]["price"] - min(entry["price"] for entry in data[:i])
        if current_diff > max_diff:
            max_diff = current_diff
            largest_value = data[i]
            smallest_value_before_largest = min(data[:i], key=lambda x: x["price"])

    data.remove(largest_value)
    data.remove(smallest_value_before_largest)

    return largest_value, smallest_value_before_largest, max_diff


def modified_tb2(data):
    """
    Calculate the modified TB2 value for the given data.
    """
    ans = []

    for _ in range(2):
        pair = find_max_difference_pair(data)
        ans.append(pair[2])

    return sum(ans)


def read_task1_csv(file_path, column_name="dam"):
    """
    Read the CSV file and extract relevant data.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file)
        data = [
            {
                "date": datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").strftime(
                    "%Y-%m-%d"
                ),
                "hour": int(entry["date"].split(" ")[1].split(":")[0]),
                "price": float(entry[column_name]),
            }
            for entry in reader
        ]
    return data


def calculate_modified_tb2_for_each_day(data):
    """
    Calculate modified TB2 for each unique date.
    """
    tb2_results = {}
    unique_dates = sorted(set(entry["date"] for entry in data))

    for date in unique_dates:
        daily_data = [entry for entry in data if entry["date"] == date]
        try:
            result = modified_tb2(daily_data)
            tb2_results[date] = round(result, 2)
        except ValueError as e:
            print(f"Skipping date {date}: {e}")

    return tb2_results


def write_to_csv(results, output_file_path):
    """
    Write the results to a CSV file.
    """
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["date", "tb2"])
        writer.writeheader()
        writer.writerows(
            [{"date": date, "tb2": tb2_value} for date, tb2_value in results.items()]
        )


if __name__ == "__main__":
    FILEPATH = "task_1.csv"
    formatted_data = read_task1_csv(FILEPATH)
    modified_tb2_results = calculate_modified_tb2_for_each_day(formatted_data)
    OUTPUTT = "modified_dam_tb2.csv"
    write_to_csv(modified_tb2_results, OUTPUTT)
