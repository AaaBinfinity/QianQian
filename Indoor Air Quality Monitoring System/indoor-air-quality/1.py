import pandas as pd
from sqlalchemy import create_engine, text
import schedule
import time

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:Cb050328@localhost:3306/airqualitydb')

# 定义表结构
tables = {
    'airqualitydata_1min': 'CREATE TABLE IF NOT EXISTS airqualitydata_1min ('
                           'id INT AUTO_INCREMENT PRIMARY KEY, '
                           'timestamp DATETIME NOT NULL, '
                           'avg_co2_concentration FLOAT, '
                           'avg_pm25_concentration FLOAT, '
                           'avg_formaldehyde_concentration FLOAT, '
                           'avg_temperature FLOAT, '
                           'avg_humidity FLOAT)',

    'airqualitydata_1h': 'CREATE TABLE IF NOT EXISTS airqualitydata_1h ('
                         'id INT AUTO_INCREMENT PRIMARY KEY, '
                         'timestamp DATETIME NOT NULL, '
                         'avg_co2_concentration FLOAT, '
                         'avg_pm25_concentration FLOAT, '
                         'avg_formaldehyde_concentration FLOAT, '
                         'avg_temperature FLOAT, '
                         'avg_humidity FLOAT)',

    'airqualitydata_1day': 'CREATE TABLE IF NOT EXISTS airqualitydata_1day ('
                           'id INT AUTO_INCREMENT PRIMARY KEY, '
                           'timestamp DATETIME NOT NULL, '
                           'avg_co2_concentration FLOAT, '
                           'avg_pm25_concentration FLOAT, '
                           'avg_formaldehyde_concentration FLOAT, '
                           'avg_temperature FLOAT, '
                           'avg_humidity FLOAT)'
}

# 创建新表
with engine.connect() as conn:
    for table_name, create_table_sql in tables.items():
        conn.execute(text(create_table_sql))

# 定义聚合函数
def aggregate_and_insert(freq, table_name):
    try:
        # 读取原始数据
        query = "SELECT * FROM airqualitydata_cleaned"
        df = pd.read_sql(query, engine)

        # 设置时间戳为索引
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        # 计算平均值
        df_resampled = df.resample(freq).mean().reset_index()
        print(f"Original columns: {df_resampled.columns.tolist()}")

        # 去除 'id' 列
        if 'id' in df_resampled.columns:
            df_resampled.drop(columns=['id'], inplace=True)

        # 重命名列名以匹配数据库表
        df_resampled.columns = ['timestamp', 'avg_co2_concentration', 'avg_pm25_concentration', 'avg_formaldehyde_concentration', 'avg_temperature', 'avg_humidity']

        # 打印重命名后的列名
        print(f"Renamed columns: {df_resampled.columns.tolist()}")

        # 清理目标表中的现有数据
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {table_name}"))

        # 插入数据
        df_resampled.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"{table_name} 数据更新完成！")
    except Exception as e:
        print(f"Error while aggregating and inserting into {table_name}: {e}")

# 定义定时任务
schedule.every(1).minutes.do(aggregate_and_insert, 'T', 'airqualitydata_1min')
schedule.every().hour.do(aggregate_and_insert, 'H', 'airqualitydata_1h')
schedule.every().day.at("00:00").do(aggregate_and_insert, 'D', 'airqualitydata_1day')

# 运行定时任务
while True:
    schedule.run_pending()
    time.sleep(1)
