"""
task 2
"""
from csv import DictReader, DictWriter
from datetime import datetime


def load_csv(file_path, location):
    """
    Load CSV file and return data as a list of dictionaries for the given location.
    """
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return [
            entry
            for entry in DictReader(file)
            if entry["Settlement Point"].upper() == location
        ]


def convert_to_datetime(row):
    """
    Convert date to datetime and round DAM price.
    """
    return {
        "datetime": datetime.strptime(
            row["\ufeffDelivery Date"] + " " + str(int(row["Delivery Hour"]) - 1),
            "%m/%d/%Y %H",
        ),
        "dam": round(float(row["Settlement Point Price"]), 2),
    }


def calculate_hourly_rtm(rtm_data):
    """
    Calculate hourly RTM average.
    """
    return sum(float(entry["Settlement Point Price"]) for entry in rtm_data) / len(
        rtm_data
    )


def fifteen_min_intervals(dam_data, rtm_data):
    """
    Task 2: Create CSV file with hourly DAM and averaged RTM prices.
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

    with open(file_path, "w", encoding="utf-8-sig", newline="") as output_file:
        headers = csv_list[0].keys()
        writer = DictWriter(output_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_list)

    return file_path


def main():
    """
    Main function.
    """
    dam_data_task2 = load_csv("DAM_Prices_2022.csv", "HB_NORTH")
    rtm_data_task2 = load_csv("RTM_Prices_2022.csv", "HB_NORTH")
    fifteen_min_intervals(dam_data_task2, rtm_data_task2)


if __name__ == "__main__":
    main()
