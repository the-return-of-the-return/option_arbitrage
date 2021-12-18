#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2020/3/21 13:57
# @Author : xiaochen
# @File   : renew_vix.py


from option.calc_vix import get_month_option, calc_sigma, get_S, calc_fk, get_month_option_000300, get_month_option_365
from basic_function.get_date import get_date_series
import pandas as pd
import numpy as np

import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def renew_vix_main(end_date):
    r = 0.02
    origin_data = pd.read_csv('E:\\xc_project\\option\\vix.csv')
    # 获取一个时间序列，可以从wind提取一个
    start_date = datetime.datetime.strptime(str(origin_data.iloc[-1, 0]), '%Y%m%d')+datetime.timedelta(days=1)
    start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
    # start_date = '20190101'
    # start_date = 2020
    # ii = datetime.datetime.today()
    # end_date = str(int(ii.strftime('%Y%m%d')))
    # end_date = '20210107'

    date_series = get_date_series(start_date, end_date)
    # date_series1 = get_date_series(start_date, str(int(end_date)+10000))
    #计算vix
    ivx = pd.DataFrame(index=date_series[0], columns=["sigma1", "sigma2", "vix", "sigma3", "sigma4"])

    for ii in date_series[0]:
        # 获取当天的所有option
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option_365(ii)

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

    ivx.to_csv("E:\\xc_project\\option\\vix.csv", encoding='gbk', mode='a', header=0)
    # ivx.to_csv("E:\\xc_project\\option\\vix.csv", encoding='gbk')


def renew_vix_main_300(end_date):
    r = 0.02
    origin_data = pd.read_csv('E:\\xc_project\\option\\vix510300.csv')
    start_date = datetime.datetime.strptime(str(origin_data.iloc[-1, 0]), '%Y%m%d')+datetime.timedelta(days=1)
    start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
    # start_date = '20191223'
    # start_date = 2020
    # ii = datetime.datetime.today()
    # end_date = str(int(ii.strftime('%Y%m%d')))
    # end_date = '20210107'

    date_series = get_date_series(start_date, end_date)
    # date_series1 = get_date_series(start_date, str(int(end_date)+10000))
    ivx = pd.DataFrame(index=date_series[0], columns=["sigma1", "sigma2", "vix", "sigma3", "sigma4"])

    for ii in date_series[0]:
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option_365(ii, option_string='510300OP.SH')

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

    ivx.to_csv("E:\\xc_project\\option\\vix510300.csv", encoding='gbk', mode='a', header=0)
    # ivx.to_csv("E:\\xc_project\\option\\vix510300.csv", encoding='gbk')


def renew_vix_main_000300():
    r = 0.02
    origin_data = pd.read_csv('E:\\xc_project\\option\\vix000300.csv')
    start_date = datetime.datetime.strptime(str(origin_data.iloc[-1, 0]), '%Y%m%d')+datetime.timedelta(days=1)
    start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
    # start_date = '20191223'
    # start_date = 2020
    ii = datetime.datetime.today()
    end_date = str(int(ii.strftime('%Y%m%d')))
    # end_date = '20200527'

    date_series = get_date_series(start_date, end_date)
    # date_series1 = get_date_series(start_date, str(int(end_date)+10000))
    ivx = pd.DataFrame(index=date_series[0], columns=["sigma1", "sigma2", "vix", "sigma3", "sigma4"])

    for ii in date_series[0]:
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option_000300(ii)

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

    ivx.to_csv("E:\\xc_project\\option\\vix000300.csv", encoding='gbk', mode='a', header=0)
    # ivx.to_csv("E:\\xc_project\\option\\vix000300.csv", encoding='gbk')


def plot_surface_ivx():
    vix = pd.read_csv('E:\\xc_project\\option\\vix.csv', index_col=0, encoding='gbk')
    # vix = vix.fillna(0)
    fig = plt.figure()

    ax = Axes3D(fig)
    Y = np.array(vix.index[-10:])
    X = np.arange(4)
    X, Y = np.meshgrid(X, Y)
    Z = np.array(vix.iloc[-10:, :4],dtype=np.float)*100
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    x_labels = np.array(vix.columns[:4])
    y_labels = np.array(vix.index[-10:])
    x = np.arange(4)
    y = np.arange(10)
    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xticklabels([x_labels[i] for i in x])
    ax.set_yticklabels([y_labels[i] for i in y])
    ax.set_zlim(10, 60)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.set_xlabel('到期月')
    # ax.set_ylabel('日期')
    ax.set_title('波动率 term structure', fontdict={'weight': 'normal', 'size': 20})


def plot_ivx(num, end_date):
    vix = pd.read_csv('E:\\xc_project\\option\\vix.csv', index_col=0, encoding='gbk')
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
    for i in range(num):
        data_temp = vix.iloc[-i-1, :4]
        ax.plot(data_temp * 100, color=colors[i], linewidth=2, label=str(vix.index[-i-1]))
    x_tick = np.arange(4)
    labels = ['sigma1', 'sigma2', 'sigma3', 'sigma4']
    ax.set_xticks(x_tick)
    ax.set_xticklabels([labels[i] for i in x_tick])
    ax.legend()
    ax.set_title(end_date + '波动率 term structure', fontdict={'weight': 'normal', 'size': 20})
    ax.set_xlabel('到期月')
    ax.set_ylabel('波动率（%）')
    plt.savefig('E:\\xc\\日报\\' + end_date + '\\波动率term_structure.png')
    plt.close()

    vix = pd.read_csv('E:\\xc_project\\option\\vix.csv', index_col=0, encoding='gbk')
    vol = pd.read_csv('E:\\xc_project\\option\\his_vol.csv', index_col=0, encoding='gbk')
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    data_temp = np.array(vix['vix'].tolist())
    data_temp2 = np.array(vol['his_vol'].tolist())
    data_temp2 = data_temp2 * 100
    labels = vix.index.tolist()
    ax.plot(data_temp, linewidth=2, label='vix')
    ax.plot(data_temp2, linewidth=2, label='his_vol')
    x = np.arange(len(labels))  # the label locations
    x_tick = np.arange(0, len(labels), 20)
    ax.set_xticks(x_tick)
    ax.set_xticklabels([labels[i] for i in x_tick])
    ax.grid(True, axis='y', linestyle='--')
    ax.set_xlabel('日期')
    ax.set_ylabel('vix值及历史vol')
    ax.legend()
    ax.set_title(end_date + ' vix及vol数据', fontdict={'weight': 'normal', 'size': 20})
    plt.savefig('E:\\xc\\日报\\' + end_date + '\\vix及vol.png')
    plt.close()



if __name__ == '__main__':
    r = 0.02
    # origin_data = pd.read_csv('E:\\xc_project\\option\\vix.csv')
    # start_date = datetime.datetime.strptime(str(origin_data.iloc[-1, 0]), '%Y%m%d')+datetime.timedelta(days=1)
    # start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
    start_date = '20191223'
    # start_date = 2020
    ii = datetime.datetime.today()
    end_date = str(int(ii.strftime('%Y%m%d')))
    end_date = '20200609'

    date_series = get_date_series(start_date, end_date)
    ivx = pd.DataFrame(index=date_series[0], columns=["sigma1", "sigma2", "vix", "sigma3", "sigma4"])

    for ii in date_series[0]:
        option_list_1, option_list_2, option_list_3, option_list_4, option_list = get_month_option_365(ii, option_string='510300OP.SH')

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

    # ivx.to_csv("E:\\xc_project\\option\\vix_temp.csv", encoding='gbk', mode='a', header=0)
    ivx.to_csv("E:\\xc_project\\option\\vix_temp_new_365_510300.csv", encoding='gbk')



