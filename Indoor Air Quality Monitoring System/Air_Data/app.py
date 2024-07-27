from flask import Flask, jsonify
import mysql.connector
from threading import Timer
import datetime
import random

app = Flask(__name__)

# 配置数据库连接
db_config = {
    'user': 'root',
    'password': 'Cb050328',
    'host': 'localhost',
    'database': 'AirQualityDB'
}


# 创建数据库连接
def get_db_connection():
    return mysql.connector.connect(**db_config)


# 创建表
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IndoorAirQuality (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            co2_concentration DECIMAL(5, 2) NOT NULL,
            pm25_concentration DECIMAL(5, 2) NOT NULL,
            formaldehyde_concentration DECIMAL(5, 2) NOT NULL,
            temperature DECIMAL(5, 2) NOT NULL,
            humidity DECIMAL(5, 2) NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()


# 插入模拟数据
def insert_mock_data():
    print("Inserting mock data")
    connection = get_db_connection()
    cursor = connection.cursor()

    current_time = datetime.datetime.now()
    co2_concentration = round(random.uniform(400, 800), 2)
    pm25_concentration = round(random.uniform(0, 100), 2)
    formaldehyde_concentration = round(random.uniform(0, 1), 2)
    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(30, 70), 2)

    cursor.execute("""
        INSERT INTO IndoorAirQuality (timestamp, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (current_time, co2_concentration, pm25_concentration, formaldehyde_concentration, temperature, humidity))

    connection.commit()
    cursor.close()
    connection.close()
    print("Inserted mock data")


# 定期插入数据的函数
def periodic_insertion():
    print("Inserting periodic data")
    insert_mock_data()
    Timer(5.0, periodic_insertion).start()  # 每5秒插入一次数据


# 启动 Flask 应用时创建表并开始定期插入数据
def initialize():
    print("Initializing database")
    create_table()
    periodic_insertion()


# 提供一个简单的 API 来查看数据
@app.route('/api/airquality/data', methods=['GET'])
def get_data():
    print("Getting data")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM IndoorAirQuality")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)


if __name__ == '__main__':
    initialize()
    app.run(debug=True)
