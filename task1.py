"""
task1 
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


def create_task_1(dam_data, rtm_data):
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

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 31, 23)
    hourly_intervals = [
        start_date + timedelta(hours=i)
        for i in range(int((end_date - start_date).total_seconds() / 3600) + 1)
    ]

    result = []
    c = 0

    for interval in hourly_intervals:
        if c < len(rtm_av):
            for dam_entry in dam_hb_north:
                if dam_entry["datetime"] == interval:
                    result.append(
                        {
                            "date": interval.strftime("%Y-%m-%d %H:%M:%S"),
                            "dam": dam_entry["dam"],
                            "rtm": f"{rtm_av[c]:.2f}",
                        }
                    )
                    break
            c += 1

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

    task_1_filepath = create_task_1(dam_data, rtm_data)
    print(f"Task 1 created at: {task_1_filepath}")


if __name__ == "__main__":
    main()
