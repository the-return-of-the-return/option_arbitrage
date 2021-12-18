import pandas as pd
import numpy as np


if __name__ == '__main__':
    # 导入数据
    result = pd.read_csv("E:/XX/option_arbitrage/result/data/open_close_total(call).csv", index_col=0)
    balance = result['balance'].tolist()
    balance = [i+2.814 for i in balance]
    n = len(balance)
    count = 0

    # 计算日胜率
    delta_balance = [balance[0]-2.814]
    for i in range(1, n):
        delta_balance.append(balance[i]-balance[i-1])
    for i in delta_balance:
        if i > 0:
            count += 1
    daily_success_rate = count/n

    # 计算盈亏比
    sum_positive = 0
    sum_negative = 0
    for i in delta_balance:
        if i > 0:
            sum_positive += i
        else:
            sum_negative += i
    profit_loss_ratio = -sum_positive/sum_negative

    # 计算收益率
    return_rate = [balance[0]/2.814-1]
    for i in range(1, n):
        return_rate.append(balance[i]/balance[i-1]-1)

    # 计算最大回撤率
    hwm = [2.814]
    drawdown = []
    for i in range(1, n):
        cur_hwm = max(hwm[i-1], balance[i])
        hwm.append(cur_hwm)
        drawdown.append((hwm[i]-balance[i])/hwm[i])
    maximum_drawdown = np.max(drawdown)

    # 计算年化收益率，收益率波动率和夏普比率
    return_rate_std = np.std(return_rate)
    sharpe_ratio = 252*np.mean(return_rate)/return_rate_std/np.sqrt(252)

    x = {'日胜率':daily_success_rate, '盈亏比': profit_loss_ratio, '最大回撤': maximum_drawdown,
         '年化收益率': 252*np.mean(return_rate), '收益率波动率': return_rate_std*np.sqrt(252), '夏普比率': sharpe_ratio}
    print(x)