-- 创建一个名为airqualitydata的表，如果不存在则创建
create table if not exists airqualitydata
(
    id                         int auto_increment
        primary key, -- 设置id为主键
    timestamp                  datetime not null, -- 设置timestamp为日期时间类型，不能为空
    co2_concentration          float    not null, -- 设置co2_concentration为浮点型，不能为空
    pm25_concentration         float    not null, -- 设置pm25_concentration为浮点型，不能为空
    formaldehyde_concentration float    not null, -- 设置formaldehyde_concentration为浮点型，不能为空
    temperature                float    not null, -- 设置temperature为浮点型，不能为空
    humidity                   float    not null -- 设置humidity为浮点型，不能为空
);

-- 创建一个名为airqualitydata_1day的表，如果不存在则创建
create table if not exists airqualitydata_1day
(
    id               int auto_increment
        primary key, -- 设置id为主键
    timestamp        datetime not null, -- 设置timestamp为日期时间类型，不能为空
    avg_co2          float    not null, -- 设置avg_co2为浮点型，不能为空
    avg_pm25         float    not null, -- 设置avg_pm25为浮点型，不能为空
    avg_formaldehyde float    not null, -- 设置avg_formaldehyde为浮点型，不能为空
    avg_temperature  float    not null, -- 设置avg_temperature为浮点型，不能为空
    avg_humidity     float    not null, -- 设置avg_humidity为浮点型，不能为空
    constraint timestamp -- 设置timestamp为唯一约束
        unique (timestamp) -- 设置timestamp为唯一约束
);

-- 创建一个名为airqualitydata_1h的表，如果不存在则创建
create table if not exists airqualitydata_1h
(
    id               int auto_increment
        primary key, -- 设置id为主键
    timestamp        datetime not null, -- 设置timestamp为日期时间类型，不能为空
    avg_co2          float    not null, -- 设置avg_co2为浮点型，不能为空
    avg_pm25         float    not null, -- 设置avg_pm25为浮点型，不能为空
    avg_formaldehyde float    not null, -- 设置avg_formaldehyde为浮点型，不能为空
    avg_temperature  float    not null, -- 设置avg_temperature为浮点型，不能为空
    avg_humidity     float    not null, -- 设置avg_humidity为浮点型，不能为空
    constraint timestamp -- 设置timestamp为唯一约束
        unique (timestamp) -- 设置timestamp为唯一约束
);

-- 创建一个名为airqualitydata_1min的表，如果不存在则创建
create table if not exists airqualitydata_1min
(
    id               int auto_increment
        primary key, -- 设置id为主键
    timestamp        datetime not null, -- 设置timestamp为日期时间类型，不能为空
    avg_co2          float    not null, -- 设置avg_co2为浮点型，不能为空
    avg_pm25         float    not null, -- 设置avg_pm25为浮点型，不能为空
    avg_formaldehyde float    not null, -- 设置avg_formaldehyde为浮点型，不能为空
    avg_temperature  float    not null, -- 设置avg_temperature为浮点型，不能为空
    avg_humidity     float    not null, -- 设置avg_humidity为浮点型，不能为空
    constraint timestamp -- 设置timestamp为唯一约束
        unique (timestamp) -- 设置timestamp为唯一约束
);

-- 创建一个名为airqualitydata_cleaned的表，如果不存在则创建
create table if not exists airqualitydata_cleaned
(
    id                         int auto_increment
        primary key, -- 设置id为主键
    timestamp                  datetime not null, -- 设置timestamp为日期时间类型，不能为空
    co2_concentration          float    not null, -- 设置co2_concentration为浮点型，不能为空
    pm25_concentration         float    not null, -- 设置pm25_concentration为浮点型，不能为空
    formaldehyde_concentration float    not null, -- 设置formaldehyde_concentration为浮点型，不能为空
    temperature                float    not null, -- 设置temperature为浮点型，不能为空
    humidity                   float    not null -- 设置humidity为浮点型，不能为空
);