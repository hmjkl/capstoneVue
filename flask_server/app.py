from datetime import datetime
from operator import ge
from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import json
import random
from flask import jsonify
import modelInfo as mi
DATE_NAME = 'Date'
OIL_PROD_NAME = 'Oil Production (m3/d)'
STEAM_INJ_NAME = 'Steam Injection (m3/d)'
WATER_PROD_NAME = 'Water Production (m3/d)'
PRESSURE_NAME = 'Pressure (kPa)'


app = Flask(__name__)
CORS(app)

df = pd.read_csv('dataset.csv')


@app.route('/api/csv-transform', methods=['POST'])
def form_to_json():
    if 'file' not in request.files:
        print('incorrect form received')

    file = request.files['file']
    response = pd.read_csv(file)
    return jsonify(generate_data_dicts(response))


@app.route('/api/model-info', methods=['GET'])
def model_to_json():
    resp = {'inputChunkLength': mi.get_prev_days(), 'outputChunkLength':
            mi.get_forward_days(), 'inputParameters': mi.get_historical_params()}
    return jsonify(resp)


@app.route('/api/predict', methods=['POST'])
def predict_prod():
    json_prod_data = request.json
    print(json_prod_data.keys())
    start_date = datetime.strptime(json_prod_data['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(json_prod_data['endDate'], '%Y-%m-%d')
    raw_data = json_prod_data['data']
    data = {
        'date': [datetime.strptime(date, '%Y-%m-%d') for date in raw_data['date']],
        # 'date': raw_data['date'],
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
            prediction_data.append(
                data['oilProd'][i]*random.uniform(0.85, 1.15))
            prediction_dates.append(data['date'][i])
    return {'date': prediction_dates, 'data': prediction_data}


@app.route('/api/proddata', methods=['GET'])
def fetch_default_data():
    return jsonify(generate_data_dicts(df))


# returns a JSONable dict that looks like
# {
#  wellNames: ['WP1', 'WP2', ...],
#  data: 'WP1' {
#    date:
#    steamInj:
#    oilProd:
#    waterProd:
#    pressure:
#  }
#  data: 'WP2' {
#    date:
#    steamInj:
#    oilProd:
#    waterProd:
#    pressure:
#  }
#  ...
# }
def generate_data_dicts(df):
    result_dict = {}
    dff = df.groupby('Well_Pair')
    group_names = dff.groups.keys()
    print(group_names)

    # @FIXME: stop using hardcoded json_resp_names and columns. Needs frontend work.
    columns_to_get = [DATE_NAME, STEAM_INJ_NAME,
                      OIL_PROD_NAME, WATER_PROD_NAME, PRESSURE_NAME]
    json_response_names = ['date', 'steamInj',
                           'oilProd', 'waterProd', 'pressure']

    for group in group_names:
        tmp = []
        for column in columns_to_get:
            tmp.append(dff.get_group(group)[column].to_list())

        res = dict(zip(json_response_names, tmp))
        result_dict[group] = res

    return {'wellNames': list(group_names), 'data': result_dict}


@app.route("/")
def idx():
    return render_template('index.html')
