"""
Showing block_value, scalar
"""
from datetime import datetime
from csv import DictReader, DictWriter


def read_hourly_prices(file_path):
    """Reads hourly prices from a CSV file."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file)
        data = [
            {
                "date": datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S"),
                "price": float(entry["price"]),
            }
            for entry in reader
        ]
    return data


def calculate_block_and_scalar(hourly_data):
    """Calculates block values and scalars for each hour."""
    block_values = {}

    for entry in hourly_data:
        hour_key = entry["date"].strftime("%H:00:00")
        block_values.setdefault(hour_key, {"sum": 0, "count": 0})
        block_values[hour_key]["sum"] += entry["price"]
        block_values[hour_key]["count"] += 1

    block_and_scalar_data = []

    for entry in hourly_data:
        hour_key = entry["date"].strftime("%H:00:00")
        block_value = block_values[hour_key]
        scalar = entry["price"] / block_value["sum"] if block_value["count"] != 0 else 0

        block_and_scalar_data.append(
            {
                "date": entry["date"].strftime("%Y-%m-%d %H:00:00"),
                "block_value": round(block_value["sum"] / block_value["count"], 2),
                "scalar": round(scalar, 2),
            }
        )

    return block_and_scalar_data


def write_block_and_scalar_to_csv(data, output_file_path):
    """Writes block and scalar data to a CSV file."""
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["date", "block_value", "scalar"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    HOURLY_PRICES_PATH = "hourly_prices.csv"
    hourly_dataa = read_hourly_prices(HOURLY_PRICES_PATH)
    block_and_scalar_dataa = calculate_block_and_scalar(hourly_dataa)

    OUTPUT_PATH = "block_and_scalar_results.csv"
    write_block_and_scalar_to_csv(block_and_scalar_dataa, OUTPUT_PATH)
