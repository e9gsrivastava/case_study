"""
task 2
"""

import csv
from datetime import datetime


def load_csv_data(file_path, location):
    """
    Load data from CSV file for the given location.
    """
    csv_path = file_path

    with open(csv_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        data = [
            entry for entry in reader if entry["Settlement Point"].upper() == location
        ]

    return data


def answer(dam_data, rtm_data):
    """
    Create Task 2 CSV file with hourly DAM and averaged RTM prices.
    """
    csv_list = []
    dam_index = 0

    for index, rtm_entry in enumerate(rtm_data, start=1):
        date_time = (
            rtm_entry["Delivery Date"]
            + " "
            + str(int(rtm_entry["Delivery Hour"]) - 1)
            + ":"
            + f"{(int(rtm_entry['Delivery Interval']) - 1) * 15}"
        )
        dam_price = dam_data[dam_index]["Settlement Point Price"]
        rtm_price = rtm_entry["Settlement Point Price"]

        date_obj = datetime.strptime(date_time, "%m/%d/%Y %H:%M")

        csv_dict = {
            "date": datetime.strftime(date_obj, "%Y-%m-%d %H:%M:%S"),
            "dam": f"{float(dam_price):.2f}",
            "rtm": f"{float(rtm_price):.2f}",
        }

        csv_list.append(csv_dict)

        if index % 4 == 0:
            dam_index += 1

    file_path = "task_2.csv"

    with open(file_path, "w", encoding="utf-8") as output_file:
        headers = csv_list[0].keys()
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_list)

    return file_path


if __name__ == "__main__":
    dam_data_task2 = load_csv_data("DAM_Prices_2022.csv", "HB_NORTH")
    rtm_data_task2 = load_csv_data("RTM_Prices_2022.csv", "HB_NORTH")
    answer(dam_data_task2, rtm_data_task2)
