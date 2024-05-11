# -*- coding: utf-8 -*-
import random
import math
import matplotlib.pyplot as plt


# (1)
array_x = []  # 创建空数组储存均匀分布随机数
array_y = []  # 创建空数组储存指数分布随机数
for i in range(1,10000):
    array_x.append(random.uniform(0,1))  # 抽取10000个[0,1]均匀分布随机数
index_exp= 1.0  # 指数分布的参数为1
for x in array_x:  # 变换抽样
    array_y.append((-1.0/index_exp)*math.log(x))
# 作图
plt.hist(array_y, bins = 100)
plt.plot()

# (2)
for i in range(0,10000000):  # 在[0,1]均匀分布区间抽取10000000个随机数
    array_x.append(random.uniform(0, 1)) 
for x in array_x:
    array_y.append((-1.0/index_exp)*math.log(x))  # 计算满足提给分布的随机数值
I = 0  # 积分结果初始化
for y in array_y:  # 计算积分结果
    I += 1 / 10000000 * math.pow(y,1.5) 
print("I = ", I, sep='')  # 打印结果