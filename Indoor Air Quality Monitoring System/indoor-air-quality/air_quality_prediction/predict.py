import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, jsonify
<<<<<<< HEAD
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有源进行跨域请求

from flask_cors import CORS
from flask import Flask

app = Flask(__name__)

# 允许从所有来源进行跨域请求
CORS(app, resources={r"/*": {"origins": "*"}})

#
app = Flask(__name__)
=======
from datetime import datetime

app = Flask(__name__)
>>>>>>> d8e037a36c2edf6ebad5baaeb702287f73112dd6

# 连接数据库并读取数据
def fetch_data(table_name, n_rows):
    engine = create_engine('mysql+mysqlconnector://root:Cb050328@localhost/airqualitydb')
    query = f"SELECT timestamp, avg_co2, avg_pm25, avg_formaldehyde, avg_temperature, avg_humidity FROM {table_name} ORDER BY timestamp DESC LIMIT {n_rows}"
    df = pd.read_sql(query, engine)
    df = df.sort_values(by='timestamp')  # 按时间升序排序
    return df
<<<<<<< HEAD
@app.errorhandler(404)
def not_found(error):
    return jsonify({"错误": "未找到该路径"}), 404
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')
=======
>>>>>>> d8e037a36c2edf6ebad5baaeb702287f73112dd6

# 数据预处理
def preprocess_data(df, scaler=None):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.ffill(inplace=True)  # 使用前向填充填补缺失值

    if scaler is None:
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df)
    else:
        scaled_data = scaler.transform(df)

<<<<<<< HEAD
    return scaled_data, scaler  

=======
    return scaled_data, scaler
>>>>>>> d8e037a36c2edf6ebad5baaeb702287f73112dd6

# 创建时间序列
def create_sequences(data, seq_length):
    x = []
    for i in range(len(data) - seq_length + 1):
        x.append(data[i:i + seq_length])
    return np.array(x)

# 预测未来值
def predict_future_values(model, data, seq_length, n_future):
    predictions = []
    current_sequence = data[-seq_length:]

    for _ in range(n_future):
        if len(current_sequence.shape) == 4:
            current_sequence = np.squeeze(current_sequence, axis=1)

        prediction = model.predict(current_sequence)
        predictions.append(prediction[0])

        prediction = np.expand_dims(prediction, axis=1)

        current_sequence = np.append(current_sequence[:, 1:, :], prediction, axis=1)

    return np.array(predictions)

# 预测每小时未来4个时间点的数据
@app.route('/predict/h', methods=['GET'])
def predict_1h():
    table_name = 'airqualitydata_1h'
    seq_length = 20
    n_future = 4

    df = fetch_data(table_name, seq_length)
    if df.shape[0] < seq_length:
        return jsonify({'错误': '数据不足，无法进行预测'}), 400

    model = load_model('air_quality_lstm_model_airqualitydata_1h.h5')

    scaled_data, scaler = preprocess_data(df)
    x_input = create_sequences(scaled_data, seq_length)
    predictions_scaled = predict_future_values(model, x_input, seq_length, n_future)
    predictions = scaler.inverse_transform(predictions_scaled)

    timestamps = pd.date_range(start=df.index[-1], periods=n_future + 1, freq='H')[1:]

    # 保留两位小数
    results = [
        {
            'timestamp': str(timestamps[i]),
            'avg_co2': round(float(predictions[i][0]), 2),
            'avg_pm25': round(float(predictions[i][1]), 2),
            'avg_formaldehyde': round(float(predictions[i][2]), 2),
            'avg_temperature': round(float(predictions[i][3]), 2),
            'avg_humidity': round(float(predictions[i][4]), 2)
        }
        for i in range(n_future)
    ]

    return jsonify(results)

# 预测每日未来4天的数据
@app.route('/predict/day', methods=['GET'])
def predict_day():
    table_name = 'airqualitydata_1day'
    seq_length = 20
    n_future = 4

    df = fetch_data(table_name, seq_length)
    if df.shape[0] < seq_length:
        return jsonify({'错误': '数据不足，无法进行预测'}), 400

    model = load_model('air_quality_lstm_model_airqualitydata_1day.h5')

    scaled_data, scaler = preprocess_data(df)
    x_input = create_sequences(scaled_data, seq_length)
    predictions_scaled = predict_future_values(model, x_input, seq_length, n_future)
    predictions = scaler.inverse_transform(predictions_scaled)

    timestamps = pd.date_range(start=df.index[-1], periods=n_future + 1, freq='D')[1:]

    # 保留两位小数
    results = [
        {
            'timestamp': str(timestamps[i]),
            'avg_co2': round(float(predictions[i][0]), 2),
            'avg_pm25': round(float(predictions[i][1]), 2),
            'avg_formaldehyde': round(float(predictions[i][2]), 2),
            'avg_temperature': round(float(predictions[i][3]), 2),
            'avg_humidity': round(float(predictions[i][4]), 2)
        }
        for i in range(n_future)
    ]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
