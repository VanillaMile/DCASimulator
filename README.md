# DCA Strategy simulator

This is a simple DCA strategy simulator, it creates a random simulation of market data and provides investment results based on user settings.


## Installation

1. Install [mongoDB community server](https://www.mongodb.com/try/download/community-kubernetes-operator)

2. If mongoDB wasn't installed as service, start mongod.exe from terminal

```bash
    {your path}\MongoDB\Server\8.0\bin\mongod.exe
```
3. Import data into Database dcaDatabase into collection stocks (Must be created first time) and rankings. NAMES ARE IMPORTANT, it's case sensitive
```bash
    Database name: dcaDatabase
    Collection name: stocks
    Collection name: rankings
```
Import full collections
```bash
    !COLLECTIONS TO IMPORT\dcaDatabase.stocks.json -> stocks
    !COLLECTIONS TO IMPORT\dcaDatabase.rankings.json -> rankings
```

4. Create venv for your project with python 3.13
```bash
    python -m venv {name}
    {name}/Scripts/activate
```
5. Install requirements
```bash
    pip install -r requirements.txt
```
6. Run script
```bash
    python run.py
```
