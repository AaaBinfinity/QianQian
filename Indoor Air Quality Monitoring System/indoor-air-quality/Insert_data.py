import pymysql
import time
import random
from datetime import datetime

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cb050328',
    'db': 'airqualitydb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接到数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()


# 执行创建表的 SQL 语句

conn.commit()

try:
    while True:
        # 生成当前时间
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 模拟生成数据
        co2_concentration = round(random.uniform(300, 1000), 2)  # CO₂ 浓度
        pm25_concentration = round(random.uniform(10, 150), 2)  # PM2.5 浓度
        formaldehyde_concentration = round(random.uniform(0.01, 0.20), 2)  # 甲醛浓度
        temperature = round(random.uniform(15, 30), 2)  # 温度
        humidity = round(random.uniform(20, 80), 2)  # 湿度

        # 插入数据的 SQL 语句
        insert_data_sql = """
            INSERT INTO airqualitydata (timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # 执行 SQL 语句，插入数据
        cursor.execute(insert_data_sql, (
        timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity))

        # 提交事务
        conn.commit()

        # 输出插入的数据
        print(
            f"插入数据: 时间={timestamp}, CO₂浓度={co2_concentration}, PM2.5浓度={pm25_concentration}, 甲醛浓度={formaldehyde_concentration}, 温度={temperature}, 湿度={humidity}")

        # 等待 10 秒
        time.sleep(10)

finally:
    # 关闭数据库连接
    cursor.close()
    conn.close()
