import pymysql
import schedule
import time
import logging
from datetime import datetime, timedelta

# 设置日志记录配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cb050328',
    'database': 'airqualitydb',
    'cursorclass': pymysql.cursors.DictCursor
}

# 创建表的函数
def create_tables():
    logging.info('创建表格如果不存在。')
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 创建 airqualitydata_1min 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS airqualitydata_1min (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME NOT NULL UNIQUE,
                    avg_co2 FLOAT NOT NULL,
                    avg_pm25 FLOAT NOT NULL,
                    avg_formaldehyde FLOAT NOT NULL,
                    avg_temperature FLOAT NOT NULL,
                    avg_humidity FLOAT NOT NULL
                );
            ''')
            logging.info('创建表格 airqualitydata_1min。')
            # 创建 airqualitydata_1h 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS airqualitydata_1h (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME NOT NULL UNIQUE,
                    avg_co2 FLOAT NOT NULL,
                    avg_pm25 FLOAT NOT NULL,
                    avg_formaldehyde FLOAT NOT NULL,
                    avg_temperature FLOAT NOT NULL,
                    avg_humidity FLOAT NOT NULL
                );
            ''')
            logging.info('创建表格 airqualitydata_1h。')
            # 创建 airqualitydata_1day 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS airqualitydata_1day (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME NOT NULL UNIQUE,
                    avg_co2 FLOAT NOT NULL,
                    avg_pm25 FLOAT NOT NULL,
                    avg_formaldehyde FLOAT NOT NULL,
                    avg_temperature FLOAT NOT NULL,
                    avg_humidity FLOAT NOT NULL
                );
            ''')
            logging.info('创建表格 airqualitydata_1day。')
        connection.commit()
    finally:
        connection.close()

# 计算并插入每分钟平均值的函数
def calculate_minutely_averages():
    logging.info('计算每分钟的平均值。')
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT MIN(timestamp) as min_time, MAX(timestamp) as max_time FROM airqualitydata_cleaned')
            result = cursor.fetchone()
            if result:
                min_time = result['min_time'].replace(second=0, microsecond=0)
                max_time = result['max_time'].replace(second=0, microsecond=0)
                current_time = min_time
                while current_time <= max_time:
                    next_time = current_time + timedelta(minutes=1)
                    cursor.execute('''
                        SELECT 
                            AVG(co2_concentration) as avg_co2, 
                            AVG(pm25_concentration) as avg_pm25, 
                            AVG(formaldehyde_concentration) as avg_formaldehyde, 
                            AVG(temperature) as avg_temperature, 
                            AVG(humidity) as avg_humidity
                        FROM airqualitydata_cleaned
                        WHERE timestamp >= %s AND timestamp < %s;
                    ''', (current_time, next_time))
                    avg_result = cursor.fetchone()
                    if all(value is not None for value in avg_result.values()):
                        cursor.execute('''
                            INSERT INTO airqualitydata_1min (timestamp, avg_co2, avg_pm25, avg_formaldehyde, avg_temperature, avg_humidity)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                avg_co2 = VALUES(avg_co2),
                                avg_pm25 = VALUES(avg_pm25),
                                avg_formaldehyde = VALUES(avg_formaldehyde),
                                avg_temperature = VALUES(avg_temperature),
                                avg_humidity = VALUES(avg_humidity);
                        ''', (current_time, avg_result['avg_co2'], avg_result['avg_pm25'], avg_result['avg_formaldehyde'], avg_result['avg_temperature'], avg_result['avg_humidity']))
                        logging.info(f'插入/更新每分钟平均值 {current_time}。')
                    current_time = next_time
        connection.commit()
    finally:
        connection.close()

# 计算并插入每小时平均值的函数
def calculate_hourly_averages():
    logging.info('计算每小时的平均值。')
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT MIN(timestamp) as min_time, MAX(timestamp) as max_time FROM airqualitydata_cleaned')
            result = cursor.fetchone()
            if result:
                min_time = result['min_time'].replace(minute=0, second=0, microsecond=0)
                max_time = result['max_time'].replace(minute=0, second=0, microsecond=0)
                current_time = min_time
                while current_time <= max_time:
                    next_time = current_time + timedelta(hours=1)
                    cursor.execute('''
                        SELECT 
                            AVG(co2_concentration) as avg_co2, 
                            AVG(pm25_concentration) as avg_pm25, 
                            AVG(formaldehyde_concentration) as avg_formaldehyde, 
                            AVG(temperature) as avg_temperature, 
                            AVG(humidity) as avg_humidity
                        FROM airqualitydata_cleaned
                        WHERE timestamp >= %s AND timestamp < %s;
                    ''', (current_time, next_time))
                    avg_result = cursor.fetchone()
                    if all(value is not None for value in avg_result.values()):
                        cursor.execute('''
                            INSERT INTO airqualitydata_1h (timestamp, avg_co2, avg_pm25, avg_formaldehyde, avg_temperature, avg_humidity)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                avg_co2 = VALUES(avg_co2),
                                avg_pm25 = VALUES(avg_pm25),
                                avg_formaldehyde = VALUES(avg_formaldehyde),
                                avg_temperature = VALUES(avg_temperature),
                                avg_humidity = VALUES(avg_humidity);
                        ''', (current_time, avg_result['avg_co2'], avg_result['avg_pm25'], avg_result['avg_formaldehyde'], avg_result['avg_temperature'], avg_result['avg_humidity']))
                        logging.info(f'插入/更新每小时平均值 {current_time}。')
                    current_time = next_time
        connection.commit()
    finally:
        connection.close()

# 计算并插入每日平均值的函数
def calculate_daily_averages():
    logging.info('计算每日的平均值。')
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT MIN(timestamp) as min_time, MAX(timestamp) as max_time FROM airqualitydata_cleaned')
            result = cursor.fetchone()
            if result:
                min_time = result['min_time'].replace(hour=0, minute=0, second=0, microsecond=0)
                max_time = result['max_time'].replace(hour=0, minute=0, second=0, microsecond=0)
                current_time = min_time
                while current_time <= max_time:
                    next_time = current_time + timedelta(days=1)
                    cursor.execute('''
                        SELECT 
                            AVG(co2_concentration) as avg_co2, 
                            AVG(pm25_concentration) as avg_pm25, 
                            AVG(formaldehyde_concentration) as avg_formaldehyde, 
                            AVG(temperature) as avg_temperature, 
                            AVG(humidity) as avg_humidity
                        FROM airqualitydata_cleaned
                        WHERE timestamp >= %s AND timestamp < %s;
                    ''', (current_time, next_time))
                    avg_result = cursor.fetchone()
                    if all(value is not None for value in avg_result.values()):
                        cursor.execute('''
                            INSERT INTO airqualitydata_1day (timestamp, avg_co2, avg_pm25, avg_formaldehyde, avg_temperature, avg_humidity)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                avg_co2 = VALUES(avg_co2),
                                avg_pm25 = VALUES(avg_pm25),
                                avg_formaldehyde = VALUES(avg_formaldehyde),
                                avg_temperature = VALUES(avg_temperature),
                                avg_humidity = VALUES(avg_humidity);
                        ''', (current_time, avg_result['avg_co2'], avg_result['avg_pm25'], avg_result['avg_formaldehyde'], avg_result['avg_temperature'], avg_result['avg_humidity']))
                        logging.info(f'插入/更新每日平均值 {current_time}。')
                    current_time = next_time
        connection.commit()
    finally:
        connection.close()

# 定时任务
def setup_scheduled_tasks():
    logging.info('设置定时任务。')
    schedule.every().minute.at(":00").do(calculate_minutely_averages)
    schedule.every().hour.at(":00").do(calculate_hourly_averages)
    schedule.every().day.at("00:00").do(calculate_daily_averages)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    create_tables()
    # 先处理历史数据
    calculate_minutely_averages()
    calculate_hourly_averages()
    calculate_daily_averages()
    # 设置定时任务
    setup_scheduled_tasks()

