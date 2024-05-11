import random
from math import pi, cos, sin, sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy as np


npar = 64  # 粒子数
ngrid = 10  # 边界划分数
L = 10  # 原胞变长
#ballsize = 1
Xs, Ys, Zs, VXs, VYs, VZs = [], [], [], [], [], []  # 坐标和速度
node = random.sample(range(1, pow(ngrid - 1,3)), npar)  # 初始化格点编号

#随机初始化
for par in range(npar):  # 给x, y, z坐标赋值
    Xs.append(1 + node[par] // pow(ngrid - 1,2))
    Ys.append(1 + node[par] % pow((ngrid - 1),2) // (ngrid - 1))
    Zs.append(1 + node[par] % pow((ngrid - 1),2) % (ngrid - 1))
    alpha = pi*random.uniform(0,1)
    beta = pi*random.uniform(0,1)
    v = random.uniform(0,1)
    VXs.append(cos(alpha) * v)
    VYs.append(sin(alpha) * cos(beta) * v)
    VZs.append(sin(alpha) * sin(beta) * v)   
 
#画出初始条件
fig = plt.figure()
ax = fig.gca(projection = '3d')
ax.scatter(Xs, Ys, Zs, c = 'b')
ax.quiver(Xs, Ys, Zs, VXs, VYs, VZs, length = 1, alpha = 0.5, color = 'g')
plt.show()    

dt = 0.02  # 每步间的时间间隔
nsim = 200  # 迭代步数
Xss, Yss, Zss, VXss, VYss, VZss = [Xs], [Ys], [Zs], [VXs], [VYs], [VZs]  # 存储每一步坐标和速度
FXss, FYss, FZss = [], [], []  # 储存每一步所受力
tXs, tYs, tZs, tVXs, tVYs, tVZs = [], [], [], [], [], []
tFXs, tFYs, tFZs = [], [], []
for sim in range(nsim):
    tXs = []
    tYs = []
    tZs = []
    tVXs = []
    tVYs = []
    tVZs = []
    tFXs = []
    tFYs = []
    tFZs = []
    r = [[0] * npar for _ in range(npar)]  # 记录
    index_image = [[0] * npar for _ in range(npar)]
    #带t的是临时操作用的状态
    for par in range(npar):#给临时状态赋值
        tXs.append(Xss[sim][par])
        tYs.append(Yss[sim][par])
        tZs.append(Zss[sim][par])
        tVXs.append(VXss[sim][par])
        tVYs.append(VYss[sim][par])
        tVZs.append(VZss[sim][par])
        tFXs.append(0)
        tFYs.append(0)
        tFZs.append(0)
    for par1 in range(npar):  # 对于每一个粒子
        for par2 in range(npar): #遍历其他例子找出其最小像粒子
            if par2 < par1: continue
            r_choice = [0] *27 
            for i in range(3):
                for j in range(3):
                    for k in range(3):  # 求出可能的最小半径值
                        r_choice[i * 9 + j * 3 + k] = sqrt(pow(tXs[par1] - tXs[par2] + (i - 1)  * L , 2) + pow(tYs[par1] - tYs[par2] + (j - 1) * L, 2) + pow(tZs[par1] - tZs[par2] + (k - 1) * L, 2))
            r[par1][par2] = r[par2][par1] = min(r_choice)  # 记录最小像矢径
            index_image[par1][par2] = index_image[par2][par1] = np.argmin(r_choice)  # 记录最小像坐标        
    for par1 in range(npar):
        for par2 in range(npar):
            if r[par1][par2] == 0:
                continue
            tFXs[par1] += 48 * (tXs[par1] - tXs[par2] +  (index_image[par1][par2]//9 - 1) * L) * (pow(r[par1][par2], -14) - 0.5 * pow(r[par1][par2], -8))
            tFYs[par1] += 48 * (tYs[par1] - tYs[par2] +  ((index_image[par1][par2]%9)//3 - 1) * L) * (pow(r[par1][par2], -14) - 0.5 * pow(r[par1][par2], -8))
            tFZs[par1] += 48 * (tZs[par1] - tZs[par2] +  (((index_image[par1][par2]%9)%3) - 1) * L) * (pow(r[par1][par2], -14) - 0.5 * pow(r[par1][par2], -8))
        if(sim != 0):
            tVXs[par1] += dt * (tFXs[par1] + FXss[sim-1][par1]) / 2
            tVYs[par1] += dt * (tFYs[par1] + FYss[sim-1][par1]) / 2
            tVZs[par1] += dt * (tFZs[par1] + FZss[sim-1][par1]) / 2
        # 计算下一步的坐标值
        # 用余数限制在原胞内
        tXs[par1] += dt * tVXs[par1] + 0.5 * tFXs[par1] * pow(dt, 2)     
        tYs[par1] += dt * tVYs[par1] + 0.5 * tFYs[par1] * pow(dt, 2)        
        tZs[par1] += dt * tVZs[par1] + 0.5 * tFZs[par1] * pow(dt, 2)
        tXs[par1] = tXs[par1] % L
        tYs[par1] = tYs[par1] % L
        tZs[par1] = tZs[par1] % L
    Xss.append(tXs)
    Yss.append(tYs)
    Zss.append(tZs)
    VXss.append(tVXs)
    VYss.append(tVYs)
    VZss.append(tVZs)
    FXss.append(tFXs)
    FYss.append(tFYs)
    FZss.append(tFZs)

#对于最后一步计算速度（之前每一步求解速度比）
for par in range(npar):#给临时状态赋值
    tVXs.append(VXss[nsim-1][par])
    tVYs.append(VYss[nsim-1][par])
    tVZs.append(VZss[nsim-1][par])
for par in range(npar):
    tVXs[par] += dt * (FXss[nsim-1][par] + FXss[nsim-2][par]) / 2
    tVYs[par] += dt * (FYss[nsim-1][par] + FYss[nsim-2][par]) / 2
    tVZs[par] += dt * (FZss[nsim-1][par] + FZss[nsim-2][par]) / 2
VXss.append(tVXs)
VYss.append(tVYs)
VZss.append(tVZs)

fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim3d(0,10)
ax.set_ylim3d(0,10)
ax.set_zlim3d(0,10)
def animate(nframe):
    plt.cla()
    ax.set_xlim3d(0,10)
    ax.set_ylim3d(0,10)
    ax.set_zlim3d(0,10)
    ax.scatter(Xss[nframe], Yss[nframe], Zss[nframe], c = 'b')
    ax.quiver(Xss[nframe], Yss[nframe], Zss[nframe], VXss[nframe], VYss[nframe], VZss[nframe], length = 1, alpha = 0.5 ,color = 'green')
anim = animation.FuncAnimation(fig,animate,frames = nsim)
anim.save("HW6_3.gif",fps = 10)