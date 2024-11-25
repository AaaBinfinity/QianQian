

from sqlalchemy import create_engine, text
import pandas as pd
import schedule
import time

# 数据库连接设置
engine = create_engine('mysql+pymysql://root:Cb050328@localhost:3306/airqualitydb')


# 定义预处理函数
def preprocess_data(df):
    # 处理缺失值
    df.ffill(inplace=True)  # 向前填充缺失值
    df.bfill(inplace=True)  # 向后填充缺失值

    # 处理异常值
    thresholds = {
        'pm25_concentration': (0, 500),
        'co2_concentration': (400, 5000),
        'formaldehyde_concentration': (0, 0.17),
        'temperature': (-10, 50),
        'humidity': (0, 100)
    }

    for column, (min_val, max_val) in thresholds.items():
        df[column] = df[column].clip(lower=min_val, upper=max_val)  # 将列值裁剪到指定范围内

    # 处理重复数据
    df.drop_duplicates(subset='timestamp', keep='last', inplace=True)  # 保留时间戳最新的记录，去除重复项

    return df

def process_real_time_data():
    try:
        # 读取原始数据
        query = 'SELECT * FROM airqualitydata ORDER BY timestamp DESC LIMIT 1'  # 获取最新的记录
        df = pd.read_sql(query, engine)  # 从数据库中读取数据到DataFrame

        if not df.empty:
            # 获取最新数据的时间戳
            latest_timestamp = df['timestamp'].iloc[0]

            # 使用连接对象检查 airqualitydata_cleaned 表中是否已有相同时间戳的记录
            with engine.connect() as conn:
                check_query = text('SELECT COUNT(*) FROM airqualitydata_cleaned WHERE timestamp = :timestamp')
                count = conn.execute(check_query, {'timestamp': latest_timestamp}).scalar()

            if count == 0:
                # 预处理数据
                df_cleaned = preprocess_data(df)  # 预处理数据

                # 打印预处理后的数据
                print("预处理后的数据:")
                print(df_cleaned)

                # 插入预处理后的数据
                with engine.connect() as conn:
                    df_cleaned.to_sql('airqualitydata_cleaned', conn, if_exists='append', index=False)  # 将数据插入到清理后的表中



            else:
                print("数据时间戳已存在，无需插入。")
    except Exception as e:
        print(f"处理数据时发生错误: {e}")  # 捕获并打印异常信息


# 设置调度任务，每10秒运行一次
schedule.every(10).seconds.do(process_real_time_data)  # 每10秒执行一次数据处理任务

# 保持程序运行
while True:
    schedule.run_pending()  # 执行调度任务
    time.sleep(1)  # 每秒检查一次任务
