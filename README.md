
## Installation

1. Install [mongoDB community server](https://www.mongodb.com/try/download/community-kubernetes-operator)

2. If mongoDB wasn't installed as service, start mongod.exe from terminal

```bash
    {your path}\MongoDB\Server\8.0\bin\mongod.exe
```
3. Import data into Database dcaDatabase into collection stocks (Must be created first time) 
NAMES ARE IMPORTANT, it's case sensitive
```bash
    Database name: dcaDatabase
    Collection name: stocks
```
Import either full collection
```bash
    Stocks\dcaDatabase.stocks.json
```
or individual files
```bash
    Stocks\Individual Stocks\BetterReturnsStock.json
    Stocks\Individual Stocks\DebugStock.json
    Stocks\Individual Stocks\MidDropStock.json
    Stocks\Individual Stocks\SNP500StyleReturns.json
```

4. Create venv for your project with python 3.13
```bash
    python -m venv {name}
    {name}/Scripts/activate
```
install requirements
```bash
    pip install -r requirements.txt
```
5. Run script
```bash
    python run.py
```
