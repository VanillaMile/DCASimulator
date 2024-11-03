
# DCA Strategy simulator

[Description]


## Installation

1. Install [mongoDB community server](https://www.mongodb.com/try/download/community-kubernetes-operator)

2. If mongoDB wasn't installed as service, start mongod.exe from terminal

```bash
  {your path}\MongoDB\Server\8.0\bin\mongod.exe
```
3. Import data into Database DCASimulator into collection Stocks (Must be created first time)

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