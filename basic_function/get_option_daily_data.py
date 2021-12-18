#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/6/26 10:52
# @Author : xiaochen
# @File   : get_option_daily_data.py

from basic_function.get_date import *
import basic_function.wind_connect as wc
import pandas as pd
# from WindPy import *

def get_option_daily_close(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    if int(startdate_str) <= 20180912 and int(enddate_str) >20180912:
        ms1 = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_CLOSE from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + '20180912' + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms1.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part1 = pd.DataFrame(select_result)
        result_part1.columns = ['date', 'close']
        result_part1 = result_part1.set_index('date')
        result_part1 = result_part1.astype(float)

        ms2 = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_CLOSE from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + '20180913' + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms2.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part2 = pd.DataFrame(select_result)
        result_part2.columns = ['date', 'close']
        result_part2 = result_part2.set_index('date')
        result_part2 = result_part2.astype(float)

        result = pd.concat([result_part1, result_part2])
    else:
        if int(enddate_str) <= 20180912:
            ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        elif int(startdate_str) >= 20180913:
            ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_CLOSE from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'

        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result = pd.DataFrame(select_result)
        result.columns = ['date', 'close']
        result = result.set_index('date')
        result = result.astype(float)

    return result


def get_option_daily_open(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    if int(startdate_str) <= 20180912 and int(enddate_str) >20180912:
        ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_OPEN from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + '20180912' + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part1 = pd.DataFrame(select_result)
        result_part1.columns = ['date', 'open']
        result_part1 = result_part1.set_index('date')
        result_part1 = result_part1.astype(float)

        ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_OPEN from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + '20180913' + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part2 = pd.DataFrame(select_result)
        result_part2.columns = ['date', 'open']
        result_part2 = result_part2.set_index('date')
        result_part2 = result_part2.astype(float)

        result = pd.concat([result_part1, result_part2], axis=1)
    else:
        if int(enddate_str) <= 20180912:
            ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        elif int(startdate_str) >= 20180913:
            ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_OPEN from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result = pd.DataFrame(select_result)
        result.columns = ['date', 'open']
        result = result.set_index('date')
        result = result.astype(float)

    return result


def get_option_daily_high(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    if int(startdate_str) <= 20180912 and int(enddate_str) >20180912:
        ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_HIGH from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + '20180912' + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part1 = pd.DataFrame(select_result)
        result_part1.columns = ['date', 'high']
        result_part1 = result_part1.set_index('date')
        result_part1 = result_part1.astype(float)

        ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_HIGH from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + '20180913' + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part2 = pd.DataFrame(select_result)
        result_part2.columns = ['date', 'high']
        result_part2 = result_part2.set_index('date')
        result_part2 = result_part2.astype(float)

        result = pd.concat([result_part1, result_part2], axis=1)
    else:
        if int(enddate_str) <= 20180912:
            ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        elif int(startdate_str) >= 20180913:
            ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_HIGH from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result = pd.DataFrame(select_result)
        result.columns = ['date', 'high']
        result = result.set_index('date')
        result = result.astype(float)

    return result


def get_option_daily_low(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    if int(startdate_str) <= 20180912 and int(enddate_str) >20180912:
        ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_LOW from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + '20180912' + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part1 = pd.DataFrame(select_result)
        result_part1.columns = ['date', 'low']
        result_part1 = result_part1.set_index('date')
        result_part1 = result_part1.astype(float)

        ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_LOW from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + '20180913' + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part2 = pd.DataFrame(select_result)
        result_part2.columns = ['date', 'low']
        result_part2 = result_part2.set_index('date')
        result_part2 = result_part2.astype(float)

        result = pd.concat([result_part1, result_part2], axis=1)
    else:
        if int(enddate_str) <= 20180912:
            ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        elif int(startdate_str) >= 20180913:
            ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT TRADE_DT, S_DQ_LOW from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result = pd.DataFrame(select_result)
        result.columns = ['date', 'low']
        result = result.set_index('date')
        result = result.astype(float)

    return result


def get_option_daily_all(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    ID INT PRIMARY KEY     NOT NULL,
#        WIND_ID           TEXT    NOT NULL,
#        TRADE_DT          INT     NOT NULL,
#        OPEN              FLOAT NULL,
#        HIGH              FLOAT NULL,
#        LOW               FLOAT NULL,
#        CLOSE             FLOAT NULL,
#        SETTLE            FLOAT NULL,
#        PRESETTLE         FLOAT NULL,
#        VOLUME            FLOAT NULL,
#        AMOUNT            FLOAT NULL,
#        OI                FLOAT NULL
    '''
    if int(startdate_str) <= 20180912 and int(enddate_str) >20180912:
        ms1 = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_HIGH, S_DQ_LOW, S_DQ_CLOSE, S_DQ_SETTLE, ' \
                      'S_DQ_PRESETTLE, S_DQ_VOLUME, S_DQ_AMOUNT, S_DQ_OI from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + '20180912' + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms1.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part1 = pd.DataFrame(select_result)
        result_part1.columns = ['wind_id', 'date', 'open', 'high', 'low', 'close', 'settle', 'presettle', 'volume', 'amount', 'hold']
        # result_part1 = result_part1.set_index('date')
        # result_part1 = result_part1.astype(float)

        ms2 = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT S_INFO_WINDCODE, TRADE_DT, S_DQ_OPEN, S_DQ_HIGH, S_DQ_LOW, S_DQ_CLOSE, S_DQ_SETTLE, ' \
                      'S_DQ_PRESETTLE, S_DQ_VOLUME, S_DQ_AMOUNT, S_DQ_OI from CHINAOPTIONEODPRICES'
        condition_part = "WHERE S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + '20180913' + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'
        select_result = ms2.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result_part2 = pd.DataFrame(select_result)
        result_part2.columns = ['wind_id', 'date', 'open', 'high', 'low', 'close', 'settle', 'presettle', 'volume', 'amount', 'hold']

        result = pd.concat([result_part1, result_part2])
    else:
        if int(enddate_str) <= 20180912:
            ms = wc.MSSQL(host="10.100.106.219", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        elif int(startdate_str) >= 20180913:
            ms = wc.MSSQL(host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="windfdb")
        select_part = 'SELECT A.S_INFO_WINDCODE, A.TRADE_DT, A.S_DQ_OPEN, A.S_DQ_HIGH, A.S_DQ_LOW, A.S_DQ_CLOSE, A.S_DQ_SETTLE, ' \
                      'A.S_DQ_PRESETTLE, A.S_DQ_VOLUME, A.S_DQ_AMOUNT, A.S_DQ_OI, B.S_INFO_COUNIT from CHINAOPTIONEODPRICES A JOIN ChinaOptionDescription B ON A.S_INFO_WINDCODE = B.S_INFO_WINDCODE'
        condition_part = "WHERE A.S_INFO_WINDCODE='" + wind_id + "' AND TRADE_DT>='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "'"
        order_part = 'ORDER BY TRADE_DT'

        select_result = ms.Selsql(select_part + ' ' + condition_part + ' ' + order_part)
        result = pd.DataFrame(select_result)

        result.columns = ['wind_id', 'date', 'open', 'high', 'low', 'close', 'settle', 'presettle', 'volume', 'amount', 'hold', 'multiplier']

    return result


if __name__ == '__main__':
    a = get_option_daily_close('20180606', '20180606', wind_id='510050.SH')
    print(a)