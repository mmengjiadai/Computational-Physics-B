import numpy as np
import pickle, os
from urllib.request import urlopen
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import time
import warnings
import seaborn as sns

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

# 按比例划分
train_to_test_ratio=0.9
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=train_to_test_ratio,test_size=1.0-train_to_test_ratio)
print('X_train shape:', X_train.shape)
print('Y_train shape:', Y_train.shape)
print()
print(X_train.shape[0], 'train samples')
print(X_critical.shape[0], 'critical samples')
print(X_test.shape[0], 'test samples')

# 叶子上最小样本数
split_range = [2, 3000, 7000, 10000]
r = len(split_range)
# 树木棵树
min_estimators = 10
max_estimators = 101
n_estimator_range = np.arange(min_estimators, max_estimators, 10)
m = len(n_estimator_range)
# 树木深度
max_depth_range = [3, 5, 8, 15, 25, 30, None]
n = len(max_depth_range)

# 分配内存
RFC_OOB_accuracy=np.zeros((r,m,n))
RFC_train_accuracy=np.zeros((r,m,n))
RFC_test_accuracy=np.zeros((r,m,n))
RFC_critical_accuracy=np.zeros((r,m,n))
run_time=np.zeros((r,m,n))

print_flag=True

classifer = RandomForestClassifier
for i, leaf_size in enumerate(split_range):
    # Define Random Forest Classifier
    myRF_clf = classifer(
        n_estimators=min_estimators,
        max_depth=None, 
        min_samples_split=leaf_size, # minimum number of sample per leaf
        oob_score=True,
        random_state=0,
        warm_start=True # this ensures that you add estimators without retraining everything
    )
    for j, n_estimator in enumerate(n_estimator_range):       
        for k, max_depth in enumerate(max_depth_range):
            if max_depth == None:
                print('leaf_size: %i, n_estimators: %i, max_depth: None '%(leaf_size, n_estimator))        
            else:
                print('leaf_size: %i, n_estimators: %i, max_depth: %i'%(leaf_size, n_estimator,max_depth))        
            start_time = time.time()
            myRF_clf.set_params(n_estimators=n_estimator)
            myRF_clf.fit(X_train, Y_train)
            run_time[i,j,k] = time.time() - start_time
    
        # check accuracy
            RFC_train_accuracy[i,j,k]=myRF_clf.score(X_train,Y_train)
            RFC_OOB_accuracy[i,j,k]=myRF_clf.oob_score_
            RFC_test_accuracy[i,j,k]=myRF_clf.score(X_test,Y_test)
            RFC_critical_accuracy[i,j,k]=myRF_clf.score(X_critical,Y_critical)
            if print_flag:
                result = (run_time[i,j,k], RFC_train_accuracy[i,j,k], RFC_OOB_accuracy[i,j,k], RFC_test_accuracy[i,j,k], RFC_critical_accuracy[i,j,k])
                print('{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}'.format("time (s)","train score", "OOB estimate","test score", "critical score"))
                print('{0:<15.4f}{1:<15.4f}{2:<15.4f}{3:<15.4f}{4:<15.4f}'.format(*result))
# In[]                
for i, leaf_size in enumerate(split_range):
    ax_train = sns.heatmap(RFC_train_accuracy[i], xticklabels=max_depth_range, yticklabels=n_estimator_range[::-1])
    ax_train.set_title('train accuracy: leaf size = %i'%leaf_size)
    ax_train.set_xlabel('max_depth')
    ax_train.set_ylabel('n_estimator')
    plt.show()
    ax_test = sns.heatmap(RFC_test_accuracy[i], xticklabels=max_depth_range, yticklabels=n_estimator_range[::-1])
    ax_test.set_title('test accuracy: leaf size = %i'%leaf_size)
    ax_test.set_xlabel('max_depth')
    ax_test.set_ylabel('n_estimator')
    plt.show()
    ax_critical = sns.heatmap(RFC_critical_accuracy[i], xticklabels=max_depth_range, yticklabels=n_estimator_range[::-1])
    ax_critical.set_title('critical accuracy: leaf size = %i'%leaf_size)
    ax_critical.set_xlabel('max_depth')
    ax_critical.set_ylabel('n_estimator')
    plt.show()

# In[]
# 寻找最佳超参数
#print(RFC_OOB_accuracy)
maximum = np.max(RFC_OOB_accuracy)    
for i in range(r):
    for j in range(m):
        for k in range(n):
            if RFC_OOB_accuracy[i][j][k] == maximum:
                if max_depth_range[k] == None:
                    print('leaf_size: %i, n_estimators: %i, max_depth: None '%(split_range[i], n_estimator_range[j]))        
                else:
                    print('leaf_size: %i, n_estimators: %i, max_depth: %i'%(split_range[i], n_estimator_range[j], max_depth_range[k]))        
