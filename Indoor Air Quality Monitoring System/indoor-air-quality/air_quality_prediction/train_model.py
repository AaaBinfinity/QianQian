import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 连接数据库并读取数据
def fetch_data(table_name):
    engine = create_engine('mysql+mysqlconnector://root:Cb050328@localhost/airqualitydb')
    query = f"SELECT timestamp, avg_co2, avg_pm25, avg_formaldehyde, avg_temperature, avg_humidity FROM {table_name}"
    df = pd.read_sql(query, engine)
    print(f"已获取 {table_name} 的数据:")
    print(df.head())
    return df


# 数据预处理
def preprocess_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.ffill(inplace=True)  # 使用前向填充填补缺失值
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    print("缩放后的数据:")
    print(scaled_data[:5])
    return scaled_data, scaler


# 创建时间序列
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    # print(f"创建的序列数量: {len(x)}")
    return np.array(x), np.array(y)


# 定义并训练模型
def train_model(x_train, y_train, x_test, y_test, model_name):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(50))
    model.add(Dense(y_train.shape[1]))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=200, batch_size=32, validation_split=0.1)

    # 保存模型
    model.save(model_name)
    print(f"模型已保存为 '{model_name}'")

    # 评估模型
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"{model_name} 的均方误差: {mse}")


# 主函数
def main():
    # 表名列表
    table_names = ['airqualitydata_1h', 'airqualitydata_1day']

    for table_name in table_names:
        print(f"正在处理 {table_name}...")

        # 获取数据
        df = fetch_data(table_name)

        # 检查数据量
        if df.shape[0] <= 5:  # 序列长度
            # print(f"{table_name} 数据量不足，无法创建序列。跳过。")
            continue

        # 预处理数据
        scaled_data, scaler = preprocess_data(df)

        # 创建训练和测试数据
        seq_length = 20  # 时间序列长度，可以根据需要调整
        x, y = create_sequences(scaled_data, seq_length)
        if len(x) == 0:
            print(f"{table_name} 创建的序列数量不足。跳过。")
            continue
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

        # 训练模型
        model_name = f'air_quality_lstm_model_{table_name}.h5'
        train_model(x_train, y_train, x_test, y_test, model_name)


if __name__ == "__main__":
    main()