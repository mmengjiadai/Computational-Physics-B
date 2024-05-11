# 机器学习作业（HW9）

## 伊辛模型

1. 代码见Ising_1.py。取树木棵树为30，树木深度参数设为None，叶子上最小样本数分别取2和1000，对样本比例百分之[0.1,10,20,30,40,50,60,70,80,90]进行遍历，

   ![image-20230114122053433](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230114122053433.png)作图如下

   最小样本数2:

   ![accuracy_ration_2](D:\PYTHON\pytorch\HW9_PB20511879_MengjiaDai\Ising\accuracy_ration_2.png)

   

   最小样本数10000:

   ​					![accuracy_ratio_10000](D:\PYTHON\pytorch\HW9_PB20511879_MengjiaDai\Ising\accuracy_ratio_10000.png)

   有此可知，训练样本比例对精度影响较小。在最小样本数为10000时Train accuracy在testset比例较低时随testset占比增大而减小。

2. 取样本比例0.9:0.1，用OOB_accuracy衡量超参数优劣

   叶子上最小样本数：[2, 3000, 7000, 10000]

   取树木棵树：n_estimator_range=[10,20,30,40,50,60,70,80,90,100]

   树木深度：max_depth_range = [3,5,8,15,25,30,None]

   train accuracy:

   ![image-20230110224354755](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110224354755.png)

   ![image-20230110224400804](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110224400804.png)

   ![image-20230110224412373](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110224412373.png)

   test accuracy:

   ![image-20230110230059799](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230059799.png)

   ![image-20230110230108207](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230108207.png)

   ![image-20230110230121474](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230121474.png)

   ![image-20230110230134956](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230134956.png)

   critical accuracy:

   ![image-20230110230152695](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230152695.png)

   ![image-20230110230158120](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230158120.png)

   ![image-20230110230213074](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230213074.png)

   ![image-20230110230223660](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230110230223660.png)

由此可知随着树木棵树的增大，准确率总体呈增大趋势；随着叶子上最小样本数的增大，准确率总体呈减小趋势；准确率不受树木深度的影响。

寻找OOB accuracy最大的参数：

leaf_size: 2, n_estimators: 90, max_depth: 3
leaf_size: 2, n_estimators: 90, max_depth: 5
leaf_size: 2, n_estimators: 90, max_depth: 8
leaf_size: 2, n_estimators: 90, max_depth: 15
leaf_size: 2, n_estimators: 90, max_depth: 25
leaf_size: 2, n_estimators: 90, max_depth: 30
leaf_size: 2, n_estimators: 90, max_depth: None 
leaf_size: 2, n_estimators: 100, max_depth: 3
leaf_size: 2, n_estimators: 100, max_depth: 5
leaf_size: 2, n_estimators: 100, max_depth: 8
leaf_size: 2, n_estimators: 100, max_depth: 15
leaf_size: 2, n_estimators: 100, max_depth: 25
leaf_size: 2, n_estimators: 100, max_depth: 30
leaf_size: 2, n_estimators: 100, max_depth: None 

用OOB准确率来选择最佳超参数，则为以上参数。即树木深度小，树木棵树大，深度任意

## 超对称

1. 取train_size = [1000, 900000, 1800000, 2700000, 3600000, 4500000]

   ![image-20230113215531797](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113215531797.png)

   单层隐藏层包含1000个神经元，用batchnorm防止过拟合，learning rate取0.1

   ![image-20230113215504561](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113215504561.png)

   ![image-20230113215230310](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113215230310.png)

   精度随datasize的增大先增大后趋于稳定

2. 取测试集与训练集样本总是为1000，learning rate取0.01

   ![image-20230113203440571](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113203440571.png)

   取层数1到5，作为参数传入model类，按照层数增加隐藏层

   ![image-20230113203538718](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113203538718.png)

   

训练结果作图如下

![image-20230113204536587](C:\Users\pseudonym\AppData\Roaming\Typora\typora-user-images\image-20230113204536587.png)

准确率随层数的增加而减小。