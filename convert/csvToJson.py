import csv
import json
from datetime import datetime as dt
import uuid
import io
import pandas as pd
import codecs

def changeToUnix(str_datetime):
    if not str_datetime:
        return
    datetime = dt.strptime(str_datetime, '%Y/%m/%d')
    return int(datetime.timestamp())

def getUuid():
    return str(uuid.uuid4())

def getNow():
    return str(int(dt.now().timestamp()))

def changeId():
    num = 0
    def genId():
        nonlocal num
        num += 1
        return str(num).zfill(3)
    return genId

def direct_sales(white_list, csv_path):
    item_list = []
    with codecs.open(csv_path, 'r', 'Shift-JIS', 'ignore') as csv_file:
        df = pd.read_csv(csv_file, header=None)
        csvstr = df.iloc[2:].to_csv(index=None, header=None)
        with io.StringIO(csvstr) as s:
            dicts = csv.DictReader(s)
            genId = changeId()
            for row in dicts:
                if int(row['No.']) in white_list:
                    data = {
                        "uuid": getUuid(),
                        "details":{
                            "id": genId(),
                            "name": row['氏名'],
                            "age": row['年齢'],
                            "createdat": changeToUnix(row['登録日']),
                            "updatedat": changeToUnix(row['更新日']),
                        },
                        "action":{
                            "history":{
                                "action_description": [row['対応履歴']],
                                "action_input_date": getNow()
                            }
                        },
                        "remarks": row['備考']
                    }
                    item_list.append(data)
        return item_list

if __name__ == "__main__":
    white_list = [2, 6, 9, 14, 16, 19, 24, 26, 30, 36, 38, 39, 40, 41, 42, 43, 44, 45, 48]
    csv_path = './item_list.csv'
    item_list = direct_sales(white_list, csv_path)

    with open('item_list.json', 'w', encoding='utf-8') as json_file:
        json.dump(item_list, json_file, indent=4, ensure_ascii=False)
        