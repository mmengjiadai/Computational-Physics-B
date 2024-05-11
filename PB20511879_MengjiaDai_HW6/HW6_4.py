import random
from math import pi, cos, sin, sqrt
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


npar = 64  # 粒子数
ngrid = 10  # 边界划分数
L = 10  #每个划分的长度
T = 85
kB = 1.38 * pow(10, -23)

Xs, Ys, VXs, VYs= [], [], [], []  # 坐标和速度
node = random.sample(range(1, pow(ngrid - 1,2)), npar)  # 初始化格点编号

#随机初始化
for par in range(npar):  # 给x, y, z坐标赋值
    Xs.append(1 + node[par] // (ngrid - 1))
    Ys.append(1 + node[par] % (ngrid - 1))
    alpha = pi*random.uniform(0,1)
    v = random.uniform(0,1)
    VXs.append(cos(alpha) * v)
    VYs.append(sin(alpha) * v) 
 
#画出初始条件
plt.xlim(0,10)       
plt.ylim(0,10)
plt.grid()
plt.scatter(Xs, Ys, color = 'b')
plt.quiver(Xs, Ys, VXs, VYs, alpha = 0.5, color = 'g')
plt.draw()    

dt = 0.02  # 每步间的时间间隔
nsim = 200  # 迭代步数
Xss, Yss, VXss, VYss = [Xs], [Ys], [VXs], [VYs]  # 存储每一步坐标和速度
FXss, FYss = [], []  # 储存每一步所受力
tXs, tYs, tVXs, tVYs = [], [], [], []
tFXs, tFYs = [], []
for sim in range(nsim):
    tXs = []
    tYs = []
    tVXs = []
    tVYs = []
    tFXs = []
    tFYs = []
    r = [[0] * npar for _ in range(npar)]  # 记录
    index_image = [[0] * npar for _ in range(npar)]
    #带t的是临时操作用的状态
    for par in range(npar):#给临时状态赋值
        tXs.append(Xss[sim][par])
        tYs.append(Yss[sim][par])
        tVXs.append(VXss[sim][par])
        tVYs.append(VYss[sim][par])
        tFXs.append(0)
        tFYs.append(0)
    for par1 in range(npar):  # 对于每一个粒子
        for par2 in range(npar): #遍历其他例子找出其最小像粒子
            if par2 < par1: continue
            r_choice = [0] * 9
            for i in range(3):
                for j in range(3):  # 求出可能的最小半径值 
                        r_choice[i * 3 + j] = sqrt(pow(tXs[par1] - tXs[par2] + (i - 1)  * L , 2) + pow(tYs[par1] - tYs[par2] + (j - 1) * L, 2))
            r[par1][par2] = r[par2][par1] = min(r_choice)  # 记录最小像矢径
            index_image[par1][par2] = index_image[par2][par1] = np.argmin(r_choice)  # 记录最小像坐标        
    for par1 in range(npar):
        for par2 in range(npar):
            if r[par1][par2] == 0:
                continue
            #if r[i][j] == 0: continue
            tFXs[par1] += 48 * (tXs[par1] - tXs[par2] +  (index_image[par1][par2]//9 - 1) * L) * (pow(r[par1][par2], -14) - 0.5 * pow(r[par1][par2], -8))
            tFYs[par1] += 48 * (tYs[par1] - tYs[par2] +  ((index_image[par1][par2]%9)//3 - 1) * L) * (pow(r[par1][par2], -14) - 0.5 * pow(r[par1][par2], -8))
            if(sim != 0):
                tVXs[par1] += dt * (tFXs[par1] + FXss[sim-1][par1]) / 2
                tVYs[par1] += dt * (tFYs[par1] + FYss[sim-1][par1]) / 2
    # 计算beta修正v
    sum_v_square = 0
    for par in range(npar):
        sum_v_square += pow(tVXs[par], 2) + pow(tVYs[par], 2)
    beta = pow((3 * npar - 4) * kB * T / sum_v_square, 0.5)
    # 速度乘beta作为下一次迭代的速度
    for par1 in range(npar):
        # 计算下一步的坐标值
        # 用余数限制在原胞内
        tXs[par1] += dt * beta * tVXs[par1] + 0.5 * tFXs[par1] * pow(dt, 2)     
        tYs[par1] += dt * beta * tVYs[par1] + 0.5 * tFYs[par1] * pow(dt, 2)        
        tXs[par1] = tXs[par1] % (L * ngrid)
        tYs[par1] = tYs[par1] % (L * ngrid)
    Xss.append(tXs)
    Yss.append(tYs)
    VXss.append(tVXs)
    VYss.append(tVYs)
    FXss.append(tFXs)
    FYss.append(tFYs)

#对于最后一步计算速度（之前每一步求解速度比）
for par in range(npar):#给临时状态赋值
    tVXs.append(VXss[nsim-1][par])
    tVYs.append(VYss[nsim-1][par])
for par in range(npar):
    tVXs[par] += dt * (FXss[nsim-1][par] + FXss[nsim-2][par]) / 2
    tVYs[par] += dt * (FYss[nsim-1][par] + FYss[nsim-2][par]) / 2
VXss.append(tVXs)
VYss.append(tVYs)

fig = plt.figure()
def animate(nframe):
    plt.cla()
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.grid()
    plt.scatter(Xss[nframe], Yss[nframe], color = 'b')
    plt.quiver(Xss[nframe], Yss[nframe], VXss[nframe], VYss[nframe], alpha = 0.5 ,color = 'green')
    plt.draw()   
anim = animation.FuncAnimation(fig,animate,frames = nsim)
anim.save("HW6_4.gif",fps = 10)