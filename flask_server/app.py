from datetime import datetime
from operator import ge
from flask import Flask, render_template, request
import pandas as pd
import json
import random
from flask import jsonify
OIL_PROD_NAME = 'Oil Production (m3/d)'
STEAM_INJ_NAME = 'Steam Injection (m3/d)'
DATE_NAME = 'Date'


app = Flask(__name__)

df = pd.read_csv('dataset.csv')

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]

@app.route('/api/predict', methods=['POST'])
def predict_prod():
  json_prod_data = request.json
  print(json_prod_data.keys())
  start_date = datetime.strptime(json_prod_data['startDate'], '%Y-%m-%d')
  end_date = datetime.strptime(json_prod_data['endDate'], '%Y-%m-%d')
  raw_data = json_prod_data['data']
  data = {
    'date': [datetime.strptime(date, '%Y-%m-%d') for date in raw_data['date']],
    #'date': raw_data['date'],
    'oilProd': raw_data['oilProd'],
    'steamInj': raw_data['steamInj']
  }

  predicted_output = get_prediction(data, start_date, end_date)

  return jsonify(predicted_output)

# Dummy function. Replace with class to prediction NN later on.
def get_prediction(data, start, end):
  prediction_data = []
  prediction_dates = []
  for i in range(0, len(data['oilProd'])):
    if (data['date'][i] < end and data['date'][i] > start):
      prediction_data.append(data['oilProd'][i]*random.uniform(0.85,1.15))
      prediction_dates.append(data['date'][i])
  return {'date': prediction_dates, 'data': prediction_data}


# @FIXME: add new post method to handle file uploads.
@app.route('/api/proddata', methods=['GET'])
def get_incomes():
    return jsonify(generate_data_dicts(df))
  
  #return jsonify(generate_data_dicts(df))

def generate_data_dicts(df):
    result_dict = {}
    dff = df.groupby('Well_Pair')
    group_names = dff.groups.keys()
    print(group_names)

    for group in group_names:
        date = dff.get_group(group)[DATE_NAME].to_list()
        oil_prod = dff.get_group(group)[OIL_PROD_NAME].to_list()
        steam_inj = dff.get_group(group)[STEAM_INJ_NAME].to_list()
        dict_tmp = {'date': date, 'oilProd': oil_prod, 'steamInj': steam_inj}
        result_dict[group] = dict_tmp

    return {'wellNames': list(group_names), 'data': result_dict}

@app.route("/")
def hello_world():
  return render_template('index.html')