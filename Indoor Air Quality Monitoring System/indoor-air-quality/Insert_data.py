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

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

<<<<<<< HEAD
# 提交事务
=======

# 执行创建表的 SQL 语句

>>>>>>> d8e037a36c2edf6ebad5baaeb702287f73112dd6
conn.commit()

try:
    while True:
        # 获取当前时间
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 生成随机数据
        co2_concentration = round(random.uniform(300, 350), 2)  # CO₂ 浓度
        pm25_concentration = round(random.uniform(10, 15), 2)  # PM2.5 浓度
        formaldehyde_concentration = round(random.uniform(0.05, 0.07), 2)  # 甲醛浓度
        temperature = round(random.uniform(15, 17), 2)  # 温度
        humidity = round(random.uniform(20, 25), 2)  # 湿度

        # 打印将要插入的数据
        print(f"将要插入的数据: 时间={timestamp}, CO₂浓度={co2_concentration}, PM2.5浓度={pm25_concentration}, 甲醛浓度={formaldehyde_concentration}, 温度={temperature}, 湿度={humidity}")

        # 插入数据
        insert_data_sql = """
            INSERT INTO airqualitydata (timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_data_sql, (
        timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity))

        # 提交事务
        conn.commit()

        # 打印插入成功的信息
        print(f"插入数据成功: 时间={timestamp}, CO₂浓度={co2_concentration}, PM2.5浓度={pm25_concentration}, 甲醛浓度={formaldehyde_concentration}, 温度={temperature}, 湿度={humidity}")

        # 暂停10秒
        time.sleep(10)

finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()
