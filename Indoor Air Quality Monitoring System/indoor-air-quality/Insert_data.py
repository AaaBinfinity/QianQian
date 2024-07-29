
'''''import pymysql
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

# 创建表的 SQL 语句
create_table_sql = """
CREATE TABLE IF NOT EXISTS airqualitydata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    co2_concentration FLOAT NOT NULL,
    pm25_concentration FLOAT NOT NULL,
    formaldehyde_concentration FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL
)
"""

# 执行创建表的 SQL 语句
cursor.execute(create_table_sql)
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


以上的TABLE是原始数据，它每10秒钟会插入一条新的数据，我需要用python对他进行实时的数据预处理，创建一个新表，用来存储预处理之后的数据，
预处理：
1. 处理缺失值
缺失值可以通过以下几种方法处理：

删除含有缺失值的记录：如果缺失值的数量较少，可以选择删除这些记录。但如果缺失值很多，这种方法可能不合适。
填充缺失值：
使用前一个有效值填充（前向填充）。
使用后一个有效值填充（后向填充）。
使用均值、中位数或众数填充。
对于时间序列数据，可以使用插值方法进行填充。
2. 处理异常值
异常值是那些偏离正常范围的数据点。可以使用以下方法检测和处理异常值：

统计方法：使用均值和标准差（例如，均值±3倍标准差）来检测异常值。
分位数方法：使用四分位数（IQR）方法来识别异常值。异常值通常定义为低于 Q1 - 1.5 * IQR 或高于 Q3 + 1.5 * IQR 的值。
基于业务规则：根据领域知识定义合理的值范围（例如，PM2.5浓度应在0 - 500 µg/m³范围内）。
3. 数据平滑
对时间序列数据进行平滑处理，可以帮助减少噪音：

移动平均：计算滑动窗口中的数据平均值。
指数平滑：使用加权平均的方法，给予最近的数据点更大的权重。
4. 数据标准化/归一化
将数据缩放到统一范围内，以便进行后续分析：

标准化：将数据转换为均值为0，标准差为1的标准正态分布。
归一化：将数据缩放到指定范围（例如0到1）。
5. 处理重复数据
检查并删除重复的记录，以避免数据重复对分析的影响。
'''

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

# 创建表的 SQL 语句
create_table_sql = """
CREATE TABLE IF NOT EXISTS airqualitydata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    co2_concentration FLOAT NOT NULL,
    pm25_concentration FLOAT NOT NULL,
    formaldehyde_concentration FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL
)
"""

# 执行创建表的 SQL 语句
cursor.execute(create_table_sql)
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
