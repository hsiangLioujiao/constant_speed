# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:11:35 2024

@author: g_s_s
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression

plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False


# 使用streamlit輸入
requ_input = st.slider("輸入 管理標準相較於調查水準 的加嚴比率", 0.0, 1.2, 0.1)
rate_input = st.slider("輸入 管理標準中 定速85km/h能效所占比率", 0.0, 1.0, 1.0)
# print(f"管理標準相較於調查水準 的加嚴比率為{requ_input:.1f}")
# print(f"管理標準中 定速85km/h能效所占比率為{rate_input:.1f}")
# print()


# 計算管理標準中 兩車速能效組合占比的函式
def requ(x65, x85, r=rate_input):
    return x65*(1-r)+x85*r
#(僅就5個車重測試數據試算，待更新)
y = list(map(requ, [7.65, 7.14, 5.7, 5.44, 5.02], [5.33, 5.11, 4.27, 4.51, 3.93], [rate_input for _ in range(5)]))
# st.write("定速65km/L之能效為[7.65, 7.14, 5.7, 5.44, 5.02]")
# st.write(f"兩車速能效組合為{y}，平均為{np.mean(y):.2f}")
# st.write("定速85km/L之能效為[5.33, 5.11, 4.27, 4.51, 3.93]")
# print("定速65km/L之能效為[7.65, 7.14, 5.7, 5.44, 5.02]")
# print(f"兩車速能效組合為{y}")
# print("定速85km/L之能效為[5.33, 5.11, 4.27, 4.51, 3.93]")
# print()


# ARTC實測數據及整理
df_ARTC = pd.DataFrame({"核定總重[噸]":[9.5, 9.5, 11, 11, 13.5, 13.5, 18.5, 18.5, 26, 26],
                   "車速[公里/小時]":[65, 85, 65, 85, 65, 85, 65, 85, 65, 85],
                   "能效[公里/公升]":[7.65, 5.33, 7.14, 5.11, 5.7, 4.27, 5.44, 4.51, 5.02, 3.93]})

aveFC_at_65 = df_ARTC[df_ARTC["車速[公里/小時]"]==65]['能效[公里/公升]'].mean()
aveFC_at_85 = df_ARTC[df_ARTC["車速[公里/小時]"]==85]['能效[公里/公升]'].mean()
aveFC65 = f"定速65km/h 平均能效{aveFC_at_65:.2f}km/L"
aveFC85 = f"定速85km/h 平均能效{aveFC_at_85:.2f}km/L"


# 計算節能效益
#(僅就5個車重測試數據試算，待更新)
no_truck = 11386 #111年大貨車新增掛牌車輛數/112年7874
km_truck = 34677 #111年大貨車年平均每車行駛里程
fuel_truck = no_truck * km_truck * (1/ np.mean(y) - 1/np.mean([i*(1+requ_input) for i in y]))/1000.
st.subheader(f"實施大貨車能效管理後，每年新車可節能{fuel_truck:.0f}公秉燃油。")
# st.write(f"原用油{no_truck * km_truck / np.mean(y) / 1000:.3f}公秉、管後用{no_truck * km_truck / np.mean([i*(1+requ_input) for i in y]) / 1000:.3f}公秉")
# print(f"實施大貨車能效管理後，每年新車可節能{fuel_truck:.0f}公秉燃油。")
# print()

st.divider()


# 使用sklearn計算線性迴歸的截距及斜率(係數)
#(僅就5個車重測試數據試算，待更新)
regre_x = np.array([9.5, 11.0, 13.5, 18.5, 26.0])
regre_y = np.array(y)

model = LinearRegression()
model.fit(regre_x[:, np.newaxis], regre_y)

intercept = model.intercept_
slope = model.coef_[0]
# st.write(f"迴歸的截距為{intercept:2f}、斜率為{slope:2f}")
# print(f"迴歸的截距為{intercept:2f}、斜率為{slope:2f}")
# print()


# 使用matplotlib繪圖
# 產生建議管理標準的數據
requ_x=[i for i in range(5, 31, 1)]
requ_y=[(1+requ_input)*(intercept+i*slope) for i in range(5, 31, 1)]

fig, ax = plt.subplots()
ax.plot(df_ARTC[df_ARTC["車速[公里/小時]"]==65]['核定總重[噸]'],
        df_ARTC[df_ARTC["車速[公里/小時]"]==65]['能效[公里/公升]'],
        marker='o', linewidth=0, 
        label=aveFC65)
ax.plot(df_ARTC[df_ARTC["車速[公里/小時]"]==85]['核定總重[噸]'],
        df_ARTC[df_ARTC["車速[公里/小時]"]==85]['能效[公里/公升]'],
        marker='d', linewidth=0,
        label=aveFC85)
ax.plot(requ_x,
        requ_y,
        label="建議管理標準")
ax.axis([5, 30, 0, 10])
ax.set_xlabel('核定總重[噸]')
ax.set_ylabel('能效[公里/公升]')
ax.set_title("本計畫調查之大貨車能效及建議管理標準")
ax.legend()


# streamlit圖示
st.pyplot(fig)

st.divider()

st.write("註:按111年大貨車新車領牌數111,386輛(交通部公路局)、111年大大貨車年平均每車行駛里程34,677公里(交通部交通統計要覽)計算。")

