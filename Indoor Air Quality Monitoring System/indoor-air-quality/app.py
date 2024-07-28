from flask import Flask
import pymysql
import threading
import random
from datetime import datetime
import sched
import time
import logging

app = Flask(__name__)

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cb050328',
    'db': 'airqualitydb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 创建数据库连接
def get_db_connection():
    return pymysql.connect(**db_config)

# 创建表如果不存在
def create_table_if_not_exists():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
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
            cursor.execute(sql)
        conn.commit()
        logging.info("表 'airqualitydata' 已就绪。")
    except Exception as e:
        logging.error(f"创建表时出错: {e}")
    finally:
        conn.close()

# 插入模拟数据到数据库
def insert_mock_data():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO airqualitydata (timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()
            co2_concentration = round(random.uniform(300.00, 600.00), 2)
            pm25_concentration = round(random.uniform(10.00, 50.00), 2)
            formaldehyde_concentration = round(random.uniform(0.00, 0.10), 2)
            temperature = round(random.uniform(18.00, 28.00), 2)
            humidity = round(random.uniform(30.00, 70.00), 2)
            cursor.execute(sql, (now, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity))
        conn.commit()
        logging.info(f"插入的数据: 时间: {now}, CO2浓度: {co2_concentration}, PM2.5浓度: {pm25_concentration}, 甲醛浓度: {formaldehyde_concentration}, 温度: {temperature}, 湿度: {humidity}")
    except Exception as e:
        logging.error(f"插入数据时出错: {e}")
    finally:
        conn.close()

# 调度任务
scheduler = sched.scheduler(time.time, time.sleep)

def schedule_task():
    scheduler.enter(2, 1, schedule_task)
    insert_mock_data()

# 开始调度任务
def start_scheduler():
    logging.info("开始调度任务...")
    scheduler.enter(0, 1, schedule_task)
    scheduler.run()

# 使用线程来运行调度任务
thread = threading.Thread(target=start_scheduler)
thread.start()

# Flask 路由
@app.route('/')
def index():
    return "数据插入服务正在运行。"

if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(debug=True)
