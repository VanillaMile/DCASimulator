import json
import os
import sys

def separateYearArray(daily_data, year):
    this_year_daily_data = []
    for daily in daily_data:
        if daily["trade_date"].startswith(year):
            this_year_daily_data.append(daily)
    return this_year_daily_data

def main(input_file, output_file):
    # if len(sys.argv) != 3:
    #     print("Usage: separateYearArray.py <input_file> <output_file>")
    #     sys.exit(1)

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    with open(input_file, "r") as f:
        data = json.load(f)
    
    for i in range(len(data["yearly_returns"])):
        toNewFile = {
            "stock_name": data["stock_name"] + "_short",
            "stock_symbol": data["stock_symbol"],
            "description": data["description"],
            "avg_daily_return": data["avg_daily_return"],
            "all_time_return": data["all_time_return"],
            "avg_yearly_return": data["avg_yearly_return"],
            "year": data["yearly_returns"][i]["year"],
            "yearly_return": data["yearly_returns"][i]["return"],
            "daily_data": []
        }
        toNewFile["daily_data"] = separateYearArray(data["daily_data"], str(data["yearly_returns"][i]["year"]))
        print("finished")
        with open(output_file + str(data["yearly_returns"][i]["year"]) + ".json", "w+") as f:
            json.dump(toNewFile, f, indent=2)

if __name__ == "__main__":
    main("BetterReturnsStock.json", "BetterReturnsStock")
    main("MidDropStock.json", "MidDropStock")
    main("SNP500StyleReturns.json", "SNP500StyleReturns")