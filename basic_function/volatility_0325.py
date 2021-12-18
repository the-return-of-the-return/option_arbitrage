#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import math

def g_black_scholes(S_0, K, T, r, P, v):
    d1 = (math.log(S_0/ K) + ((v ** 2) / 2) * self.T) / (v * math.sqrt(self.T))
    d2 = d1 - v * math.sqrt(T)
    if self.CallPutFlag == 'c':
        g_black_scholes = S_0 * math.exp((self.b - self.r) * self.T) * st.norm.cdf(d1) - self.X * math.exp(
            -self.r * self.T) * st.norm.cdf(d2)
    elif self.CallPutFlag == 'p':
        g_black_scholes = self.X * math.exp(-self.r * self.T) * st.norm.cdf(-d2) - S_0 * math.exp(
            (self.b - self.r) * self.T) * st.norm.cdf(-d1)
    return g_black_scholes


def vega(self,v):
    d1 = (math.log(self.S / self.X) + (self.b + (v ** 2) / 2) *self.T)/ (v * math.sqrt(self.T))
    vega = self.S * math.exp((self.b - self.r) * self.T) * st.norm.pdf(d1)*math.sqrt(self.T)
    return vega


def g_implied_volatility_nr(S_0, K, T, r, P, epsilon):
    vi = math.sqrt(abs(math.log(S_0 / K) + r * T) * 2 / T)
    ci = g_black_scholes(vi)
    vega_i = vega(vi)
    mindiff = abs(P - ci)
    while abs(P- ci) >= epsilon and abs(P - ci) <= mindiff:
        vi = vi - (ci - P) / vega_i
        ci = g_black_scholes(vi)
        vega_i = vega(vi)
        mindiff = abs(P - ci)
    if abs(P - ci) < epsilon:
        g_implied_volatility_nr = vi
    else:
        g_implied_volatility_nr = 'NA'
    return g_implied_volatility_nr

g_implied_volatility_nr(S0=2.736, K=2.700, T=12/252, r=0.0535, P=0.0368)