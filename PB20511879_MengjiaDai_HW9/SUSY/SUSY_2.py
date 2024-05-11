from __future__ import print_function, division
import os,sys
import numpy as np
import pandas as pd
import torch # pytorch package, allows using GPUs
import torch.nn as nn # construct NN
import torch.nn.functional as F  # implements forward and backward definitions of an autograd operation
import torch.optim as optim  # different update rules such as SGD, Nesterov-SGD, Adam, RMSProp, etc
import matplotlib.pyplot as plt
import argparse # handles arguments
import sys; sys.argv=['']; del sys # required to use parser in jupyter notebooks
# fix seed
seed=17
np.random.seed(seed)
torch.manual_seed(seed)

from torchvision import datasets # load data

class SUSY_Dataset(torch.utils.data.Dataset):
    """SUSY pytorch dataset."""

    def __init__(self, data_file, root_dir, dataset_size, train=True, transform=None, high_level_feats=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            train (bool, optional): If set to `True` load training data.
            transform (callable, optional): Optional transform to be applied on a sample.
            high_level_festures (bool, optional): If set to `True`, working with high-level features only.
                                        If set to `False`, working with low-level features only.
                                        Default is `None`: working with all features
        """


        features=['SUSY','lepton 1 pT', 'lepton 1 eta', 'lepton 1 phi', 'lepton 2 pT', 'lepton 2 eta', 'lepton 2 phi',
                'missing energy magnitude', 'missing energy phi', 'MET_rel', 'axial MET', 'M_R', 'M_TR_2', 'R', 'MT2',
                'S_R', 'M_Delta_R', 'dPhi_r_b', 'cos(theta_r1)']

        low_features=['lepton 1 pT', 'lepton 1 eta', 'lepton 1 phi', 'lepton 2 pT', 'lepton 2 eta', 'lepton 2 phi',
                'missing energy magnitude', 'missing energy phi']

        high_features=['MET_rel', 'axial MET', 'M_R', 'M_TR_2', 'R', 'MT2','S_R', 'M_Delta_R', 'dPhi_r_b', 'cos(theta_r1)']


        #Number of datapoints to work with
        df = pd.read_csv(root_dir+data_file, header=None,nrows=dataset_size,engine='python')
        df.columns=features
        Y = df['SUSY']
        X = df[[col for col in df.columns if col!="SUSY"]]

        # set training and test data size
        train_size=int(0.8*dataset_size)
        self.train=train

        if self.train:
            X=X[:train_size]
            Y=Y[:train_size]
            print("Training on {} examples".format(train_size))
        else:
            X=X[train_size:]
            Y=Y[train_size:]
            print("Testing on {} examples".format(dataset_size-train_size))


        self.root_dir = root_dir
        self.transform = transform

        # make datasets using only the 8 low-level features and 10 high-level features
        if high_level_feats is None:
            self.data=(X.values.astype(np.float32),Y.values.astype(int))
            print("Using both high and low level features")
        elif high_level_feats is True:
            self.data=(X[high_features].values.astype(np.float32),Y.values.astype(int))
            print("Using high-level features only.")
        elif high_level_feats is False:
            self.data=(X[low_features].values.astype(np.float32),Y.values.astype(int))
            print("Using low-level features only.")


    # override __len__ and __getitem__ of the Dataset() class

    def __len__(self):
        return len(self.data[1])

    def __getitem__(self, idx):

        sample=(self.data[0][idx,...],self.data[1][idx])

        if self.transform:
            sample=self.transform(sample)

        return sample

def load_data(args):

    data_file='\SUSY.csv'
    root_dir=r'D:\PYTHON\pytorch\HW9_PB20511879_MengjiaDai\SUSY\SUSY.csv'

    kwargs = {} # CUDA arguments, if enabled
    # load and noralise train and test data
    train_loader = torch.utils.data.DataLoader(
        SUSY_Dataset(data_file,root_dir,args.dataset_size,train=True,high_level_feats=args.high_level_feats),
        batch_size=args.batch_size, shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(
        SUSY_Dataset(data_file,root_dir,args.dataset_size,train=False,high_level_feats=args.high_level_feats),
        batch_size=args.test_batch_size, shuffle=True, **kwargs)

    return train_loader, test_loader


class model(nn.Module):
    def __init__(self,high_level_feats=None,layer=1):
        # inherit attributes and methods of nn.Module
        super(model, self).__init__()
        self.layer = layer
        # an affine operation: y = Wx + b
        if high_level_feats is None:
            self.fc1 = nn.Linear(18, 100) # all features
        elif high_level_feats:
            self.fc1 = nn.Linear(10, 200) # low-level only
        else:
            self.fc1 = nn.Linear(8, 200) # high-level only


        self.batchnorm1=nn.BatchNorm1d(100, eps=1e-05, momentum=0.1)
        self.batchnorm2=nn.BatchNorm1d(100, eps=1e-05, momentum=0.1)

        self.fc2 = nn.Linear(100, 100) # see forward function for dimensions
        self.fc3 = nn.Linear(100, 2)

    def forward(self, x):
        '''Defines the feed-forward function for the NN.

        A backward function is automatically defined using `torch.autograd`

        Parameters
        ----------
        x : autograd.Tensor
            input data

        Returns
        -------
        autograd.Tensor
            output layer of NN

        '''
        lay = self.layer-1
        # apply rectified linear unit
        x = F.relu(self.fc1(x))
        x=self.batchnorm1(x)
        #x = F.dropout(x, training=self.training)
        for i in range(lay):
            x = F.relu(self.fc2(x))
            x = self.batchnorm1(x)

        # apply rectified linear unit
        #x = F.relu(self.fc2(x))
        # apply dropout
        #x=self.batchnorm2(x)
        #x = F.dropout(x, training=self.training)


        # apply affine operation fc2
        x = self.fc3(x)
        # soft-max layer
        x = F.log_softmax(x,dim=1)

        return x


def evaluate_model(args, train_loader, test_loader):
    # create model
    DNN = model(high_level_feats=args.high_level_feats,layer=args.num_layer)
    # negative log-likelihood (nll) loss for training: takes class labels NOT one-hot vectors!
    criterion = F.nll_loss
    # define SGD optimizer
    optimizer = optim.SGD(DNN.parameters(), lr=args.lr, momentum=args.momentum)

    # optimizer = optim.Adam(DNN.parameters(), lr=0.001, betas=(0.9, 0.999))

    ################################################

    def train(epoch):
        '''Trains a NN using minibatches.

        Parameters
        ----------
        epoch : int
            Training epoch number.

        '''

        # set model to training mode (affects Dropout and BatchNorm)
        DNN.train()
        # loop over training data
        for batch_idx, (data, label) in enumerate(train_loader):
            # zero gradient buffers
            optimizer.zero_grad()
            # compute output of final layer: forward step
            output = DNN(data)
            label = label.type(torch.LongTensor)
            # compute loss
            loss = criterion(output, label)
            # run backprop: backward step
            loss.backward()
            # update weigths of NN
            optimizer.step()

            # print loss at current epoch
            if batch_idx % args.log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                           100. * batch_idx / len(train_loader), loss.item()))

        return loss.item()

    ################################################

    def test():
        '''Tests NN performance.

        '''

        # evaluate model
        DNN.eval()

        test_loss = 0  # loss function on test data
        correct = 0  # number of correct predictions
        # loop over test data
        for data, label in test_loader:
            # compute model prediction softmax probability
            output = DNN(data)
            label = label.type(torch.LongTensor)
            # compute test loss
            test_loss += criterion(output, label, size_average=False).item()  # sum up batch loss
            # find most likely prediction
            pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
            # update number of correct predictions
            correct += pred.eq(label.data.view_as(pred)).cpu().sum().item()

        # print test loss
        test_loss /= len(test_loader.dataset)

        print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.3f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

        return test_loss, correct / len(test_loader.dataset)

    ################################################

    train_loss = np.zeros((args.epochs,))
    test_loss = np.zeros_like(train_loss)
    test_accuracy = np.zeros_like(train_loss)

    epochs = range(1, args.epochs + 1)
    for epoch in epochs:
        train_loss[epoch - 1] = train(epoch)
        test_loss[epoch - 1], test_accuracy[epoch - 1] = test()

    return test_loss[-1], test_accuracy[-1]

def grid_search(args):


    # perform grid search over learnign rate and number of hidden neurons
    dataset_size=1000#np.logspace(2,5,4).astype('int')
    learning_rate=0.01
    num_layers = [1,2,3,4,5]

    # pre-alocate data
    test_loss=np.zeros(len(num_layers),dtype=np.float64)
    test_accuracy=np.zeros_like(test_loss)

    # do grid search
    for i, num_layer in enumerate(num_layers):
        # upate data set size parameters
        args.dataset_size = dataset_size
        args.batch_size = int(0.01*dataset_size)
        args.num_layer = num_layer
        # load data
        train_loader, test_loader = load_data(args)
        args.lr = learning_rate
        test_loss[i],test_accuracy[i] = evaluate_model(args, train_loader,test_loader)


    plot_data_2(num_layers,test_accuracy)


def plot_data_1(dataset_sizes, test_accuracy):
    plt.figure()
    plt.plot(dataset_sizes, test_accuracy, '--b^', label='Accuracy')
    plt.xlabel('Train Data Size')
    plt.ylabel('Test Accuracy')
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def plot_data_2(num_layers, test_accuracy):
    plt.figure()
    plt.plot(num_layers, test_accuracy, '--b^', label='Accuracy')
    plt.xlabel('Number of Hidden Layers')
    plt.ylabel('Test Accuracy')
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def plot_data(x, y, data):
    # plot results
    fontsize = 16

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(data, interpolation='nearest', vmin=0, vmax=1)

    cbar = fig.colorbar(cax)
    cbar.ax.set_ylabel('accuracy (%)', rotation=90, fontsize=fontsize)
    cbar.set_ticks([0, .2, .4, 0.6, 0.8, 1.0])
    cbar.set_ticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

    # put text on matrix elements
    for i, x_val in enumerate(np.arange(len(x))):
        for j, y_val in enumerate(np.arange(len(y))):
            c = "${0:.1f}\\%$".format(100 * data[j, i])
            ax.text(x_val, y_val, c, va='center', ha='center')

    # convert axis vaues to to string labels
    x = [str(i) for i in x]
    y = [str(i) for i in y]

    ax.set_xticklabels([''] + x)
    ax.set_yticklabels([''] + y)

    ax.set_xlabel('$\\mathrm{learning\\ rate}$', fontsize=fontsize)
    ax.set_ylabel('$\\mathrm{hidden\\ neurons}$', fontsize=fontsize)

    plt.tight_layout()

    plt.show()


# Training settings
parser = argparse.ArgumentParser(description='PyTorch SUSY Example')
parser.add_argument('--dataset_size', type=int, default=100000, metavar='DS',
                help='size of data set (default: 100000)')
parser.add_argument('--high_level_feats', type=bool, default=None, metavar='HLF',
                help='toggles high level features (default: None)')
parser.add_argument('--batch-size', type=int, default=100, metavar='N',
                help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=10, metavar='N',
                help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.05, metavar='LR',
                help='learning rate (default: 0.02)')
parser.add_argument('--momentum', type=float, default=0.8, metavar='M',
                help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                help='disables CUDA training')
parser.add_argument('--seed', type=int, default=2, metavar='S',
                help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                help='how many batches to wait before logging training status')
parser.add_argument('--num_layer', type=int, default=1, metavar='N',
                help='number of hidden layers')
args = parser.parse_args()

# set seed of random number generator
torch.manual_seed(args.seed)

grid_search(args)

