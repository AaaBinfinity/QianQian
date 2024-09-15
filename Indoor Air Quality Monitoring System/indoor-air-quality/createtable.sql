create table if not exists airqualitydata
(
    id                         int auto_increment
        primary key,
    timestamp                  datetime not null,
    co2_concentration          float    not null,
    pm25_concentration         float    not null,
    formaldehyde_concentration float    not null,
    temperature                float    not null,
    humidity                   float    not null
);

create table if not exists airqualitydata_1day
(
    id               int auto_increment
        primary key,
    timestamp        datetime not null,
    avg_co2          float    not null,
    avg_pm25         float    not null,
    avg_formaldehyde float    not null,
    avg_temperature  float    not null,
    avg_humidity     float    not null,
    constraint timestamp
        unique (timestamp)
);

create table if not exists airqualitydata_1h
(
    id               int auto_increment
        primary key,
    timestamp        datetime not null,
    avg_co2          float    not null,
    avg_pm25         float    not null,
    avg_formaldehyde float    not null,
    avg_temperature  float    not null,
    avg_humidity     float    not null,
    constraint timestamp
        unique (timestamp)
);

create table if not exists airqualitydata_1min
(
    id               int auto_increment
        primary key,
    timestamp        datetime not null,
    avg_co2          float    not null,
    avg_pm25         float    not null,
    avg_formaldehyde float    not null,
    avg_temperature  float    not null,
    avg_humidity     float    not null,
    constraint timestamp
        unique (timestamp)
);

create table if not exists airqualitydata_cleaned
(
    id                         int auto_increment
        primary key,
    timestamp                  datetime not null,
    co2_concentration          float    not null,
    pm25_concentration         float    not null,
    formaldehyde_concentration float    not null,
    temperature                float    not null,
    humidity                   float    not null
);


