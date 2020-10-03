#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date           : 2020-09-19 19:50:03
# @Author         : Yongwei Nong
# @version        : 1.0.0v
# @Description    : 计算MACD,KDJ,RSI,WILLR,BBI,MTM,BIAS等7种股票交易指标 

import pandas as pd
import numpy as np
import talib as ta
import tushare as ts

#通过tushare获取股票交易数据
def get_stock_data(ts_code,start_date,end_date):
    '''
      tc_code,start_date,end_date分别为股票交易代码,数据起始和结束时间
    '''
    ts.set_token('************************************')
    pro = ts.pro_api()
    df = pro.daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    return df
    

#MACD指标计算函数
def get_macd(df):
    '''
    MACD 异同移动平均线
    算法:
    运用快速(12天)和慢速(26天)移动平均线及其聚合与分离的征兆,加以双重平滑运算
    用法:
         1.DIF、DEA均为正，DIF向上突破DEA，买入信号参考。
         2.DIF、DEA均为负，DIF向下跌破DEA，卖出信号参考。
         3.DIF线与K线发生背离，行情可能出现反转信号。
         4.DIF、DEA的值从正数变成负数，或者从负数变成正数并不是交易信号，因为它们落后于市场.
     
    df是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数,默认为12,26,9
    返回值是包含原始数据和macd_diff,macd_dea,macd三个列的dataframe
    '''
    short_ = 12
    long_ = 26
    m = 9
    df['macd_diff']=(df['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                    df['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()).shift(-1)
    df['macd_dea']=(df['macd_diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()).shift(-1)
    df['macd']=(2*(df['macd_diff']-df['macd_dea'])).shift(-1)
    return df 

#KDJ指标计算函数
def get_kdj(df):
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value = df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100   #RSV值
    df['kdj_k'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['kdj_d'] = df['kdj_k'].ewm(com=2).mean()
    df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
    df['kdj_k'] = round(df['kdj_k'], 2)
    df['kdj_d'] = round(df['kdj_d'], 2)
    df['kdj_j'] = round(df['kdj_j'], 2)
    return df

#RSI指标计算函数
def get_rsi(df):
    '''
    调用talib库计算rsi指标
    '''
    df["rsi_6"] = (ta.RSI(df['close'], timeperiod=6)).shift(-6)
    df["rsi_12"] = (ta.RSI(df['close'], timeperiod=12)).shift(-12)
    df["rsi_24"] = (ta.RSI(df['close'], timeperiod=24)).shift(-24)
    return df

#bias指标计算函数
def get_bias(df):
    '''
    N期BIAS=(当日收盘价-N期平均收盘价)/N期平均收盘价*100%
    '''
    df['bias_6'] = (df['close'] - df['close'].rolling(6, min_periods=1).mean())/ df['close'].rolling(6, min_periods=1).mean()*100
    df['bias_12'] = (df['close'] - df['close'].rolling(12, min_periods=1).mean())/ df['close'].rolling(12, min_periods=1).mean()*100
    df['bias_24'] = (df['close'] - df['close'].rolling(24, min_periods=1).mean())/ df['close'].rolling(24, min_periods=1).mean()*100
    df['bias_6'] = (round(df['bias_6'], 2)).shift(-1)
    df['bias_12'] = (round(df['bias_12'], 2)).shift(-1)
    df['bias_24'] = (round(df['bias_24'], 2)).shift(-1)
    return df

#威廉指标
def get_willr(df):
    '''
    使用talib库的WILLR方法
    '''
    df['willr_14'] = (ta.WILLR(df['high'], df['low'], df['close'], timeperiod=14)).shift(-13)
    df['willr_34'] = (ta.WILLR(df['high'], df['low'], df['close'], timeperiod=34)).shift(-33)
    return df

#MTM指标计算函数
def get_mtm(df):
    '''
    MTM动力指标
    算法：
    MTM线　　当日收盘价与N日前的收盘价的差
    MTMMA线　对上面的差值求N日移动平均
    参数：N 间隔天数，也是求移动平均的天数，默认为6
    用法：
    1.MTM从下向上突破MTMMA，买入信号
    2.MTM从上向下跌破MTMMA，卖出信号
    3.股价续创新高，而MTM未配合上升，意味上涨动力减弱
    4.股价续创新低，而MTM未配合下降，意味下跌动力减弱
    5.股价与MTM在低位同步上升，将有反弹行情；反之，从高位同步下降，将有回落走势。
    '''
    M = N = 6
    df['mtm']=(df['close']-df['close'].shift(M)).shift(-M)
    df['mtmma']=(df['mtm'].rolling(N).mean()).shift(-(N+M-1))
    return df

#BBI指标计算函数
def get_bbi(df):
    '''
    BBI多空指标
    算法: BBI=(3日均价+6日均价+12日均价+24日均价)÷4 
    '''
    bbi_3 = df['close'].rolling(3, min_periods=3).mean().shift(-2)
    bbi_6 = df['close'].rolling(6, min_periods=6).mean().shift(-5)
    bbi_12 = df['close'].rolling(12, min_periods=12).mean().shift(-11)
    bbi_24 = df['close'].rolling(24, min_periods=24).mean().shift(-23)
    rsv = (bbi_3 + bbi_6 + bbi_12 + bbi_24 ) / 4
    df['bbi'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['bbi'] = round(df['bbi'], 2)
    return df
 
