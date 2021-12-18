import pandas as pd
import numpy as np
import sqlite3
import scipy.interpolate as spi
import matplotlib.pyplot as plt
from dateutil.parser import parse
from basic_function.calc_Greek import calc_call_delta, calc_gamma, calc_vega, calc_theta_call
from basic_function.calc_implied_volatility import call_implied_vol
from basic_function.get_etf_daily_data import get_daily_close
import pdb
# from model.skew.iv_diff_call import iv_diff_call
# from model.skew.skew_call import skew_call


# 连接数据库，选出所有交易日
def get_trade_date(start_date, end_date):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"SELECT DISTINCT trade_dt\nFROM OPTION_LOCAL ol\nwhere TRADE_DT>={start_date} " \
          f"and TRADE_DT <={end_date}\norder by TRADE_DT"
    c.execute(sql)
    trade_dt_total = c.fetchall()
    trade_dt_total = [i[0] for i in trade_dt_total]
    return trade_dt_total


# 根据交易日选出近月到期日
def get_latest_maturity_date(trade_date):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"select min(OPTION_ENDTRADE) \nfrom OPTION_LOCAL\nwhere TRADE_DT ={trade_date} and CALL_PUT='call'"
    c.execute(sql)
    result = c.fetchall()
    option_end_date = result[0][0]
    return option_end_date


# 选出近月期权包含的所有执行价格k
def get_k_total_latest(trade_date, option_end_date):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"SELECT k,CLOSE\nfrom OPTION_LOCAL ol\nwhere " \
          f"TRADE_DT ={trade_date} and CALL_PUT='call' and OPTION_ENDTRADE={option_end_date} " \
          f"and (CONTRACT_MULTIPLIER = 10000.0 or CONTRACT_MULTIPLIER='10000')\norder by K ASC"
    c.execute(sql)
    result = c.fetchall()
    k_total = [i[0] for i in result]
    return k_total


# 选出近月期权中不同的执行价格k对应的close
def get_close_total_latest(trade_date, option_end_date):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"SELECT k,CLOSE\nfrom OPTION_LOCAL ol\nwhere " \
          f"TRADE_DT ={trade_date} and CALL_PUT='call' and OPTION_ENDTRADE={option_end_date} " \
          f"and (CONTRACT_MULTIPLIER = 10000.0 or CONTRACT_MULTIPLIER='10000')\norder by K ASC"
    c.execute(sql)
    result = c.fetchall()
    close_total = [i[1] for i in result]
    return close_total


# 出近月期权中不同的执行价格k对应的wind_id
def get_wind_id_total_latest(trade_date, option_end_date):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"SELECT k,CLOSE,wind_id\nfrom OPTION_LOCAL ol\nwhere " \
          f"TRADE_DT ={trade_date} and CALL_PUT='call' and OPTION_ENDTRADE={option_end_date} " \
          f"and (CONTRACT_MULTIPLIER = 10000.0 or CONTRACT_MULTIPLIER='10000')\norder by K ASC"
    c.execute(sql)
    result = c.fetchall()
    wind_id_total = [i[2] for i in result]
    return wind_id_total


# 配置delta=a(a=0.25或0.5）的期权
def option_delta_allocation(delta_total, close_total, k_total, wind_id_total, iv_total, a, T, R, s0):
    if min(delta_total) < a < max(delta_total):
        delta_left = max([i for i in delta_total if i < a])
        delta_right = min([i for i in delta_total if i > a])
        close_left = close_total[delta_total.index(delta_left)]
        close_right = close_total[delta_total.index(delta_right)]
        k_left = k_total[delta_total.index(delta_left)]
        k_right = k_total[delta_total.index(delta_right)]
        p_left = (delta_right - a) / (delta_right - delta_left)
        p_right = 1 - p_left
        wind_id_left = wind_id_total[delta_total.index(delta_left)]
        wind_id_right = wind_id_total[delta_total.index(delta_right)]
        iv_left = iv_total[delta_total.index(delta_left)]
        iv_right = iv_total[delta_total.index(delta_right)]
        gamma_left = calc_gamma(s0, k_left, T, iv_left, R)
        gamma_right = calc_gamma(s0, k_right, T, iv_right, R)
        vega_left = calc_vega(s0, k_left, T, iv_left, R)
        vega_right = calc_vega(s0, k_right, T, iv_right, R)
        theta_left = calc_theta_call(s0, k_left, T, iv_left, R)
        theta_right = calc_theta_call(s0, k_right, T, iv_right, R)
        i = 1
        j = 1
    elif max(delta_total) <= a:
        delta_left = max(delta_total)
        delta_right = 0
        close_left = close_total[delta_total.index(delta_left)]
        close_right = 0
        k_left = k_total[delta_total.index(delta_left)]
        k_right = 0
        p_left = a / delta_left
        p_right = 0
        wind_id_left = wind_id_total[delta_total.index(delta_left)]
        wind_id_right = '0'
        iv_left = iv_total[delta_total.index(delta_left)]
        iv_right = 0
        gamma_left = calc_gamma(s0, k_left, T, iv_left, R)
        gamma_right = 0
        vega_left = calc_vega(s0, k_left, T, iv_left, R)
        vega_right = 0
        theta_left = calc_theta_call(s0, k_left, T, iv_left, R)
        theta_right = 0
        i = 1
        j = 0
        print('j=0')
    else:
        delta_left = 0
        delta_right = min(delta_total)
        close_left = 0
        close_right = close_total[delta_total.index(delta_right)]
        k_left = 0
        k_right = k_total[delta_total.index(delta_right)]
        p_left = 0
        p_right = a / delta_right
        wind_id_left = '0'
        wind_id_right = wind_id_total[delta_total.index(delta_right)]
        iv_left = 0
        iv_right = iv_total[delta_total.index(delta_right)]
        gamma_left = 0
        gamma_right = calc_gamma(s0, k_right, T, iv_right, R)
        vega_left = 0
        vega_right = calc_vega(s0, k_right, T, iv_right, R)
        theta_left = 0
        theta_right = calc_theta_call(s0, k_right, T, iv_right, R)
        i = 0
        j = 1
        print('i=0')
    result = pd.DataFrame({'index': ['left', 'right'], 'wind_id': [wind_id_left, wind_id_right], 'k': [k_left, k_right],
                          'p': [p_left, p_right], 'close': [close_left, close_right], 'iv': [iv_left, iv_right],
                           'delta': [delta_left, delta_right], 'gamma': [gamma_left, gamma_right],
                           'vega': [vega_left, vega_right], 'theta': [theta_left, theta_right]})
    result.set_index(['index'], inplace=True)
    return result


# 根据交易日wind_id和交易日选出close
def get_option_close(trade_date, wind_id):
    data_path = r'E:\XX\option_arbitrage\data\raw\option.db'
    my_db = sqlite3.connect(data_path)
    c = my_db.cursor()
    sql = f"SELECT K,CLOSE \nfrom OPTION_LOCAL ol\nwhere TRADE_DT = {trade_date} and CALL_PUT='call' " \
          f"and wind_id='{wind_id}'\norder by K ASC"
    c.execute(sql)
    result = c.fetchall()
    close = result[0][1]
    return close


# 期权价格会不断发生变化，所以需要更新之前做多做空的期权的信息
def option_after_date_change(option, trade_date, option_end_date, s0, T, R):
    if option.loc['left', 'k'] != 0 and option.loc['right', 'k'] != 0:
        option.loc['left', 'close'] = get_option_close(trade_date,  option.loc['left', 'wind_id'])
        option.loc['left', 'iv'] = call_implied_vol(s0, option.loc['left', 'k'], T, option.loc['left', 'close'], R)
        option.loc['left', 'delta'] = calc_call_delta(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'gamma'] = calc_gamma(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'vega'] = calc_vega(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'theta'] = calc_theta_call(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['right', 'close'] = get_option_close(trade_date,  option.loc['right', 'wind_id'])
        option.loc['right', 'iv'] = call_implied_vol(s0, option.loc['right', 'k'], T, option.loc['right', 'close'], R)
        option.loc['right', 'delta'] = calc_call_delta(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'gamma'] = calc_gamma(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'vega'] = calc_vega(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'theta'] = calc_theta_call(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
    elif option.loc['left', 'k'] == 0 and option.loc['right', 'k'] != 0:
        option.loc['right', 'close'] = get_option_close(trade_date, option.loc['right', 'wind_id'])
        option.loc['right', 'iv'] = call_implied_vol(s0, option.loc['right', 'k'], T, option.loc['right', 'close'], R)
        option.loc['right', 'delta'] = calc_call_delta(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'gamma'] = calc_gamma(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'vega'] = calc_vega(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
        option.loc['right', 'theta'] = calc_theta_call(s0, option.loc['right', 'k'], T, option.loc['right', 'iv'], R)
    elif option.loc['left', 'k'] != 0 and option.loc['right', 'k'] == 0:
        option.loc['left', 'close'] = get_option_close(trade_date, option.loc['left', 'wind_id'])
        option.loc['left', 'iv'] = call_implied_vol(s0, option.loc['left', 'k'], T, option.loc['left', 'close'], R)
        option.loc['left', 'delta'] = calc_call_delta(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'gamma'] = calc_gamma(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'vega'] = calc_vega(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
        option.loc['left', 'theta'] = calc_theta_call(s0, option.loc['left', 'k'], T, option.loc['left', 'iv'], R)
    return option


# 计算收益，并且计算来自gamma的收益，来自theta的收益和来自Vega的收益
def calc_total_greeks(open_temp, close_temp, trade_date, trade_date_open, s1, s0, balance, balance1):
    # delta = 2 * option.loc[0, 'p']*option.loc[0, 'delta'] + 2 * option.loc[1, 'p']*option.loc[1, 'delta'] \
    #         - option.loc[2, 'p']*option.loc[2, 'delta'] - option.loc[3, 'p']*option.loc[3, 'delta']
    # delta = state * delta
    delta_s0 = s0 - s1
    position = [open_temp.loc[i, 'position'] for i in range(4)]
    gamma = [open_temp.loc[i, 'gamma'] for i in range(4)]
    from_gamma = sum([0.5*gamma[i]*position[i]*delta_s0**2 for i in range(4)])
    vega = [open_temp.loc[i, 'vega'] for i in range(4)]
    iv_change = [close_temp.loc[i, 'iv'] - open_temp.loc[i, 'iv'] for i in range(4)]
    from_vega = sum([position[i] * iv_change[i] * vega[i] for i in range(4)])
    t = (parse(str(trade_date))-parse(str(trade_date_open))).days/365
    from_theta = sum([open_temp.loc[i, 'position'] * open_temp.loc[i, 'theta'] * t for i in range(4)])
    total_greeks_df = pd.DataFrame({'trade_date': [trade_date], 's0': [s0], 'delta_s': [s0-s1], 'balance': [balance],
                                    'return': [balance - balance1], 'from_gamma': [from_gamma],
                                    'from_vega': [from_vega], 'from_theta': [from_theta]})
    return total_greeks_df


def skew_arbitrage_call(start_date=20200226, end_date=20210330):
    R = 0.02
    option_string = '510050.SH'
    data_path = r"E:\XX\option_arbitrage\data\mid\csv\skew_call_up_middle_low.csv"
    up_middle_low = pd.read_csv(data_path, index_col=0)
    up_middle_low = up_middle_low.to_dict()

    # 连接数据库，选出所有交易日
    trade_dt_total = get_trade_date(start_date, end_date)

    # 获取etf每天的收盘价
    etf_daily_close_df = get_daily_close(str(start_date), str(end_date), option_string)
    etf_daily_close_df.set_index(['date'], inplace=True)

    # 读取vix指数
    data_path_2 = r"E:\XX\option_arbitrage\data\mid\csv\vix.csv"
    vix_all = pd.read_csv(data_path_2, index_col=0)

    # 定义一个字典储存到期天数及其对应的iv_diff
    iv_diff_all = {}

    # 初始余额为0
    balance = 0
    state = 0
    state_all = []
    balance_all = []
    trade_date_all = []

    iv_diff_quantile_up = []
    iv_diff_quantile_middle = []
    iv_diff_quantile_low = []
    time_stamp = []

    figure, axs = plt.subplots(3, 1)

    open_close_df = pd.DataFrame()
    open_close_total_df = pd.DataFrame()

    for trade_date in trade_dt_total:
        print(trade_date)
        # 根据交易日选出近月到期日
        option_end_date = get_latest_maturity_date(trade_date)

        # 计算T
        days = (parse(str(option_end_date)) - parse(str(trade_date))).days
        T = days / 365

        # 选出标的当天价格
        s0 = etf_daily_close_df.loc[trade_date, 'close']

        # 首先根据state决定是否需要平仓
        if state == 1 or state == -1:
            # 由于价格的变化，修改各个期权对应greeks
            option_delta_025 = option_after_date_change(option_delta_025, trade_date, option_end_date, s0, T, R)
            option_delta_05 = option_after_date_change(option_delta_05, trade_date, option_end_date, s0, T, R)
            close_025 = option_delta_025.loc['left', 'p'] * option_delta_025.loc['left', 'close'] \
                        + option_delta_025.loc['right', 'p'] * option_delta_025.loc['right', 'close']
            close_05 = option_delta_05.loc['left', 'p'] * option_delta_05.loc['left', 'close'] \
                       + option_delta_05.loc['right', 'p'] * option_delta_05.loc['right', 'close']

            close_df = pd.concat([option_delta_025, option_delta_05], ignore_index=True)
            close_df.insert(0, 'position', [state * 2 * option_delta_025.loc['left', 'p'],
                                           state * 2 * option_delta_025.loc['right', 'p'],
                                           - state * option_delta_05.loc['left', 'p'],
                                           - state * option_delta_05.loc['right', 'p']])

            balance += state * (close_05 - 2 * close_025)

            # 计算总的gamma贡献、vega贡献和theta贡献
            greeks = calc_total_greeks(open_df, close_df, trade_date, trade_date_open, s1, s0, balance, balance1)
            open_df.insert(0, 'option', ['option(delta<0.25)', 'option(delta>0.25)',
                                         'option(delta<0.5)', 'option(delta>0.5)'])
            open_df.set_index(['option'], inplace=True)
            open_df = pd.concat([open_df], keys=['open a position'])
            open_df = pd.concat([open_df], keys=[trade_date_open])
            open_close_df = open_close_df.append(open_df)

            close_df.insert(0, 'option',
                            ['option(delta<0.25)', 'option(delta>0.25)', 'option(delta<0.5)', 'option(delta>0.5)'])
            close_df.set_index(['option'], inplace=True)
            close_df = pd.concat([close_df], keys=['close a position'])
            close_df = pd.concat([close_df], keys=[trade_date])
            open_close_df = open_close_df.append(close_df)

            # close_total_df = calc_total_greeks(close_df, option_end_date, s0, close_025, close_05, balance, state)
            # close_total_df = pd.concat([close_total_df], keys=[0])
            # close_total_df = pd.concat([close_total_df], keys=[trade_date])
            open_close_total_df = open_close_total_df.append(greeks)

        balance_all.append(balance)
        trade_date_all.append(parse(str(trade_date)))
        balance1 = balance

        # 如果距离到期日仅剩不到五天的时间，或者自己输入日期区间的最后一个到期日，那么选择不开仓
        if days <= 4 or trade_date == trade_dt_total[-1]:
            state = 0
            state_all.append(state)
            continue

        # 如果出现比较长的节假日则不开仓
        trade_date_next_day = trade_dt_total[trade_dt_total.index(trade_date) + 1]
        days_2 = (parse(str(trade_date_next_day)) - parse(str(trade_date))).days
        if days_2 > 5:
            state = 0
            state_all.append(state)
            continue

        # 根据交易日和近月到期日选出K和close以及对应的wind_id
        k_total = get_k_total_latest(trade_date, option_end_date)
        close_total = get_close_total_latest(trade_date, option_end_date)
        wind_id_total = get_wind_id_total_latest(trade_date, option_end_date)
        n = len(close_total)

        # 计算各个k值对应的隐含波动率和delta，按照delta大小进行排序，最后根据插值法算出iv_diff
        iv_total = [call_implied_vol(s0, k_total[i], T, close_total[i], R) for i in range(n)]
        delta_total = [calc_call_delta(s0, k_total[i], T, iv_total[i], R) for i in range(n)]
        paired_sorted = sorted(zip(delta_total, iv_total, k_total, close_total, wind_id_total), key=lambda x: x[0])
        delta_total, iv_total, k_total, close_total, wind_id_total = zip(*paired_sorted)
        iv_diff = np.interp(0.25, delta_total, iv_total) - np.interp(0.5, delta_total, iv_total)

        # 配置 delta = 0.5和0.25的期权
        option_delta_05 = option_delta_allocation(delta_total, close_total,
                                                  k_total, wind_id_total, iv_total, 0.5, T, R, s0)
        option_delta_025 = option_delta_allocation(delta_total, close_total,
                                                   k_total, wind_id_total, iv_total, 0.25, T, R, s0)
        close_025 = option_delta_025.loc['left', 'p'] * option_delta_025.loc['left', 'close'] \
                    + option_delta_025.loc['right', 'p'] * option_delta_025.loc['right', 'close']
        close_05 = option_delta_05.loc['left', 'p'] * option_delta_05.loc['left', 'close'] \
                   + option_delta_05.loc['right', 'p'] * option_delta_05.loc['right', 'close']

        # 计算gamma的值
        gamma_025 = option_delta_025.loc['left', 'p'] * option_delta_025.loc['left', 'gamma'] \
                    + option_delta_025.loc['right', 'p'] * option_delta_025.loc['right', 'gamma']
        gamma_05 = option_delta_05.loc['left', 'p'] * option_delta_05.loc['left', 'gamma'] \
                    + option_delta_05.loc['right', 'p'] * option_delta_05.loc['right', 'gamma']

        # 提取vix的值
        ind = vix_all.index.get_loc(trade_date)
        vix_1 = vix_all.loc[trade_date, 'sigma1']
        vix_0 = vix_all.iloc[ind-1, 0]
        vix_diff = vix_1 - vix_0

        # 根据iv_diff的大小决定是否开仓
        condition_1 = (state == 1 and iv_diff > up_middle_low[str(days)][1]+0.0001)
        condition_2 = (state == 1 and iv_diff < up_middle_low[str(days)][2]-0.0001)
        condition_3 = (state == -1 and iv_diff < up_middle_low[str(days)][1]-0.0001)
        condition_4 = (state == -1 and iv_diff > up_middle_low[str(days)][0]+0.0001)
        condition_5 = (state == 0 and iv_diff > up_middle_low[str(days)][0]+0.0001)
        condition_6 = (state == 0 and iv_diff < up_middle_low[str(days)][2]-0.0001)

        if condition_1 or condition_4 or condition_5:  # 买入0.5，卖出0.25
            print('开仓1')
            if gamma_05 - 2 * gamma_025 < 0 and vix_diff/vix_0 > 0.1 and vix_1 < 0.3:
                print('有异常1')
                state = 0
                axs[0].scatter(parse(str(trade_date)), iv_diff, c='blue')
                continue
            else:
                balance += 2*close_025 - close_05
                state = 1
                axs[0].scatter(parse(str(trade_date)), iv_diff, c='red')
        elif condition_2 or condition_3 or condition_6:
            print('开仓2')
            if 2 * gamma_025 - gamma_05 < 0 and vix_diff/vix_1 > 0.1 and vix_1 < 0.3:
                print('有异常2')
                state = 0
                axs[0].scatter(parse(str(trade_date)), iv_diff, c='blue')
                continue
            else:
                balance += close_05 - 2*close_025
                state = -1
                axs[0].scatter(parse(str(trade_date)), iv_diff, c='green')
        else:
            state = 0
            axs[0].scatter(parse(str(trade_date)), iv_diff, c='blue')

        state_all.append(state)
        iv_diff_quantile_up.append(up_middle_low[str(days)][0])
        iv_diff_quantile_middle.append(up_middle_low[str(days)][1])
        iv_diff_quantile_low.append(up_middle_low[str(days)][2])
        time_stamp.append(parse(str(trade_date)))

        # 将当天的s0储存到s1
        s1 = s0
        trade_date_open = trade_date

        # 储存开仓包含的细节数据
        if state == 1 or state == -1:
            open_df = pd.concat([option_delta_025, option_delta_05], ignore_index=True)
            open_df.insert(0, 'position', [-state*2*option_delta_025.loc['left', 'p'],
                                           -state*2*option_delta_025.loc['right', 'p'],
                                           state*option_delta_05.loc['left', 'p'],
                                           state*option_delta_05.loc['right', 'p']])

            # open_total_df = calc_total_greeks(open_df, option_end_date, s0, close_025, close_05, balance, state)
            # open_total_df = pd.concat([open_total_df], keys=[state])
            # open_total_df = pd.concat([open_total_df], keys=[trade_date])
            # open_close_total_df = open_close_total_df.append(open_total_df)

    axs[0].plot(time_stamp, iv_diff_quantile_up, linewidth=0.5)
    axs[0].plot(time_stamp, iv_diff_quantile_middle, linewidth=0.5)
    axs[0].plot(time_stamp, iv_diff_quantile_low, linewidth=0.5)
    axs[0].set_xlabel('date')
    axs[0].set_ylabel('iv_diff')
    axs[0].set_xlim(min(trade_date_all), max(trade_date_all))

    axs[1].plot(trade_date_all,  etf_daily_close_df['close'], linewidth=2, color='black')
    axs[1].set_ylabel('s0')
    axs[1].set_xlabel('date')
    axs[1].set_xlim(min(trade_date_all), max(trade_date_all))

    # plt.scatter(trade_date_all, state_all)
    # plt.show()
    axs[2].plot(trade_date_all, balance_all, linewidth=1)
    axs[2].set_xlabel('date')
    axs[2].set_ylabel('balance')
    axs[2].set_xlim(min(trade_date_all), max(trade_date_all))
    plt.tight_layout()
    plt.show()

    pdb.set_trace()
    open_close_df.to_csv(r'E:\XX\option_arbitrage\result\data\open_close_detail(call).csv')
    open_close_total_df.set_index(['trade_date'], inplace=True)
    open_close_total_df.to_csv(r'E:\XX\option_arbitrage\result\data\open_close_total(call).csv')

    return trade_date_all, balance_all

    # all_information = pd.DataFrame({'trade_date': date_all, 'end_date': end_date_all, 'position': position_all,
    #                                 's0': s0_all, 'close_025': close_025_all, 'close_05': close_05_all,
    #                                 'balance': balance_after_trade,
    #                                 'k1': k_1_all, 'k2': k_2_all, 'k3': k_3_all, 'k4': k_4_all,
    #                                 'delta1': delta_1_all, 'delta2': delta_2_all, 'delta3': delta_3_all,
    #                                 'delta4': delta_4_all, 'close1': close_1_all, 'close2': close_2_all,
    #                                 'close3': close_3_all, 'close4': close_4_all, 'p1': p_1_all, 'p2': p_2_all,
    #                                 'p3': p_3_all, 'p4': p_4_all})
    # all_information.set_index(['trade_date', 'position'], inplace=True)
    # all_information.to_csv('E:\\XX\\option_arbitrage\\data\\mid\\csv\\test_0426.csv')


if __name__ == '__main__':
    # 采用偏度策略进行交易
    x1, y1 = skew_arbitrage_call(20200701, 20200901)