#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date          : 2020-09-19 19:50:03
# @Author        : Yongwei Nong
# @version       : 1.0.0v
# @Description   : 将MACD,KDJ,RSI,WILLR,BBI,MTM,BIAS等7种指标的数据结果进行分析
#                  每个指标的分析结果返回1，2，3三个数字,分别表示卖出,买进,观望三个决策建议
#                  把超过三个指标的分析决策建议相同的股票推荐出来,做为股票交易依据

from tradeindex import  *

#MACD指标分析
def analysis_macd(df_data):
    df_data['MACD_金叉死叉'] = ''
    macd_position = df_data["macd_diff"] > df_data["macd_dea"]
    df_data.loc[macd_position[(macd_position == True) & (macd_position.shift() == False)].index, 'MACD_金叉死叉'] = '金叉'
    df_data.loc[macd_position[(macd_position == False) & (macd_position.shift() == True)].index, 'MACD_金叉死叉'] = '死叉'
    rise_fall_diff = Rise_fall(df_data["macd_diff"].tolist())
    rise_fall_dea = Rise_fall(df_data["macd_dea"].tolist())
    rise_fall_macd = Rise_fall(df_data["macd"].tolist())
    if df_data["macd_diff"].iloc[0] > 0 and df_data["macd_dea"].iloc[0] > 0 and rise_fall_diff and  rise_fall_dea:
        data = {
           "code": 2,
           "policy": "当DIF和dea均大于0并向上移动时，一般表示为股市处于多头行情中，可以买入或持股"
        }
    elif df_data["macd_diff"].iloc[0] > 0 and df_data["macd_dea"].iloc[0] > 0 and not rise_fall_diff and not rise_fall_dea:
        data = {
           "code": 1,
           "policy": "当DIF和dea均大于0但都向下移动时，一般表示为股票行情处于多头市场的短期回调阶段,可以先卖出股票观望"
        }
    elif df_data["macd_diff"].iloc[0] < 0 and df_data["macd_dea"].iloc[0] < 0 and not rise_fall_diff and not rise_fall_dea:
        data = {
           "code": 1,
           "policy": "当DIF和dea均小于0并向下移动时，一般表示为股市处于空头行情中，可以卖出股票或观望"
        }
    elif df_data["macd_diff"].iloc[0] < 0 and df_data["macd_dea"].iloc[0] < 0 and rise_fall_diff and  rise_fall_dea:
        data = {
           "code": 2,
           "policy": "当DIF和dea均小于0时但向上移动时，一般表示为空头市场的反弹阶段，股票将上涨，在总体看空的情况下，可以少量买进股票"
        }
    elif macd_position.iloc[0]  and rise_fall_diff and not macd_position.iloc[1]: # 金叉
        data = {
           "code": 2,
           "policy": "macd金叉"
        }
    elif macd_position.iloc[1] and not macd_position.iloc[0] and not rise_fall_diff: #死叉
        data = {
           "code": 1,
           "policy": "macd死叉"
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 

#KDJ指标分析
def analysis_kdj(df_data):
    df_data['KDJ_金叉死叉'] = ''
    kdj_position = df_data['kdj_k'] > df_data['kdj_d']
    df_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    df_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
    rise_fall_k = Rise_fall(df_data["kdj_k"].tolist())
    buy = 0
    sell = 0
    for n in df_data['kdj_k'].tolist()[0:21]:
        if n < 10:          #超卖区 
            buy = 1 + buy
        elif n > 90:        #超买区 
            sell = 1 + sell
    for n in df_data['kdj_d'].tolist()[0:21]:
        if n < 20:          #超卖区
            buy = 1 + buy
        elif n > 80:        #超买区 
            sell = 1 + sell
    if buy > 20:
        data = {
           "code": 2,
           "policy": "kdj超卖区"
        }
    elif sell > 20:
        data = {
           "code": 1,
           "policy": "kdj超买区"
        }
    elif kdj_position.iloc[1] and not kdj_position.iloc[0] and not rise_fall_k: #死叉 
        data = {
           "code": 1,
           "policy": "kdj死叉"
        }
        policy = 1 
    elif kdj_position.iloc[0] and not kdj_position.iloc[1] and rise_fall_k:  #金叉
        data = {
           "code": 2,
           "policy": "kdj金叉"
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 
    

#RSI指标分析
def analysis_rsi(df_data):
    df_data['rsi_buy_sell_6'] = ''
    rsi_buy_position_6 = df_data['rsi_6'] > 70
    rsi_sell_position_6 = df_data['rsi_6'] < 30
    df_data.loc[rsi_buy_position_6[(rsi_buy_position_6 == True) & (rsi_buy_position_6.shift() == False)].index, 'rsi_buy_sell_6'] = '超买'
    df_data.loc[rsi_sell_position_6[(rsi_sell_position_6 == True) &(rsi_sell_position_6.shift() == False)].index, 'rsi_buy_sell_6'] = '超卖'

    df_data['rsi_金叉死叉'] = ''
    rsi_position = df_data["rsi_12"] > df_data["rsi_6"]
    df_data.loc[rsi_position[(rsi_position == True) & (rsi_position.shift() == False)].index, 'rsi_金叉死叉'] = '金叉'
    df_data.loc[rsi_position[(rsi_position == False) &(rsi_position.shift() == True)].index, 'rsi_金叉死叉'] = '死叉'
    rise_fall_rsi_6 = Rise_fall(df_data["rsi_6"].tolist())
    rise_fall_rsi_12 = Rise_fall(df_data["rsi_12"].tolist())
    rise_fall_close = Rise_fall(df_data["close"].tolist())
    buy = 0
    sell = 0
    for data in [df_data['rsi_6'].tolist()[0:21],df_data['rsi_12'].tolist()[0:21],df_data['rsi_24'].tolist()[0:21]]:
        for d in data:
            if d < 30:          #超卖区 
                buy = 1 + buy
            elif d > 70:        #超买区 
                sell = 1 + sell
    if buy > 30:
        data = {
           "code": 2,
           "policy": "rsi超卖区"
        }
    elif sell > 30:
        data = {
           "code": 1,
           "policy": "rsi超买区"
        }
    elif (rise_fall_rsi_6 or rise_fall_rsi_12) and not rise_fall_close:
        data = {
           "code": 2,
           "policy": "股价走低，RSI走高,考虑买进"
        }
    elif (not rise_fall_rsi_6 or not rise_fall_rsi_12) and rise_fall_close:
        data = {
           "code": 1,
           "policy": "股价走高，RSI走底, 考虑卖出"
        }
    elif rsi_buy_position_6.iloc[0] and not rsi_buy_position_6.iloc[1] and rise_fall_rsi_6:  #金叉
        data = {
           "code": 2,
           "policy": "rsi金叉"
        }
    elif not rsi_position.iloc[0] and rsi_position.iloc[1] and not rise_fall_rsi_6:   #死叉
        data = {
           "code": 1,
           "policy": "rsi死叉"
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 
   
#WILLR指标分析
def analysis_willr(df_data):
    willr_buy_position_14 = df_data['willr_14'] > 85
    willr_sell_position_14 = df_data['willr_14'] < 15
    df_data.loc[willr_buy_position_14[(willr_buy_position_14 == True) & (willr_buy_position_14.shift() == True)].index, 'willr_buy_sell_14'] = '超卖'
    df_data.loc[willr_sell_position_14[(willr_sell_position_14 == True) & (willr_sell_position_14.shift() == True)].index, 'willr_buy_sell_14'] = '超买'
    buy = 0
    sell = 0
    for data in [df_data['willr_14'].tolist()[0:21],df_data['willr_34'].tolist()[0:21]]:
        for d in data:
            if d < 15:          #超卖区 
                buy = 1 + buy
            elif d > 85:        #超买区 
                sell = 1 + sell
    rise_fall_close = Rise_fall(df_data["close"].tolist())
    rise_fall_willr = Rise_fall(df_data["willr_14"].tolist())
    if sell > 20: 
        data = {
           "code": 1,
           "policy": "W&R连续几次撞顶，局部形成双重或多重顶，是卖出的信号"
        }
    elif buy > 20:
        data = {
           "code": 2,
           "policy": "W&R连续几次撞底，局部形成双重或多重底，是买进的信号"
        }
    elif rise_fall_close and willr_buy_position_14.iloc[0]:
        data = {
           "code": 1,
           "policy": "在W&R进入高位后，一般要回头，如果股价继续上升就产生了背离，是卖出信号"
        }
    elif not rise_fall_willr and not rise_fall_close:
        data = {
           "code": 2,
           "policy": "在W&R进入低位后，一般要反弹，如果股价继续下降就产生了背离"
        }
    elif willr_buy_position_14.iloc[0] and willr_buy_position_14.iloc[1] and rise_fall_willr:
        data = {
           "code": 2,
           "policy": "willr金叉"
        }
    elif willr_sell_position_14.iloc[0] and willr_sell_position_14.iloc[1] and not rise_fall_willr:
        data = {
           "code": 1,
           "policy": "willr死叉"
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 

#BBI指标分析
def analysis_bbi(df_data):
    df_data['bbi_buy_sell'] = ''
    df_data['bbi_trade_info'] = ''
    bbi_position = df_data['close'] > df_data["bbi"]
    df_data.loc[bbi_position[(bbi_position == False) & (bbi_position.shift() == False)].index, 'bbi_buy_sell'] = '超买'
    df_data.loc[bbi_position[(bbi_position == True) & (bbi_position.shift() == True)].index, 'bbi_buy_sell'] = '超卖'
    df_data.loc[bbi_position[(bbi_position == False) & (bbi_position.shift() == True)].index, 'bbi_trade_info'] = '卖出信号'
    df_data.loc[bbi_position[(bbi_position == True) & (bbi_position.shift() == False)].index, 'bbi_trade_info'] = '买入信号'
    rise_fall_bbi = Rise_fall(df_data["bbi"].tolist())
    if bbi_position.iloc[0] and bbi_position.iloc[1] and rise_fall_bbi:
        data = {
           "code": 2,
           "policy": "bbi超卖"
        }
    elif not bbi_position.iloc[0] and not bbi_position.iloc[1] and not rise_fall_bbi:
        data = {
           "code": 1,
           "policy": "bbi超买"
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 
   
#MTM指标分析
def analysis_mtm(df_data):
    df_data['mtm_trade_info'] = ''
    mtm_position = df_data['mtm'] > df_data["mtmma"]
    stock_position = df_data['close'] > df_data["close"].shift(1)
    mtm_goup = df_data['mtm'] > df_data["mtm"].shift(1)
    df_data.loc[mtm_position[(mtm_position == True) & (mtm_position.shift() == False)].index, 'mtm_trade_info'] = '买入信号'
    df_data.loc[mtm_position[(mtm_position == False) & (mtm_position.shift() == True)].index, 'mtm_trade_info'] = '卖出信号'
    df_data.loc[stock_position[(stock_position == True) & (mtm_goup.shift() == False)].index, 'mtm_trade_info'] = '卖出信号'
    df_data.loc[stock_position[(stock_position == False) & (mtm_goup.shift() == True)].index, 'mtm_trade_info'] = '买入信号'

    rise_fall_mtm = Rise_fall(df_data["mtm"].tolist())
    rise_fall_close = Rise_fall(df_data["close"].tolist())
    if mtm_position.iloc[0] and not mtm_position.iloc[1] and rise_fall_mtm:
        data = {
           "code": 2,
           "policy": "一般情况下，MTM由上向下跌破中心线时为卖出时机，相反，MTM由下向上突破中心线时为买进时机"
        }
    elif not mtm_position.iloc[0] and  mtm_position.iloc[1] and not rise_fall_mtm:
        data = {
           "code": 1,
           "policy": "一般情况下，MTM由上向下跌破中心线时为卖出时机，相反，MTM由下向上突破中心线时为买进时机"
        }
    elif rise_fall_close and not rise_fall_mtm:
        data = {
           "code": 1,
           "policy": "股价在上涨行情中创新高点，而MTM未能配合上升，出现背驰现象，意味上涨动力减弱，此时应关注行情，慎防股价反转下跌."
        }
    elif not rise_fall_close and rise_fall_mtm:
        data = {
           "code": 2,
           "policy": "股价在下跌行情中走出新低点，而MTM未能配合下降，出现背驰，该情况意味下跌动力减弱，此时应注意逢低承接"
        }
    elif (rise_fall_close and rise_fall_mtm) or (not rise_fall_close and not rise_fall_mtm):
        data = {
           "code": 1,
           "policy": "若股价与MTM在低位同步上升，显示短期将有反弹行情；若股价与MTM在高位同步下降，则显示短期可能出现股价回落."
        }
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 
     
   
#BIAS指标分析
def analysis_bias(df_data):
    buy = 0
    sell = 0
    for n in df_data['bias_6'].tolist()[0:21]:
        if n > 4.5: 
            buy = 1 + buy
        elif n < -4:
            sell = 1 + sell
    for n in df_data['bias_12'].tolist()[0:21]:
        if n > 6: 
            buy = 1 + buy
        elif n < -5.5:
            sell = 1 + sell
    for n in df_data['bias_24'].tolist()[0:21]:
        if n > 9: 
            buy = 1 + buy
        elif n < -8:
            sell = 1 + sell
    if buy > 30:    #满足30个买进条件
        df_data.loc['bias_trade_info'] = '买入信号'
        data = {
           "code": 2,
           "policy": "bias买入信号"
        }
    elif sell > 30:
        data = {
           "code": 1,
           "policy": "bias卖出信号"
        }
        df_data.loc['bias_trade_info'] = '卖出信号'
    else:
        data = {
           "code": 3,
           "policy": ""
        }
    return data 

#判断一组数据上涨还是下跌
def Rise_fall(array):
    rise = 0 
    fall = 0
    for i in range(2,9):
        avg = np.mean(array[0:i])  
        if array[0] > avg:
            rise = 1 + rise
        else:
            fall = 1 + fall
    if rise > 4 and array[0] > array[1]: 
        return True 
    else:
        return False 
