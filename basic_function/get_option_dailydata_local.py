#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/7/1 9:11
# @Author : xiaochen
# @File   : get_option_dailydata_local.py

import pandas as pd
import sqlite3

# ID,WIND_ID,TRADE_DT,OPTION_NAME,CALL_PUT,K,OPTION_STARTTRADE,OPTION_ENDTRADE,OPEN,HIGH,LOW,CLOSE,SETTLE,PRESETTLE,VOLUME,AMOUNT,OI
# 数据标签， wind代码， 交易日期， 期权全名， 认购认沽， 执行价， 期权上市日， 期权最后交易日， 开， 高， 低， 收， 结算价， 前结算价， 交易额， 交易量， 持仓量


def get_option_dailydata_local(startdate_str, enddate_str, wind_id, name, *a):
    select_info = str()
    conn = sqlite3.connect('E:\\xc_project\\option\\basic_data\\option.db')
    c = conn.cursor()
    for i in a:
        select_info = select_info + ',' + i
    select_part = "SELECT WIND_ID, TRADE_DT" + select_info + " from OPTION_LOCAL"
    condition_part = "WHERE TRADE_DT >='" + startdate_str + "' AND TRADE_DT<='" + enddate_str + "' AND WIND_ID='" + wind_id + "'"
    order_part = "ORDER BY TRADE_DT"
    cursor = c.execute(select_part + ' ' + condition_part + ' ' + order_part)
    res = c.fetchall()
    res = pd.DataFrame(res)
    res.columns = ['wind_id', 'date'] + name
    return res

if __name__ == '__main__':
    m = get_option_dailydata_local('20190601', '20190630', '10001862.SH', ['close', 'open'],'CLOSE', 'OPEN')
