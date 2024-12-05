#data format: day, date, open, close, change
import json
import csv

def convert_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    json_data = []
    collectionArray = []
    for row in data[1:]:
        collectionArray.append({
            "day": row[0],
            "trade_date": row[1],
            "open_price": row[2],
            "close_price": row[3],
            "change": row[4]
        })
    json_data.append({
        "stock_name": "Name",
        "stock_symbol": "Symbol",
        "description": "Description",
        "avg_daily_return": "00",
        "all_time_return": "00",
        "avg_yearly_return": "00",
        "yearly_returns": [
            {
                "year": "Year",
                "return": "Return"
            }
        ],
        "daily_data": collectionArray
    })
    with open('data.json', 'w') as file:
        json.dump(json_data, file, indent=4)

convert_data('data.csv')