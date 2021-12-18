#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/6/5 10:57
# @Author : xiaochen
# @File   : get_etf_daily_data.py

from basic_function import wind_connect as wc
import pandas as pd


def get_daily_close(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms =wc.MSSQL()
    select_part = 'SELECT F2_1120, F8_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'close']
    result['date'] = result['date'].astype(str)
    # result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_high(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1120, F6_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'high']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_low(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1120, F7_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'low']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_open(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1120, F5_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'open']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_preclose(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1120, F4_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'preclose']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_backadj_close(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1425, F7_1425 from TB_OBJECT_1425 A JOIN TB_OBJECT_0001 B ON A.F1_1425 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1425>='"+startdate_str+"' AND F2_1425<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1425'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'close']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_backadj_close_api(startdate_str, enddate_str, wind_id):
    w.start()
    close = w.wsd(wind_id, "close", startdate_str, enddate_str, "PriceAdj=F")
    t = [str(x)[:10].replace('-', '') for x in close.Times]
    close = pd.DataFrame(data=close.Data[0], index=t, columns=['close'])
    return close


def get_daily_backadj_ETF_close(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL(db="windfdb")
    select_part = 'SELECT TRADE_DT, S_DQ_ADJCLOSE from ChinaClosedFundEODPrice '
    condition_part = "WHERE S_INFO_WINDCODE='"+wind_id+"' AND TRADE_DT>='"+startdate_str+"' AND TRADE_DT<='"+enddate_str+"'"
    order_part = 'ORDER BY TRADE_DT'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'close']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_backadj_preclose(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1425, F3_1425 from TB_OBJECT_1425 A JOIN TB_OBJECT_0001 B ON A.F1_1425 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1425>='"+startdate_str+"' AND F2_1425<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1425'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'preclose']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result
#
#
def get_daily_adjust_factor(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1425, F10_1425 from TB_OBJECT_1425 A JOIN TB_OBJECT_0001 B ON A.F1_1425 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1425>='"+startdate_str+"' AND F2_1425<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1425'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'adj_factor']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_adjust_factor_ETF(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL(db='windfdb')
    select_part = 'SELECT TRADE_DT, S_DQ_ADJFACTOR from ChinaClosedFundEODPrice '
    condition_part = "WHERE S_INFO_WINDCODE='"+wind_id+"' AND TRADE_DT>='"+startdate_str+"' AND TRADE_DT<='"+enddate_str+"'"
    order_part = 'ORDER BY TRADE_DT'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'adj_factor']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_IOPV(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据,基金iopv
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL(db='windfdb')
    select_part = 'SELECT PRICE_DATE, F_IOPV_NAV from CMFIOPVNAV '
    condition_part = "WHERE F_INFO_WINDCODE='"+wind_id+"' AND PRICE_DATE>='"+startdate_str+"' AND PRICE_DATE<='"+enddate_str+"'"
    order_part = 'ORDER BY PRICE_DATE'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'iopv']
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.astype(float)
    return result


def get_daily_preadj_close(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    adjust_factor = get_daily_adjust_factor(startdate_str, enddate_str, wind_id)
    preadj_factor = adjust_factor / adjust_factor.iloc[-1, :]
    close_raw_data = get_daily_close(startdate_str, enddate_str, wind_id)
    result = close_raw_data*preadj_factor
    result.columns = ['preadj_close']
    result = result.set_index('date')
    result = result.astype(float)
    return result


def calc_preadj_price(raw_price, adj_factor):
    return raw_price[0]*adj_factor['adj_factor']


def get_daily_aver_price(startdate_str, enddate_str, wind_id):
    '''
    通过wind底层数据库提取每日交易所数据
    :param startdate_str: 提取期初日期
    :param enddate_str: 提取期末日期
    :param wind_id: 提取的wind代码
    :return:
    '''
    ms = wc.MSSQL()
    select_part = 'SELECT F2_1120, F9_1120, F11_1120 from TB_OBJECT_1120 A JOIN TB_OBJECT_0001 B ON A.F1_1120 = B.F16_0001 '
    condition_part = "WHERE F1_0001='"+wind_id+"' AND F2_1120>='"+startdate_str+"' AND F2_1120<='"+enddate_str+"'"
    order_part = 'ORDER BY F2_1120'
    select_result = ms.Selsql(select_part+' '+condition_part+' '+order_part)
    result = pd.DataFrame(select_result)
    result.columns = ['date', 'amount', 'volume']
    result['aver_price'] = result['volume']/result['amount']*10
    result['date'] = result['date'].astype(str)
    result = result.set_index('date')
    result = result.loc[:, 'aver_price']
    result = result.astype(float)
    return result


if __name__ == '__main__':
    startdate_str = '20190501'
    enddate_str = '20190531'
    wind_id = '510050.SH'
    a = get_daily_close(startdate_str, enddate_str, wind_id)
    print(a)
