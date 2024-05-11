# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from scipy import stats

def linear_congurence_2d(a=137, c=187, m=256, seed=1):  
    
    '''
    使用线性同余法产生二维列表的函数
    '''
    array_x = []
    array_y = []  # 建立空列表用于储存两个维度
    rand = seed  # rand为随机数列，初始值为seed
    i = False  # 记录生成数字序号奇偶性
    rand_norm = rand/m # 将生成的随机数置于[0,1]
    while rand: 
        if not i:  # 将序号偶数的随机数赋给array_x
            array_x.append(rand_norm)
        else:  # 将序号奇数的随机数赋给array_y
            array_y.append(rand_norm)
        rand = (a * rand + c) % m
        rand_norm =  rand/m  # 计算下一个随机数值
        i = not i  # 改变序号奇偶性
    if i:
        array_x.pop()
    return array_x, array_y  # 返回二维随机数列


def linear_congurence_3d(a=137, c=187, m=256, seed=1):  
    
    '''
    使用线性同余法产生三维列表的函数
    '''
    array_x = []
    array_y = [] 
    array_z = []  # 建立空列表用于储存三个维度
    rand = seed  # rand为随机数列，初始值为seed
    i = 0  # 记录生成数字序号被3整除的余数
    rand_norm = rand/m # 将生成的随机数置于[0,1]
    while rand: 
        if i == 0:  # 将序号偶数的随机数赋给array_x
            array_x.append(rand_norm)
        elif i == 1:  # 将序号奇数的随机数赋给array_y
            array_y.append(rand_norm)
        elif i == 2:
            array_z.append(rand_norm)
        rand = (a * rand + c) % m
        rand_norm =  rand/m  # 计算下一个随机数值
        i = (i + 1) % 3  # 改变序号奇偶性
    if i == 1:
        array_x.pop()
    elif i == 2:
        array_x.pop()
        array_y.pop()
    return array_x, array_y, array_z  # 返回二维随机数列


def uniformity_3d(array_x, array_y, array_z, segment = 3):
    
    '''
    验证三维均匀性
    '''
    
    cell = [0] * pow(segment, 3)  # 将三维空间均匀分割为小立方体
    # 每个立方体计包含的初始点数为零
    for i in range(len(array_x3d)):  # 使用int向下取证，将坐标值分入所属立方体内
        index = int(array_x3d[i] * segment) + int(array_y3d[i] * segment) * segment + int(array_z3d[i] * segment) * segment * segment
        cell[index] = cell[index] +1
        # calculate chi2卡方检验所使用的值
        chi2 = 0  # 初始化
    for i in range(27):
        chi2 += pow(cell[i]-(len(array_x3d)/27), 2)/(len(array_x3d)/27)  # 卡方检验值   
    chi2 = chi2/(27-1)  # 自由度归一
    print("chi2 value is: {0:.4f}".format(chi2))  # 打印归一后的chi2值 
    pvalue = 1 - stats.chi2.cdf(chi2,1)  # p值
    print("corresponding to a p-value of: {0:.4f}".format(pvalue))  # 打印p值


if __name__ == '__main__':
    # 绘图
    array_x2d, array_y2d = linear_congurence_2d()  #生成二维随机列表
    array_x3d, array_y3d, array_z3d = linear_congurence_3d()  # 生成三维随机列表
    plt.figure(figsize=(10,6))  # 设置绘图区域参数
    plt.scatter(array_x2d, array_y2d, marker='o')  # 绘制二维散点图
    plt.figure(figsize=(10,6))  # 设置绘图区域参数
    ax = plt.axes(projection = '3d')  # 创建3d绘图区域
    ax.scatter3D(array_x3d, array_y3d, array_z3d)  # 绘制三维散点图
    
    # 验证三维均匀性
    uniformity_3d(array_x3d, array_y3d, array_z3d, segment = 3)
    



    
        