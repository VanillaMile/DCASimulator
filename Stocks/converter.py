import json
import os
import sys

def convert_to_float(data):
    data["avg_daily_return"] = round(float(data["avg_daily_return"].strip("%")) / 100, ndigits=4)
    data["all_time_return"] = round(float(data["all_time_return"].strip("%")) / 100, ndigits=4)
    data["avg_yearly_return"] = round(float(data["avg_yearly_return"].strip("%")) / 100, ndigits=4)
    
    for yearly_return in data["yearly_returns"]:
        if isinstance(yearly_return["year"], str):
            yearly_return["year"] = int(yearly_return["year"])
            yearly_return["return"] = round(float(yearly_return["return"].strip("%")) / 100, ndigits=4)
    for daily_data in data["daily_data"]:
        daily_data["day"] = int(daily_data["day"])
        daily_data["open_price"] = float(daily_data["open_price"])
        daily_data["close_price"] = float(daily_data["close_price"])
        daily_data["change"] = float(daily_data["change"])
    return data

def main():
    if len(sys.argv) != 3:
        print("Usage: converter.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    with open(input_file, "r") as f:
        data = json.load(f)
    
    data = convert_to_float(data)

    with open(output_file, "w+") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
    
