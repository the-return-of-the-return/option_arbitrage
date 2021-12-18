import pandas as pd
import numpy as np
import sqlite3
import scipy.interpolate as spi
import matplotlib.pyplot as plt
from dateutil.parser import parse
from basic_function.calc_Greek import calc_put_delta
from basic_function.calc_implied_volatility import put_implied_vol
from basic_function.get_etf_daily_data import get_daily_close
import datetime
from statsmodels.tsa.stattools import adfuller  #adf检验
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math


# 获取此时间段所有的期权到期日
def get_end_date(start_date=20160323, end_date=20200226):
    my_db = sqlite3.connect('E:\\XX\\option_arbitrage\\data\\raw\\option.db')
    c = my_db.cursor()
    sql =f"select distinct OPTION_ENDTRADE from OPTION_LOCAL where OPTION_ENDTRADE>={start_date} " \
         f"and OPTION_ENDTRADE<={end_date} order by OPTION_ENDTRADE "
    c.execute(sql)
    end_date_all = [i[0] for i in c.fetchall()]
    return end_date_all


# 针对每一个近月到期日，获取到期日的前五周时间里的所有交易日，不超过25个
def get_trade_date(end_date):
    start_date = parse(str(end_date))+datetime.timedelta(days=-35)
    start_date = int(start_date.strftime("%Y%m%d"))
    # 连接数据库，选出所有交易日
    my_db = sqlite3.connect('E:\\XX\\option_arbitrage\\data\\raw\\option.db')
    c = my_db.cursor()
    sql = f"SELECT DISTINCT trade_dt\nFROM OPTION_LOCAL ol\nwhere TRADE_DT>={start_date} " \
              f"and TRADE_DT <{end_date}\norder by TRADE_DT"
    c.execute(sql)
    trade_dt_total = c.fetchall()
    trade_dt_total = [i[0] for i in trade_dt_total]
    return trade_dt_total


# 根据交易日和近月到期日选出所有的k和close
def get_k_and_close(i, j):
    my_db = sqlite3.connect('E:\\XX\\option_arbitrage\\data\\raw\\option.db')
    c = my_db.cursor()
    sql = f"SELECT k,CLOSE\nfrom OPTION_LOCAL ol\nwhere " \
          f"TRADE_DT ={j} and CALL_PUT='put' and OPTION_ENDTRADE={i} " \
          f"and CONTRACT_MULTIPLIER ='10000'\norder by K ASC"
    c.execute(sql)
    result = c.fetchall()
    k_total = [i[0] for i in result]
    close_total = [i[1] for i in result]
    return k_total, close_total


# 根据所有的合约到期日，计算出每个到期日对应的波动率偏度，数据量不超过48*25个
def seasonal_skew_put(end_date_all):
    R = 0.02

    # 获取etf每天的收盘价
    etf_daily_close_df = get_daily_close(str(20160101), str(20201231), '510050.SH')
    etf_daily_close_df.set_index(['date'], inplace=True)

    # 定义一个字典储存到期天数及其对应的iv_diff
    iv_diff_all = {}
    iv_diff_all_list = []
    days_to_maturity_list = []

    for i in end_date_all:
        print('到期日：', i)
        trade_dt_total = get_trade_date(i)
        for j in trade_dt_total:
            print('交易日', j)
            days = (parse(str(i)) - parse(str(j))).days
            T = days / 365
            s0 = etf_daily_close_df.loc[j, 'close']
            k_total, close_total = get_k_and_close(i, j)
            n = len(close_total)

            # 计算各个k值对应的隐含波动率
            iv_total = [put_implied_vol(s0, k_total[i], T, close_total[i], R) for i in range(n)]
            # 计算各个k对应的delta
            delta_total = [calc_put_delta(s0, k_total[i], T, iv_total[i], R) for i in range(n)]

            iv_total = [i[1] for i in sorted(zip(delta_total, iv_total))]
            delta_total = sorted(delta_total)
            iv_delta_025 = np.interp(-0.25, delta_total, iv_total)
            iv_delta_05 = np.interp(-0.5, delta_total, iv_total)
            iv_diff = iv_delta_025 - iv_delta_05
            iv_diff_all_list.append(iv_diff)
            days_to_maturity_list.append(days)

            # 将这个值储存在字典中
            if days in iv_diff_all.keys():
                iv_diff_all[days].append(iv_diff)
            else:
                iv_diff_all[days] = [iv_diff]
    return iv_diff_all, iv_diff_all_list, days_to_maturity_list


# 将计算得到的波动率偏度数据进行一系列的处理，比如做曲线拟合，检验自相关性，检验平稳性，等等
def skew_put_regression():
    # 一年十二个月，没一个月都有一个期权到期日，针对四年共48个到期日，计算出所有天数对应的iv_diff
    end_date_all = get_end_date(20160323, 20200226)
    iv_diff_all_dict, iv_diff_all_list, days_to_maturity_list = seasonal_skew_put(end_date_all)

    # 自相关图检验
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(iv_diff_all_list, lags=20, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(iv_diff_all_list, lags=20, ax=ax2)
    plt.show()

    # 检验平稳性
    temp = np.array(iv_diff_all_list)
    t = adfuller(temp)  # ADF检验
    output = pd.DataFrame(index=['Test Statistic Value', "p-value", "Lags Used", "Number of Observations Used",
                                 "Critical Value(1%)", "Critical Value(5%)", "Critical Value(10%)"], columns=['value'])
    output['value']['Test Statistic Value'] = t[0]
    output['value']['p-value'] = t[1]
    output['value']['Lags Used'] = t[2]
    output['value']['Number of Observations Used'] = t[3]
    output['value']['Critical Value(1%)'] = t[4]['1%']
    output['value']['Critical Value(5%)'] = t[4]['5%']
    output['value']['Critical Value(10%)'] = t[4]['10%']
    print(output)

    # 波动率序列
    print(iv_diff_all_dict)
    plt.plot(iv_diff_all_list)
    plt.ylabel('iv_diff')
    plt.show()

    # 波动率偏度的均值
    iv_diff_all_mean = []
    iv_diff_all_days = []
    sum_count = 0
    sum_iv_diff = 0
    for i in sorted(iv_diff_all_dict.keys()):
        iv_diff_all_days.append(i)
        iv_diff_all_mean.append(np.mean(iv_diff_all_dict[i]))
        sum_iv_diff += sum(iv_diff_all_dict[i])
        sum_count += len(iv_diff_all_dict[i])
    mean = sum_iv_diff/sum_count

    index_days_to_maturity = []
    for i in range(len(iv_diff_all_days)):
        index_days_to_maturity.append(iv_diff_all_mean[i]/mean)
    plt.plot(iv_diff_all_days, index_days_to_maturity)
    plt.ylabel('index')
    plt.show()

    # 波动率偏度的线性拟合
    mean_x = np.mean(days_to_maturity_list)
    mean_y = np.mean(iv_diff_all_list)
    list_1 = [(j-mean_x)*(i-mean_y) for (i, j) in zip(iv_diff_all_list, days_to_maturity_list)]
    list_2 = [(i-mean_x)**2 for i in days_to_maturity_list]
    a = sum(list_1)/sum(list_2)
    b = mean_y - a * mean_x
    plt.scatter(days_to_maturity_list, iv_diff_all_list)
    x = np.arange(1, 35, 1)
    y = a * x + b
    plt.plot(x, y)
    plt.show()

    # 波动率偏度的多项式拟合
    x_up = []
    x_low = []
    y_up = []
    y_low = []
    for i in sorted(iv_diff_all_dict.keys()):
        a = iv_diff_all_dict[i]
        b = sorted(a)
        a.sort(reverse=True)
        for j in range(math.ceil(len(a)*0.4)):
            y_up.append(a[j])
            x_up.append(i)
            y_low.append(b[j])
            x_low.append(i)

    x_up = np.array(x_up).reshape(-1, 1)
    y_up = np.array(y_up).reshape(-1, 1)
    days_to_maturity_list = np.array(days_to_maturity_list).reshape(-1, 1)
    iv_diff_all_list = np.array(iv_diff_all_list).reshape(-1, 1)
    x_low = np.array(x_low).reshape(-1, 1)
    y_low = np.array(y_low).reshape(-1, 1)

    poly_features_3 = PolynomialFeatures(degree=6)
    linear_reg_best = LinearRegression()
    fit_x = np.linspace(start=1, stop=35, num=1000).reshape(-1, 1)

    linear_reg_best.fit(poly_features_3.fit_transform(x_up), y_up)
    fit_linear_best_up = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))
    linear_reg_best.fit(poly_features_3.fit_transform(days_to_maturity_list), iv_diff_all_list)
    fit_linear_best_middle = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))
    linear_reg_best.fit(poly_features_3.fit_transform(x_low), y_low)
    fit_linear_best_low = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))

    plt.plot(fit_x, fit_linear_best_up, 'r-', color='red')
    plt.plot(fit_x, fit_linear_best_middle, 'r-', color='blue')
    plt.plot(fit_x, fit_linear_best_low, 'r-', color='green')
    plt.plot(days_to_maturity_list, iv_diff_all_list, 'b.')
    plt.xlabel("np.linspace(1, 35, 1000)")
    plt.ylabel("curve fitting using Polynomial")
    plt.legend(['0.8-quantile', '0.5-quantile', '0.2-quantile'])
    plt.show()

    hypo_best = linear_reg_best.predict(poly_features_3.fit_transform(x_up))
    print(mean_squared_error(hypo_best, y_up))
    hypo_best = linear_reg_best.predict(poly_features_3.fit_transform(days_to_maturity_list))
    print(mean_squared_error(hypo_best, iv_diff_all_list))
    hypo_best = linear_reg_best.predict(poly_features_3.fit_transform(x_low))
    print(mean_squared_error(hypo_best, y_low))
    # 当多项式取到3阶时MSE=0.00012829834554331016
    # 当多项式取到4阶时MSE=0.00012742433856382287

    # 将得到的数据储存在csv文件里
    fit_x = np.array(sorted(iv_diff_all_dict.keys())).reshape(-1, 1)

    linear_reg_best.fit(poly_features_3.fit_transform(x_up), y_up)
    fit_linear_best_up = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))
    linear_reg_best.fit(poly_features_3.fit_transform(days_to_maturity_list), iv_diff_all_list)
    fit_linear_best_middle = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))
    linear_reg_best.fit(poly_features_3.fit_transform(x_low), y_low)
    fit_linear_best_low = linear_reg_best.predict(poly_features_3.fit_transform(fit_x))

    iv_diff_up_middle_low = {}
    dict_key = sorted(iv_diff_all_dict.keys())
    # 定义两个列表来储存iv_diff的均值和方差
    for i in range(len(sorted(iv_diff_all_dict.keys()))):
        iv_diff_up_middle_low[dict_key[i]] = [fit_linear_best_up[i][0], fit_linear_best_middle[i][0],
                                              fit_linear_best_low[i][0]]
    iv_diff_up_middle_low_pd = pd.DataFrame(iv_diff_up_middle_low)
    iv_diff_up_middle_low_pd.to_csv("E:\\XX\\option_arbitrage\\data\\mid\\csv\\skew_put_up_middle_low.csv")
    print(iv_diff_up_middle_low_pd)


if __name__ == "__main__":
    skew_put_regression()