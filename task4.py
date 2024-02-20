"""
rtm_tb2.csv
"""
from datetime import datetime
from csv import DictReader, DictWriter

def calculate_tbn_revenue(data, n):
    """
    Calculate TBn.
    """
    sorted_data = sorted(data, key=lambda x: x["price"])
    top_n_prices = sum(entry["price"] for entry in sorted_data[:n])
    bottom_n_prices = sum(entry["price"] for entry in sorted_data[-n:])
    tbn_revenue = top_n_prices - bottom_n_prices
    return -tbn_revenue

def read_task1_csv(file_path, column_name="rtm"):
    """
    Read data from task1.csv file and convert it to the desired format.
    """
    with open(file_path, "r", encoding="utf-8") as csv_file:
        reader = DictReader(csv_file)
        data = [
            {
                "date": datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
                "price": float(entry[column_name]),
            }
            for entry in reader
        ]
    return data

def calculate_tb2_for_each_day(data):
    """
    Calculate TB2 revenue for each day.
    """
    tb2_results = {}
    unique_dates = sorted(set(entry["date"] for entry in data))

    for date in unique_dates:
        daily_data = [entry for entry in data if entry["date"] == date]
        tb2_results[date] = round(calculate_tbn_revenue(daily_data, 2), 2)

    return tb2_results

def write_to_csv(results, output_file_path):
    """
    Write results to a CSV file.
    """
    with open(output_file_path, "w", newline="", encoding="utf-8") as csv_output_file:
        writer = DictWriter(csv_output_file, fieldnames=["date", "tb2"])
        writer.writeheader()
        writer.writerows([{"date": date, "tb2": tb2_value} for date, tb2_value in results.items()])

TASK_1_FILE_PATH = "task_1.csv"
formatted_data = read_task1_csv(TASK_1_FILE_PATH)
rtm_tb2_results = calculate_tb2_for_each_day(formatted_data)
RTM_TB2_OUTPUT_FILE_PATH = "rtm_tb2.csv"
write_to_csv(rtm_tb2_results, RTM_TB2_OUTPUT_FILE_PATH)
