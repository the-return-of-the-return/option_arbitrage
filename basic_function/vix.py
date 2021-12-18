#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 3030/4/24 10:10
# @Author : xiaochen
# @File   : vix.py

import pandas as pd
import math
import pandas as pd
import numpy as np
from WindPy import *
w.start()

# 获取一个option list 需要包含到期时间date2end、收盘价格数据close、执行价K，看涨看跌情况call、put
def get_option_list(date_str):
    option_list = w.wset("optionchain", "date="+ date_str +";us_code=510050.SH;option_var=510050OP.SH;call_put=全部")
    option_list = pd.DataFrame(option_list.Data)
    option_list = option_list.T
    option_list.columns = ['us_wind_id', 'us_name', 'OPid', 'wind_id', 'name', 'style', 'K', 'month', 'call_put', 'start_date', 'end_date', 'date2end', 'asset_style', 'multiplier']
    option_list['close'] = option_list['wind_id'].apply(lambda x: w.wsd(x, "close", date_str, date_str, "").Data[0][0])
    return option_list


def get_month_option(date_str):
    # 需要一个函数获取每天的期权list
    option_list = get_option_list(date_str)
    option_list =option_list[option_list['multiplier'] == 10000]

    # 筛选到期日与设定窗口最近的
    if option_list['date2end'].sort_values().drop_duplicates().iloc[0] >= 7:
        option_list_1 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[0]]
        option_list_2 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[1]]
        option_list_3 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[2]]
        option_list_4 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[3]]
    else:
        option_list_1 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[1]]
        option_list_2 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[2]]
        option_list_3 = option_list[option_list['date2end'] == option_list['date2end'].sort_values().drop_duplicates().iloc[3]]
        option_list_4 = pd.DataFrame()
    return option_list_1, option_list_2, option_list_3,option_list_4, option_list


"""获取执行价间隔数据"""
def get_delta_k(k):
    delta_k = pd.Series(map(lambda i: (k.iloc[i + 1] - k.iloc[i - 1]) / 2, (i for i in range(1, k.shape[0] - 1))))
    delta_k = (pd.Series(k.iloc[1] - k.iloc[0]).append(delta_k)).append(pd.Series(k.iloc[k.shape[0] - 1] - k.iloc[k.shape[0] - 2]))
    return delta_k


"""获取认购期权价格与认沽期权价格相差最小的执行价"""
def get_S(option_list):
    call_option = option_list[option_list['call_put'] == "认购"]
    put_option = option_list[option_list['call_put'] == "认沽"]
    min_k = np.min(abs(np.array(call_option["close"]) - np.array(put_option["close"])))
    num = np.where(abs(np.array(call_option["close"]) - np.array(put_option["close"])) == min_k)[0][0]
    k = call_option["K"].iloc[num]
    k = option_list[option_list["K"] == k].sort_values(["call_put"])
    #    min_k = np.min(abs(option_list['K'] - target_k))
    #    option_list = option_list[abs(option_list['K'] - target_k) == min_k]
    return k


"""计算F, T, K0"""
def calc_fk(k, r, option_list):
    t = option_list['date2end'].iloc[0] / 365
    f = k["K"].iloc[0] + math.exp(r * t) * (k["close"].iloc[0] - k["close"].iloc[1])
    min_kf = np.max(option_list["K"][option_list["K"] < f] - f)
    if option_list[option_list["K"] - f == min_kf].empty is False:
        k0 = option_list[option_list["K"] - f == min_kf]["K"].iloc[0]
    else:
        k0 = np.min(option_list['K'])
    return t, f, k0


def cal_p(k, k0, option_list):
    if k < k0:
        p = option_list[option_list['K'] == k][option_list["call_put"] == "认沽"]
        p = p['close'].iloc[-1]
    elif k > k0:
        p = option_list[option_list['K'] == k][option_list["call_put"] == "认购"]
        p = p['close'].iloc[-1]
    elif k == k0:
        p = np.mean(option_list[option_list['K'] == k]['close'])
    return p


def calc_sigma(option_list, r):
    option_list = option_list.sort_values(by=['K'])
    k_list = option_list['K'].drop_duplicates()
    delta_k1 = get_delta_k(k_list)
    k1 = get_S(option_list)
    t1, f1, k0_1 = calc_fk(k1, r, option_list)
    p1 = k_list.apply(lambda x: cal_p(x, k0_1, option_list))
    sigma1 = 2 / t1 * ((np.array(delta_k1) / (np.array(k_list) ** 2) * np.array(p1)) * math.exp(r * t1)).sum() - 1 / t1 * (f1 / k0_1 - 1) ** 2
    return sigma1


def main():
    r = 0.02
    # 需要一个时间序列
    date_series = w.tdays("2020-04-23", "2020-04-23", "")
    date_series = pd.DataFrame(date_series.Data[0])
    date_series[0] = date_series[0].apply(lambda x: str(x)[:10].replace('-', ''))
    ivx = pd.DataFrame(index=date_series[0], columns=["sigma1", "sigma2", "vix", "sigma3", "sigma4"])

    for ii in date_series[0]:
        # 获取当天的所有option
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option(ii)

        sigma1 = calc_sigma(option_list_1, r)
        sigma2 = calc_sigma(option_list_2, r)
        sigma3 = calc_sigma(option_list_3, r)
        if option_list_4.empty is True:
            sigma4 = np.nan
        else:
            sigma4 = calc_sigma(option_list_4, r)

        ivx.loc[ii, "sigma1"] = np.sqrt(sigma1)
        ivx.loc[ii, "sigma2"] = np.sqrt(sigma2)
        k1 = get_S(option_list_1)
        k2 = get_S(option_list_2)
        t1, f1, k0_1 = calc_fk(k1, r, option_list_1)
        t2, f2, k0_2 = calc_fk(k2, r, option_list_2)

        ivx.loc[ii, "sigma3"] = np.sqrt(sigma3)
        ivx.loc[ii, "sigma4"] = np.sqrt(sigma4)
        vix = 100 * np.sqrt((t1 * sigma1 * ((t2 * 365 - 30) / (t2 * 365 - t1 * 365)) + t2 * sigma2 * ((-t1 * 365 + 30) / (t2 * 365 - t1 * 365))) * (365 / 30))
        ivx.loc[ii, "vix"] = vix
        if option_list_4.empty is True:
            ivx = pd.DataFrame(ivx, columns=['sigma4', 'sigma1', 'sigma2', 'sigma3', 'vix'])
        else:
            ivx = pd.DataFrame(ivx, columns=['sigma1', 'sigma2', 'sigma3', 'sigma4', 'vix'])
        print(ii + "complete")
