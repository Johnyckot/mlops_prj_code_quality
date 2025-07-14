import os
import requests
import numpy as np
import pandas as pd
import json

def create_tf_serving_json(data):
    return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

def score_model(dataset):
    url = 'https://dbc-88b955c3-50c9.cloud.databricks.com/serving-endpoints/soft_defect_predict/invocations'
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}', 'Content-Type': 'application/json'}
    ds_dict = {'dataframe_split': dataset.to_dict(orient='split')} if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(method='POST', headers=headers, url=url, data=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()



test_data = {"loc":[1.0, 1.1]
            ,"v(g)":[1.0, 1.4]
            ,"ev(g)":[1.0, 1.4]
            ,"iv(g)":[1.0, 1.4]
            ,"n":[1.0, 1.3]
            ,"v":[1.0, 1.3]
            ,"l":[1.0, 1.3]
            ,"d":[1.0, 1.3]
            ,"i":[1.0, 1.3]
            ,"e":[1.0, 1.3]
            ,"b":[1.0, 1.3]
            ,"t":[1.0, 1.3]
            ,"lOCode":[1.0, 2]
            ,"lOComment":[1.0, 2]
            ,"lOBlank":[1.0, 2]
            ,"locCodeAndComment":[1.0, 2]
            ,"uniq_Op":[1.0, 1.2]
            ,"uniq_Opnd":[1.0, 1.2]
            ,"total_Op":[1.0, 1.2]
            ,"total_Opnd":[1.0, 1.2]
            ,"branchCount":[1.0, 1.4]
            }

expected_predictions = {'predictions': [1, 0]}

predictions = score_model(pd.DataFrame(test_data))
print(predictions)

assert predictions == expected_predictions, f"Expected {expected_predictions}, but got {predictions}"
