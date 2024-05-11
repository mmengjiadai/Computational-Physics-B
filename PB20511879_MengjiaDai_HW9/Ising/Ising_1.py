import numpy as np
import pickle, os
from urllib.request import urlopen
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import time
import warnings

# 启用警告
warnings.filterwarnings("ignore")
# 加载数据
print("Loading data ... ")
#url_main = 'https://physics.bu.edu/~pankajm/ML-Review-Datasets/isingMC/';
data_file_name = r"D:\PYTHON\pytorch\HW9_PB20511879_MengjiaDai\Ising\Ising2DFM_reSample_L40_T=All.pkl" 
label_file_name = r"D:\PYTHON\pytorch\HW9_PB20511879_MengjiaDai\Ising\Ising2DFM_reSample_L40_T=All_labels.pkl"
with open(data_file_name,'rb') as f1:
    data = pickle.load(f1)
    data = np.unpackbits(data).reshape(-1, 1600)
    data=data.astype('int')
    data[np.where(data==0)]=-1
with open(label_file_name,'rb') as f2:
    labels = pickle.load(f2)
print("Finished")

# 对数据分组
X_ordered=data[:70000,:]
Y_ordered=labels[:70000]
X_critical=data[70000:100000,:]
Y_critical=labels[70000:100000]
X_disordered=data[100000:,:]
Y_disordered=labels[100000:]
del data,labels
X=np.concatenate((X_ordered,X_disordered))
Y=np.concatenate((Y_ordered,Y_disordered))
# 设置树木棵树
n_estimator = 30
# 设置叶子上最小样本数
leaf_size = 2
print("Setting Classifier ... ")

# 随机森林
classifer = RandomForestClassifier
# 按照不同的比例分割并定义数据集
divs = [0.1,10,20,30,40,50,60,70,80,90]
n = len(divs)
myRF_clf = classifer(
        n_estimators=n_estimator,
        max_depth=None,
        min_samples_split=leaf_size, # minimum number of sample per leaf
        oob_score=True,
        random_state=0,
        warm_start=True # this ensures that you add estimators without retraining everything
    )
RFC_OOB_accuracy=np.zeros((n,1))
RFC_train_accuracy=np.zeros((n,1))
RFC_test_accuracy=np.zeros((n,1))
RFC_critical_accuracy=np.zeros((n,1))
run_time=np.zeros((n,1))
print_flag=True
print("Finished")
for i, div in enumerate(divs):
    train_to_test_ratio=div/100
    print()
    print('n_estimators: %i, leaf_size: %i, train:test = %.3f:%.3f'%(n_estimator,leaf_size,train_to_test_ratio,1-train_to_test_ratio))
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=train_to_test_ratio)
    print('X_train shape:', X_train.shape)
    print('Y_train shape:', Y_train.shape)
    print()
    print(X_train.shape[0], 'train samples')
    print(X_critical.shape[0], 'critical samples')
    print(X_test.shape[0], 'test samples')
    start_time = time.time()
    myRF_clf.set_params(n_estimators=n_estimator)
    myRF_clf.fit(X_train, Y_train)
    run_time[i,0] = time.time() - start_time
    # 计算准确率
    RFC_train_accuracy[i,0]=myRF_clf.score(X_train,Y_train)
    RFC_OOB_accuracy[i,0]=myRF_clf.oob_score_
    RFC_test_accuracy[i,0]=myRF_clf.score(X_test,Y_test)
    RFC_critical_accuracy[i,0]=myRF_clf.score(X_critical,Y_critical)
    if print_flag:
            result = (run_time[i,0], RFC_train_accuracy[i,0], RFC_OOB_accuracy[i,0], RFC_test_accuracy[i,0], RFC_critical_accuracy[i,0])
            print('{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}'.format("time (s)","train score", "OOB estimate","test score", "critical score"))
            print('{0:<15.4f}{1:<15.4f}{2:<15.4f}{3:<15.4f}{4:<15.4f}'.format(*result))
            
# 画出准确率与训练集占比的关系图
plt.figure()
plt.plot(divs,RFC_train_accuracy,'--b^',label='Train')
plt.plot(divs,RFC_test_accuracy,'--r^',label='Test')
plt.plot(divs,RFC_critical_accuracy,'--g^',label='Critical')

plt.xlabel('Test Set Ratio')
plt.ylabel('Accuracy')
lgd=plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig("Ising_RF.pdf",bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.show()