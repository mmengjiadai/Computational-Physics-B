# 作业三

## 理论推导

 
$$
\begin{align}
&f(x)=Aexp(-\frac{x^2}{2})\\
&归一化条件\int_{-\infty}^{\infty}f(x)dx=1\\
&A=\frac{1}{\int_{-\infty}^{\infty}exp(-\frac{x^2}{2})}=\frac{1}{\sqrt{2\pi}}
\end{align}
$$
A的值不需要知道

## 代码说明

包含高斯抽样函数，抽样结果作图函数。运行该程序，从命令行传入参数，可调用前述两函数得到结果。具体见注释

## 运行结果

设置delta下限0.1，上限2.0，中间取20个点，对于x均值和x的平方均值，epsilon均取0.01.抽样结果如下图

<center class="half">    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011153306016.png" width="200"/>    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154148792.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154239867.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154249717.png" width="200"/> </center>

<center class="half">    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154258892.png" width="200"/>     <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154311379.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154320515.png" width="200"/> <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154334130.png" width="200"/> </center>

<center class="half">        <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154348805.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154358887.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154408599.png" width="200"/> 
<img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155607557.png" width="200"/></center>

<center class="half">    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155631294.png" width="200"/>    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155640376.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155648971.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155657127.png" width="200"/> </center>

<center class="half">    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155704762.png" width="200"/>    <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155711409.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155719020.png" width="200"/>  <img src="C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011155726427.png" width="200"/> </center>

所测得时间和accept/try比值如下,分别作图

![image-20221011161959811](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011161959811.png)

![image-20221011161908099](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011161908099.png)

![image-20221011161925354](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011161925354.png)

执行多次，发现每次结果不同，抽样图像与time-delta，ratio-delta曲线均有较大涨落，总体趋势为time和ratio均随delta的下降而下降。

保持delta不变，改变epsilon为0.1或0.001，发现图像与理论曲线严重不符。调节delta为0.1至1.0，间隔0.1，同样对三种epsilon测试，同样发现仅有epsilon=0.01时图像较为平滑。epsilon越大，迭代次数越小，time越小，ratio无明显规律

总共发现了两个点效果较好，epsilon均取0.01，如图

![image-20221011164443624](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011164443624.png)

![image-20221011164443624](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20221011154148792.png)