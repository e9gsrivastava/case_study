"""
Create a csv file containing DAM & RTM prices
at hourly intervals from Jan 1 to Jan 31, 
2022 for HB_NORTH. The csv file should be
named ‘task_1.csv’ with only 3 columns. 
"""
from csv import DictReader, DictWriter
from datetime import datetime, timedelta


def load_csv(file_path):
    """
    Load CSV file and return data as a list of dictionaries.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(DictReader(file))


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


def _hourly_intervals(dam_data, rtm_data):
    """
    Task 1: Create CSV file with hourly DAM and RTM prices.
    """
    dam_hb_north = [
        convert_to_datetime(row)
        for row in dam_data
        if row["Settlement Point"] == "HB_NORTH"
    ]
    rtm_hb_north = [row for row in rtm_data if row["Settlement Point"] == "HB_NORTH"]

    rtm_av = [
        calculate_hourly_rtm(rtm_hb_north[i : i + 4])
        for i in range(0, len(rtm_hb_north), 4)
    ]

    hourly_intervals = [
        datetime(2022, 1, 1) + timedelta(hours=i) for i in range(24 * 31)
    ]

    result = [
        {
            "date": interval.strftime("%Y-%m-%d %H:%M:%S"),
            "dam": dam_entry["dam"],
            "rtm": f"{rtm_entry:.2f}",
        }
        for interval, dam_entry, rtm_entry in zip(
            hourly_intervals, dam_hb_north, rtm_av
        )
    ]

    output_file_path = "task_1.csv"

    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["date", "dam", "rtm"])
        writer.writeheader()
        writer.writerows(result)

    return output_file_path


def main():
    """
    Main function.
    """
    dam_data = load_csv("DAM_Prices_2022.csv")
    rtm_data = load_csv("RTM_Prices_2022.csv")

    task_1_filepath = _hourly_intervals(dam_data, rtm_data)
    print(task_1_filepath)


if __name__ == "__main__":
    main()
