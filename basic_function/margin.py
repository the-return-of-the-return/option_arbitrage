#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/7/26 9:55
# @Author : xiaochen
# @File   : margin.py

import pandas as pd
import numpy as np


def open_margin_call(pre_settle, pre_underlying_close, underlying_close, K):
    '''

    :param pre_settle: 期权前结算价
    :param pre_underlying_close: 前收盘价
    :param underlying_close: 当期价格
    :param K: 行权价
    :return:
    '''
    lowest_margin = (pre_settle + max(0.12 * pre_underlying_close - max(K - underlying_close, 0), 0.07 * pre_underlying_close))
    return lowest_margin


def open_margin_put(pre_settle, pre_underlying_close, underlying_close, K):
    lowest_margin = min(pre_settle + max(0.12 * pre_underlying_close - max(underlying_close - K, 0), 0.07 * pre_underlying_close), K)
    return lowest_margin


def maintain_margin_call(settle, underlying_close, K):
    lowest_margin = (settle + max(0.12 * underlying_close - max(K - underlying_close, 0), 0.07 * underlying_close))
    return lowest_margin


def maintain_margin_put(settle, underlying_close, K):
    lowest_margin = min(
        settle + max(0.12 * underlying_close - max(underlying_close - K, 0), 0.07 * underlying_close), K)
    return lowest_margin

if __name__ == '__main__':
    pre_settle = 0.0336
    pre_underlying_close = 0.0336
    underlying_close = 0.0381
    K = 3.0
    margin_price = open_margin_call(pre_settle, pre_underlying_close, underlying_close, K)
    print(margin_price)


