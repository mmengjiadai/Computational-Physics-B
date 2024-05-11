import numpy as np
import matplotlib.pyplot as plt

# 定义类描述元素
class element:
    def __init__(self, index, x, y):
        # 记录三角形元素的三个节点编号和坐标
        self.index = index
        self.x = x
        self.y = y
        # 计算三角形元素的b和c
        self.b = [self.y[(i+1)%3]-self.y[(i+2)%3] for i in range(3)]
        self.c = [self.x[(i+2)%3]-self.x[(i+1)%3] for i in range(3)]

def finite_element_matrix(lenx, leny ,x_index, y_index):  # 定义函数输出有限元素法线性方程矩阵，传入边界分割间距h
    element_index = np.zeros((lenx, leny), dtype = int)  #初始化格点编号
    index = 0;
    for i in range(1,lenx-1):  # 先给内点赋值
        for j in range(1,leny-1):
            element_index[i][j] = index
            index = index + 1
    n_inner = index
    for i in range(lenx):  # 给边界点赋值
        element_index[0][i] = index 
        index = index + 1
    for i in range(1,lenx-1):
        element_index[i][0] = index 
        index = index + 1
        element_index[i][leny-1] = index
        index = index + 1
    for i in range(lenx):  # 给边界点赋值
        element_index[leny-1][i] = index 
        index = index + 1
    n_outer = index - n_inner
    element_list = [] # 初始化元素列表
    # 按顺序添加元素
    for i in range(lenx-1):
        for j in range(1, leny):
            element_list.append(
                element(
                    index=[element_index[i, j], element_index[i, j-1], element_index[i+1, j-1]],
                    x=[x_index[i], x_index[i], x_index[i+1]],
                    y=[y_index[j], y_index[j-1], y_index[j-1]]
                )
            )
            element_list.append(
                element(
                    index=[element_index[i, j], element_index[i+1, j-1], element_index[i+1, j]],
                    x=[x_index[i], x_index[i+1], x_index[i+1]],
                    y=[y_index[j], y_index[j-1], y_index[j]]
                )
            )
    
    # 按有限元素方法计算矩阵
    Delta = (bound_x[1] - bound_x[0])*(bound_y[1] - bound_y[0])/len(element_list)
    K = np.zeros((index,index))  # 新建K矩阵
    for e in element_list:  # 由对称性计算K的一半
        for i in range(3):
            for j in range(i, 3):
                K[e.index[i], e.index[j]] += (e.b[i]*e.b[j] + e.c[i]*e.c[j])/4/Delta
    K += K.T - np.diag(np.diag(K))  # 由对称性补全K矩阵
    
    # 代入边界条件
    Phi_2 = np.zeros((n_outer, 1))
    Phi_2[:lenx, 0] = Phi_2[-lenx:, 0] = np.ones(lenx)
    
    # 返回线性方程组矩阵
    return K, Phi_2, element_index, n_inner

def over_relaxation_iteration(lenx, leny, element_index, Phi_2, n_inner, K, omega, norm_stop):  #超松弛迭代
    phi = np.hstack((np.ones(n_inner), Phi_2.T[0]))  # 只需迭代内点，初始化为1，拼接边界点
    phi_last = phi.copy()  # 储存上一次迭代结果
    step = 0  # 记录迭代步数
    norm = 1  # 范数判断迭代是否停止，初始化为1
    k_nonzero = []  # 找出矩阵中的非零值
    for i in range(n_inner):
        k_nonzero.append([])
        for j in range(lenx*leny):
            if K[i, j] != 0 and i != j:
                k_nonzero[-1].append(j)    
    # 迭代时只改变内部节点
    while norm > 1e-6:
        for i in range(n_inner):
            phi[i] = (1-omega)*phi[i]
            a = omega/K[i, i]
            for j in k_nonzero[i]:
                phi[i] -= a*K[i, j]*phi[j]
        norm = np.max(abs(phi-phi_last))
        phi_last = phi.copy()
        step += 1
    print("omega = %f, Converges in %d steps" %(omega,step))  # 输出迭代步数
    solution = np.zeros((lenx, leny))
    for i in range(lenx):  # 填入函数值
        for j in range(leny):
            solution[i, j] = phi[element_index[i, j]]
    return solution  # 将函数值转化为xy平面矩阵形式并输出

def plot_contour(solution, x_index, y_index):  # 对函数值作图
    fig = plt.figure(figsize=(5, 5), dpi=100)
    plt.contourf(x_index, y_index, solution.T)
    plt.show()
    
# 测试程序
if __name__ == '__main__':
    # 依题意设定参数
    h = 0.1
    bound_x = [0.0, 1.0] #边界x坐标
    bound_y = [0.0, 1.0] #边界y坐标
    lenx = len(np.arange(bound_x[0], bound_x[1], h)) + 1  # x格点数目
    leny = len(np.arange(bound_y[0], bound_y[1], h)) + 1  # y格点数目
    x_index = np.arange(bound_x[0], bound_x[1]+h, h)  # x格点坐标
    y_index = np.arange(bound_y[0], bound_y[1]+h, h)  # y格点坐标
    phi_ans = np.zeros((lenx + 1)*(leny + 1))
    K, Phi_2, element_index, n_inner= finite_element_matrix(lenx, leny ,x_index, y_index) 
    #for i in np.linspace(1.0,1.9,19)
    #for i in np.linspace(1.5,1.6,21):
    #    solution = over_relaxation_iteration(lenx, leny, element_index, Phi_2, n_inner, K, i, 1e-6)  
    solution = over_relaxation_iteration(lenx, leny, element_index, Phi_2, n_inner, K, 1.54, 1e-6)
    plot_contour(solution, x_index, y_index)