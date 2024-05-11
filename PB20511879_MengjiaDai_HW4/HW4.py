# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

phi = np.zeros((91, 91))  # numpy二维数组储存差分点函数值，初值设为0
phi_last = np.zeros((91, 91))  # numpy二维数组储存前一次迭代后差分点函数值，初值设为0
# 对边界点赋值，不再改变
for i in range(91):
    phi[i][0] = 0
    phi[i][90] = np.sin(i*np.pi/90)
    phi[0][i] = 0
    phi[90][i] = 0
ep = 1
while(ep>1e-6):  # 范数判断条件
    for i in range(91):
        for j in range(91):
            phi_last[i][j] = phi[i][j]  # 此次迭代值赋给phi_last
    # 按从左下角开始，向右向上的顺序，开始迭代
    for i in range(1,90,1):
        for j in range(1,90,1):
            phi[i][j] = phi[i][j] + (7/16)*(phi[i+1][j] + phi[i-1][j] + phi[i][j+1] + phi[i][j-1] - 4 * phi[i][j])
    ep = np.linalg.norm(np.abs(phi-phi_last), ord=np.inf)/np.linalg.norm(phi, ord=np.inf)  # 计算范数迭代条件
    
# 作图
z_fin = phi.reshape((1, 91*91))  # 化为一维，投影到z轴作图
x = np.zeros((91,91))  # 建立x坐标值矩阵
for i in range(91):
    for j in range(91):
        x[i][j] = i*np.pi/90
x_ax = x.reshape((1, 91*91))  # 化为一维，投影到x轴作图
y = np.zeros((91,91))  # 建立x坐标值矩阵
for i in range(91):
    for j in range(91):
        y[i][j] = j*np.pi/90
y_ax = y.reshape((1, 91*91))  # 化为一维，投影到x轴作图

colors = np.arange(20, 80, 60.0/(91*91))  # 建立颜色列表
fig = plt.figure()
ax = Axes3D(fig)  # 画三维图
ax.set_xlabel('x')  # 标注坐标轴
ax.set_ylabel('y')
ax.set_title("Finite Difference",fontsize=20)  # 标注有限差分法
ax.scatter(x_ax, y_ax, z_fin, c=colors, cmap='viridis')  # 使用cmap以区分图像
plt.show()  # 作图

z = np.zeros((91,91))  # 建立精确值矩阵
for i in range(91):
    for j in range(91):
        z[i][j] = np.sin(i*np.pi/90)*np.sinh(j*np.pi/90)/np.sinh(np.pi)
z_exact = z.reshape((1,91*91))  # 化为一维，投影到z轴作图
fig_exact = plt.figure()  
ax_exact = Axes3D(fig_exact)  # 画三维图
ax_exact.set_xlabel('x')  # 标注坐标轴
ax_exact.set_ylabel('y')
ax_exact.set_title("Exact Solution",fontsize=20)  # 标注精确解
ax_exact.scatter(x_ax, y_ax, z_exact, c=colors, cmap='magma')  # 使用cmap以区分图像
plt.show()  # 作图

# 打印相差的范数
ep = np.linalg.norm(np.abs(z-phi),ord=np.inf)/np.linalg.norm(z,ord=np.inf)
print('error: ',ep)

