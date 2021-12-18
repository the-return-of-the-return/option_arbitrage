#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/2/15 14:52
# @Author : xiaochen
# @File   : get_date.py

from basic_function import wind_connect as wc
import pandas as pd


# from WindPy import *

def calc_day(start_date, end_date, basic_datapath = r'G:\my_data'):
    '''

    :param start_date: num
    :param end_date: num
    :param basic_datapath:
    :return:
    '''
    daily_date = pd.read_hdf(basic_datapath + '\\date_series.h5', key='daily_date')
    daily_date_num = pd.to_numeric(daily_date[0])
    date_series = pd.DataFrame(daily_date[(daily_date_num >= start_date) & (daily_date_num <= end_date)].values)
    return date_series


def get_date_series(start_date, end_date, filepath = 'G:\\my_data\\'):
    '''

    :param start_date:
    :param end_date:
    :param filepath:
    :return:
    '''
    ws = wc.MSSQL()
    # now_date = time.strftime('%Y%m%d',time.localtime(time.time()))

    select_part = "select F1_1010 from TB_OBJECT_1010"
    condition_part = " where F1_1010 >= '"+str(start_date)+" ' and F1_1010 <= '"+str(end_date)+"' "
    order_part = "order by F1_1010"

    date_series = ws.Selsql(select_part + condition_part + order_part)
    date_series = pd.DataFrame(date_series)
    # print(date_series.head())
    # date_month = pd.DataFrame(data = [i[0:6] for i in date_series[0]])
    # grouped = date_month.groupby(0)
    # idx = grouped.tail(1)
    # date_monthend = date_series.iloc[idx.index, 0]
    #     #
    #     # #date_series.to_hdf(filepath + 'daily_date.h5', key='daily_date')
    #     # date_series.to_hdf(filepath + 'date_series.h5', key='daily_date')
    #     # date_monthend.to_hdf(filepath + 'date_series.h5', key='monthend_date')
    #     # ####################获取月度数据##############################
    return date_series

def get_fix_window_series(end_date_str, window):
    '''

    :param end_date: 结束时间str
    :param window: 时间窗口
    :return:
    '''

    ws = wc.MSSQL()
    # now_date = time.strftime('%Y%m%d',time.localtime(time.time()))

    select_part = "select F1_1010 from TB_OBJECT_1010"
    condition_part = " where F1_1010 >= '" + '20061229' + " ' and F1_1010 <= '" + end_date_str + "' "
    order_part = "order by F1_1010"

    date_series = ws.Selsql(select_part + condition_part + order_part)
    date_series = pd.DataFrame(date_series)
    date_series = date_series.iloc[-window:, :]
    return date_series


