# -*- coding: utf-8 -*-
from math import pow, exp, pi, sqrt
from random import uniform
from time import time
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Metropolis方法抽取Gauss分布
def Gauss(x, delta, ep_mean, ep_smean):  # 传入设定的x，delta，判断平衡所用条件
    # 初始化各变量
    walks = [x]
    Ntry, Nacc = 0, 0
    mean = x
    square_mean = pow(x,2)
    start = time()  # 计算起始时间
    retry = True
    while(retry): # 平衡条件判据
        while True:  #执行while循环直至accept
            Ntry += 1
            xtry = x + uniform(-1.0*delta,delta)
            while xtry < -5.0 or xtry > 5.0:
                xtry = x + uniform(-1.0*delta,delta)
            r = exp(-0.5*pow(xtry,2))/exp(-0.5*pow(x,2))
            if r>=1.0:  # 第一个条件成立则更新数据并跳出循环
                x = xtry
                Nacc += 1
                break  
            elif uniform(0,1) <= r:  # 第二个条件成立则更新数据并跳出循环
                x = xtry
                Nacc += 1
                break
            else:  # 否则不更细，继续循环
                walks.append(x)
                mean = (mean*(len(walks) - 1) + x)/len(walks)
                square_mean = (square_mean*(len(walks) - 1) + pow(x,2))/len(walks) 
        walks.append(x)
        mean = (mean*(len(walks) - 1) + x)/len(walks)
        square_mean = (square_mean*(len(walks) - 1) + pow(x,2))/len(walks)  # 更新平衡条件判据
        retry = (abs(mean)>0.1) or (abs(square_mean-1)>0.1)
    finish = time()  # 计算结束时间
    total = finish - start
    return walks, Ntry, Nacc, total

# 对抽样结果作图
def walkplot(walks,d):
    X = np.linspace(-5,5,100)
    Y = 1/sqrt(2*pi)*np.exp(-0.5*np.power(X,2))
    plt.figure()
    plt.plot(X,Y)  # 作出理论曲线图
    plt.hist(walks, bins = 100, range = [-5,5], density = True)  # 作出分布图
    plt.title('delta = {0}'.format(d))  
    plt.show()
    
# 测试程序
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Enter required data')  # 命令行传参设置
   parser.add_argument("-mi","--delta_min", type=float,default = 0.1)
   parser.add_argument("-ma","--delta_max", type=float,default = 2.0)
   parser.add_argument("-nu","--delta_num", type=int,default = 20)
   parser.add_argument("-em","--ep_mean", type=float,default = 0.01)
   parser.add_argument("-es","--ep_smean", type=float,default = 0.01)
   args = parser.parse_args()
   times = []  # 记录时间
   ratio = []  # 记录比例
   delta = np.linspace(args.delta_min,args.delta_max,args.delta_num)
   for d in delta:  # 对多个delta批量测试
       walks, Ntry, Nacc, total = Gauss(0.0, d, args.ep_mean, args.ep_smean)
       print("delta = {0}: time = {1}s, ratio = {2}".format(d, total, float(Nacc)/float(Ntry)))
       times.append(total)
       ratio.append(float(Nacc)/float(Ntry))
       walkplot(walks,d)
   plt.figure()  # 以delta为横坐标对time作图
   plt.plot(delta,times)
   plt.title('time')
   plt.xlabel('delta')
   plt.ylabel('time/s')
   plt.show()
   plt.figure()  # 以delta为横坐标对ratio作图
   plt.plot(delta,ratio)
   plt.title('ratio')
   plt.xlabel('delta')
   plt.ylabel('ratio')
   plt.show()