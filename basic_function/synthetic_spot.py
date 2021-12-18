#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2020/4/1 16:21
# @Author : xiaochen
# @File   : synthetic_spot.py

from option.choose_option_with_hedge import ChooseOption
import pandas as pd
from pylab import mpl
from WindPy import *
w.start()
# import mplfinance as mpf

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

cm = ChooseOption()


def synthetic_spot(date_str, k, option_moveup=5, contract_month=1):
    call_option = cm.choose_option_2(date_str, option_moveup, k, contract_month, 'call')
    put_option = cm.choose_option_2(date_str, option_moveup, k, contract_month, 'put')
    k = call_option['K']
    call_price = call_option['close']
    put_price = put_option['close']
    spot = (call_price - put_price) + k
    return spot
#############################################################################


def main():
    op = w.wsd("510050.SH", "open", "20190101", "20200401", "")
    time_ = [str(x).replace('-', '') for x in op.Times]
    open_ = pd.DataFrame(op.Data[0], index=time_)
    open_.columns = ['open']
    option_moveup = 5
    contract_month = 1
    filepath = 'I:\\option_basis_data\\'
    ana_k = open_['open'].iloc[0]
    option_dura = 0
    basic_data = pd.DataFrame(columns=['synthetic_spot', 'synthetic_spot1', 'synthetic_spot2', 'synthetic_spot3'])
    for i in range(len(open_)):
        if option_dura == 0:
            ana_k = open_['open'].iloc[i]
            option_dura = cm.choose_option(open_.index[i], option_moveup, ana_k, contract_month=1, call_put='call')['date_expiration']
        else:
            option_dura = option_dura - 1
        ii = open_.index[i]

        mm1 = synthetic_spot(ii, ana_k, option_moveup, contract_month)
        if ana_k <= 2.95:
            mm2 = synthetic_spot(ii, ana_k+0.05, option_moveup, contract_month)
        else:
            mm2 = synthetic_spot(ii, ana_k + 0.075, option_moveup, contract_month)
        mm3 = synthetic_spot(ii, ana_k - 0.05, option_moveup, contract_month)
        mm = (mm1+mm2+mm3)/3
        data = pd.DataFrame(data=[[mm, mm1, mm2, mm3]], index=[ii])

        data.columns = ['synthetic_spot', 'synthetic_spot1', 'synthetic_spot2', 'synthetic_spot3']
        basic_data = basic_data.append(data)
        print(ii, 'ok')

    basic_data.to_csv('synthetic_spot.csv')

if __name__ == '__main__':
    main()