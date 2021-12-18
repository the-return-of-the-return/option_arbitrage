#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/6/6 15:05
# @Author : xiaochen
# @File   : calc_implied_volatility.py

import pandas as pd
import numpy as np
import scipy.stats as stats


# 计算看涨期权价格
def call_bs_price(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0/K) + (r+np.square(implied_vol)/2)*T)/(implied_vol*np.sqrt(T))
    d2 = (np.log(S0/K) + (r-np.square(implied_vol)/2)*T)/(implied_vol*np.sqrt(T))
    call = S0 * stats.norm.cdf(d1)-K * np.exp(-r * T) * stats.norm.cdf(d2)
    return call


# 计算看跌期权价格
def put_bs_price(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0/K) + (r+np.square(implied_vol)/2)*T)/(implied_vol*np.sqrt(T))
    d2 = (np.log(S0/K) + (r-np.square(implied_vol)/2)*T)/(implied_vol*np.sqrt(T))
    put = -S0 * stats.norm.cdf(-d1)+K * np.exp(-r * T) * stats.norm.cdf(-d2)
    return put


def call_implied_vol(S0, K, T, C, r=0):
    high = 1                #设置波动率初值
    low = 0

    while high-low > 0.0000001:
        midd = (high + low)/2

        if call_bs_price(S0, K, T, midd, r) > C:
            high = midd
        elif call_bs_price(S0, K, T, midd, r) < C:
            low = midd

    implied_vol = (high + low)/2
    return implied_vol





def put_implied_vol(S0, K, T, P, r=0):
    high = 1
    low = 0

    while high-low > 0.0000001:
        midd = (high + low)/2

        if put_bs_price(S0, K, T, midd, r) < P:
            low = midd
        elif put_bs_price(S0, K, T, midd, r) > P:
            high = midd

    implied_vol = (high + low)/2
    return implied_vol

# implied_vol = put_implied_vol(S0=2.736, K=2.700, T=12/252, r=0.0535, P=0.0368)
