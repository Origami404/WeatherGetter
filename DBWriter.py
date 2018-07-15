import sqlite3
import os
import Logger


def weather_connect():
    return sqlite3.connect('./JiangmenWeather.db')


# TODO 把这些东西都改改啊妈耶重复的打开数据库/链接/关闭出现了多少次啊. 写个高阶函数简便一下
def init():
    if os.path.exists('inited.conf'):
        Logger.get_logger('DBWriter_init').info('Has been init, skip')
        return
    create_tables()
    os.mknod('inited.conf')
    Logger.get_logger('DBWriter_init').info('DB init successfully!')


def insert(table_name, column_list, values_list):
    connection = weather_connect()
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO {table_name} ({str(column_list)[1:-1]}) VALUES ({str(values_list)[1:-1]});')
    connection.commit()
    Logger.get_logger('DBWriter_insert')\
        .debug(f'Has insert values( {column_list} {values_list} ) into table: {table_name}')


def create_tables():
    connection = weather_connect()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE now (
        UPDATE_TIME   DATE PRIMARY KEY NOT NULL ,
        TEMP          INT              NOT NULL ,
        WEATHER       TEXT             NOT NULL ,
        WIND_ANG      INT              NOT NULL ,
        WIND_DIR      TEXT             NOT NULL ,
        WIND_SC       INT              NOT NULL ,
        WIND_SPC      INT              NOT NULL ,
        HUMIDITY      INT              NOT NULL ,
        PRECIPITATION REAL             NOT NULL ,
        VISIBILITY    INT              NOT NULL 
    );""")
    cursor.execute("""CREATE TABLE air(
    UPDATE_TIME DATE PRIMARY KEY NOT NULL ,
    AQI         INT              NOT NULL ,
    MAIN        TEXT             NOT NULL ,
    PM10        INT              NOT NULL ,
    PM25        INT              NOT NULL ,
    NO2         INT              NOT NULL ,
    SO2         INT              NOT NULL ,
    CO          REAL             NOT NULL ,
    O3          INT              NOT NULL 
    );""")
    cursor.execute(make_lifestyle_table_sql())
    cursor.execute("""CREATE TABLE sun_and_moon (
        UPDATE_TIME DATE PRIMARY KEY NOT NULL ,
        SUNRISE     DATE             NOT NULL ,
        SUNSET      DATE             NOT NULL , 
        MOONRISE    DATE             NOT NULL ,
        MOONSET     DATE             NOT NULL 
    );""")
    connection.commit()
    Logger.get_logger('DBWriter_create_tables').info('Create Tables Success!')


def show_tables():
    connection = weather_connect()
    cursor = connection.cursor()
    result = cursor.execute("select name from sqlite_master where type = 'table';")
    return [x[0] for x in result.fetchall()]


def make_lifestyle_table_sql():
    lifestyle_type_list = ['comf', 'cw', 'drsg', 'flu', 'sport', 'trav', 'uv', 'air', ]
    sql_command = 'CREATE TABLE lifestyle (\nUPDATE_TIME DATE PRIMARY KEY NOT NULL,\n'
    for lifestyle_type in lifestyle_type_list:
        sql_command = sql_command + f'{lifestyle_type.upper()}_BRF TEXT NOT NULL,\n' \
                                    f'{lifestyle_type.upper()}_TXT TEXT NOT NULL,\n'
    return sql_command[:-2] + ');'




