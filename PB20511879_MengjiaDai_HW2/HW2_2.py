# -*- coding: utf-8 -*-
#（1）
import random
import math
import matplotlib.pyplot as plt


array_x = []
array_y = []
for i in range(0,10000):  # 在[0,1]均匀分布区间抽取1000个随机数
    array_x.append(random.uniform(0, 1)) 
for x in array_x:
    array_y.append(math.tan(math.pi*x))  # 计算满足提给分布的随机数值
# 作图（由于所给随机数分布于无穷区间内，故限定作图范围-10~10）
plt.hist(array_y, bins = 1000, range=(-10,10)) 
plt.show()

# (2)
for i in range(0,10000000):  # 在[0,1]均匀分布区间抽取10000000个随机数
    array_x.append(random.uniform(0, 1)) 
for x in array_x:
    array_y.append(math.tan(math.pi*x))  # 计算满足提给分布的随机数值
I_0 = 0  # x>0区间积分结果初始化
for y in array_y:  # 计算x>0区间积分结果
    I_0 += 1 / (2 * 10000000) * math.pi * math.sqrt(abs(y))
print("I = (1+i)", I_0, sep='')  # 打印结果
