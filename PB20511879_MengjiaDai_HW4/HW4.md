# 运行说明

## 代码思路

$$
\begin{align}
& 区域为(x,y)\in[0,\pi]\times [0,\pi],已h=\frac{\pi}{90}进行分割，则\\
& n=0,1,...90,有x_i= \frac{i\pi}{90},y_i = \frac{j\pi}{90},\\
& \phi_{i,j}^{(k+1)} =\phi_{i,j}^{(k)}+\frac{\omega}{4}(\phi_{i+1,j}^{(k)}+\phi_{i-1,j}^{(k+1)}+\phi_{i,j+1}^{(k)}+\phi_{i,j-1}^{(k+1)}-h^2q_{i,j}-4\phi_{i,j}^{(k)}) \\
&=\phi_{i,j}^{(k)}+\frac{\omega}{4}(\phi_{i+1,j}^{(k)}+\phi_{i-1,j}^{(k+1)}+\phi_{i,j+1}^{(k)}+\phi_{i,j-1}^{(k+1)}-4\phi_{i,j}^{(k)})\\
&对边界点赋值并保持不变。\\
&即\phi_{0,j}=\phi_{90,j}=\phi_{i,0}=0\\
&\phi_{i,90}=sin(\frac{i\pi}{90})\\
&内点取初值为零进行迭代。\\
&范数判断标准ep = \frac{||\Delta^{(k)}||}{||\phi^{(k)}||}，\Delta_{i,j} = \phi^{(k)}_{i,j}-\phi^{(k-1)}_{i,j}\\
&取ep<10^{-6}停止迭代。
\end{align}
$$

## 实现细节

见代码注释。对差分法所得解，精确解，并计算二者误差（用无穷范数度量）
$$
\begin{align}
&error =\frac{||\Delta||}{||\phi^{exact}||}，\Delta = \phi^{final}_{i,j}-\phi^{exact}_{i,j}
\end{align}
$$


## 运行结果

有限差分法作图：

![image-20221101165936060](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221101165936060.png)

精确解作图

![image-20221101165828129](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221101165828129.png)



范数误差

![image-20221101170005648](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221101170005648.png)

二者结果相同