#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/6/10 14:10
# @Author : xiaochen
# @File   : calc_Greek.py

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def calc_call_delta(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    delta = stats.norm.cdf(d1)
    return delta


def calc_put_delta(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    delta = stats.norm.cdf(d1) - 1
    return delta


def calc_gamma(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    gamma = stats.norm.pdf(d1)/(S0*implied_vol*np.sqrt(T))
    return gamma


def calc_theta_call(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    d2 = (np.log(S0 / K) + (r - np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    theta = -S0*stats.norm.pdf(d1)*implied_vol/(2*np.sqrt(T))-r*K*np.exp(-r*T)*stats.norm.cdf(d2)
    return theta


def calc_theta_put(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    d2 = (np.log(S0 / K) + (r - np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    theta = -S0*stats.norm.pdf(d1)*implied_vol/(2*np.sqrt(T))+r*K*np.exp(-r*T)*stats.norm.cdf(-d2)
    return theta


def calc_vega(S0, K, T, implied_vol, r=0):
    d1 = (np.log(S0 / K) + (r + np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    vega = S0*np.sqrt(T)*stats.norm.pdf(d1)
    return vega


def calc_rho_call(S0, K, T, implied_vol, r=0):
    d2 = (np.log(S0 / K) + (r - np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    rho = K*T*np.exp(-r*T)*stats.norm.cdf(d2)
    return rho


def calc_rho_put(S0, K, T, implied_vol, r=0):
    d2 = (np.log(S0 / K) + (r - np.square(implied_vol) / 2) * T) / (implied_vol * np.sqrt(T))
    rho = -K*T*np.exp(-r*T)*stats.norm.cdf(-d2)
    return rho

if __name__ == '__main__':
    vol = np.linspace(0.01, 0.5)
    theta1 = [-calc_theta_put(1, 1, 1 / 12, x) for x in vol]
    theta2 = [-calc_theta_put(1, 1.2, 1 / 12, x) for x in vol]
    theta3 = [-calc_theta_put(1, 0.8, 1 / 12, x) for x in vol]
    theta1 = np.array(theta1)
    theta2 = np.array(theta2)
    theta3 = np.array(theta3)
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True, axis='y')
    x = np.arange(len(vol))  # the label locations
    x_tick = np.arange(0, len(vol), 10)
    ax.plot(theta1, color='r')
    ax.plot(theta2, color='b')
    ax.plot(theta3, color='g')

    K = np.linspace(0.76, 1.25)
    theta1 = [-calc_theta_put(1, 1, 1 / 12, x) for x in vol]
    theta2 = [-calc_theta_put(1, 1.2, 1 / 12, x) for x in vol]
    theta3 = [-calc_theta_put(1, 0.8, 1 / 12, x) for x in vol]


    vol = np.linspace(0.01, 0.5)
    theta1 = [-calc_theta_put(1, 1, 1 / 12, x) for x in vol]
    theta2 = [-calc_theta_put(1, 1.2, 1 / 12, x) for x in vol]
    theta3 = [-calc_theta_put(1, 0.8, 1 / 12, x) for x in vol]
    theta1 = np.array(theta1)
    theta2 = np.array(theta2)
    theta3 = np.array(theta3)
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True, axis='y')
    x = np.arange(len(vol))  # the label locations
    x_tick = np.arange(0, len(vol), 10)
    ax.plot(theta1, color='r')
    ax.plot(theta2, color='b')
    ax.plot(theta3, color='g')

    K = np.linspace(0.76, 1.25)
    vega1 = [calc_vega(1, x, 1 / 12, 0.2) for x in K]
    vega2 = [calc_vega(1, x, 1 / 12, 0.2) for x in K]
    vega3 = [calc_vega(1, x, 1 / 12, 0.2) for x in K]

    date = np.linspace(1/365, 50/365)
    gamma = [calc_gamma(1, 1, x, 0.2, r=0) for x in date]
    gamma = np.array(gamma)
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True, axis='y')
    x = np.arange(len(date))  # the label locations
    x_tick = np.arange(0, len(date), 10)
    ax.plot(gamma, color='r')

