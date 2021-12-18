#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2020/4/3 11:14
# @Author : xiaochen
# @File   : renew_skew.py


from matplotlib.ticker import LinearLocator, FormatStrFormatter

from option.calc_skew import skew_basic_info, calcS, calcSkew
from option.calc_vix import get_month_option, get_month_option_365

from basic_function.get_date import get_date_series
import pandas as pd
import numpy as np
from WindPy import *
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
w.start()
def renew_skew_main(end_date):
    r = 0.02
    origin_data = pd.read_csv('E:\\xc_project\\option\\skew.csv')
    start_date = str(origin_data.iloc[-1, 0]+1)
    # # start_date = '20150209'
    # ii = datetime.datetime.today()
    # end_date = str(int(ii.strftime('%Y%m%d')))
    # end_date = '20210120'
    date_series = get_date_series(start_date, end_date)
    # date_series1 = get_date_series(start_date, str(int(end_date)+10000))
    skew = pd.DataFrame(index=date_series[0], columns=['S1', 'S2', 'skew'])

    for ii in date_series[0]:
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option_365(ii)
        S1 = calcS(option_list_1, r)
        S2 = calcS(option_list_2, r)
        t1 = option_list_1['date2end'].iloc[0]
        t2 = option_list_2['date2end'].iloc[0]
        sk = calcSkew(S1, S2, t1, t2)
        skew.loc[ii, 'S1'] = S1
        skew.loc[ii, 'S2'] = S2
        skew.loc[ii, 'skew'] = sk
        print(ii + ' OK!')
    # skew.to_csv("E:\\xc_project\\option\\skew.csv", encoding='gbk')
    skew.to_csv("E:\\xc_project\\option\\skew.csv", encoding='gbk', mode='a', header=0)

def plot_skew(num, end_date):
    skew = pd.read_csv('E:\\xc_project\\option\\skew.csv', index_col='date', encoding='gbk')
    skew = skew.iloc[-num:, :]
    # ii = datetime.datetime.today()
    # end_date = str(int(ii.strftime('%Y%m%d')))
    # end_date = '20201014'
    # vix = vix.fillna(0)
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    colors = ['#1f77b4',
              '#ff7f0e',
              '#2ca02c',
              '#d62728',
              '#9467bd',
              '#8c564b',
              '#e377c2',
              '#7f7f7f',
              '#bcbd22',
              '#17becf',
              '#1a55FF']

    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    data_temp = np.array(skew['skew'].tolist())

    labels = skew.index.tolist()
    ax.plot(data_temp, linewidth=2, label='vix')
    x = np.arange(len(labels))  # the label locations
    x_tick = np.arange(0, len(labels), 20)
    ax.set_xticks(x_tick)
    ax.set_xticklabels([labels[i] for i in x_tick])
    ax.grid(True, axis='y', linestyle='--')
    ax.set_xlabel('日期')
    ax.set_ylabel('skew情况')
    ax.legend()
    ax.set_title(end_date + ' skew数据', fontdict={'weight': 'normal', 'size': 20})
    plt.savefig('E:\\xc\\日报\\' + end_date + '\\skew.png')
    plt.close()


if __name__ == '__main__':
    # renew_skew_main('20210121')
    plot_skew(500, '20210121')