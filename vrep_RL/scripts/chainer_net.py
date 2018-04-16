import numpy as np
from chainer import functions as F
from chainer import links as L
from chainer import Chain
from chainer import optimizers
from chainer import  Link
import chainer

class DepthwiseConv(Link):
    def __init__(self, n_input, n_output):
        super().__init__()
        with self.init_scope():
            self.W  = chainer.Parameter(initializer=chainer.initializers.GlorotNormal(),
                                        shape=(n_input, n_output))
            self.b = chainer.Parameter(initializer=chainer.initializers.Constant(),
                                      shape=(n_output))
    
    def __call__(self,  x,  stride=1, return_f_map=False):
        if return_f_map:
            return F.depthwise_convolution_2d(x, self.W, self.b, stride=stride),  self.W
        else :
            return F.depthwise_convolution_2d(x, self.W, self.b, stride=stride)



class Model(Chain):
    def __init__(self, out_size):
        super().__init__()
        with self.init_scope():
            self.conv1_1 =DepthwiseConv(in_channels=1, ksize=3, stride=2,
                                   out_channel=32)
            self.bn1_1 = L.BatchNormalization()
            self.conv1_2 = L.Convolution2D(in_channels=32, ksize=1, stride=1,
                                   out_channel=32)
            self.bn1_2 = L.BatchNormalization()
            
            
            self.conv2_1 = DepthwiseConv(in_channels=32, ksize=3, stride=2,
                                   out_channel=64)
            self.bn2_1 = L.BatchNormalization()
            self.conv2_2 = L.Convolution2D(in_channels=64, ksize=1, stride=1,
                                   out_channel=64)
            self.bn2_2 = L.BatchNormalization()
            
            
            self.conv3_1 =DepthwiseConv(in_channels=64, ksize=3, stride=2,
                                   out_channel=128)
            self.bn3_1 = L.BatchNormalization()
            self.conv3_2 = L.Convolution2D(in_channels=128, ksize=1, stride=1,
                                   out_channel=128)
            self.bn3_2 = L.BatchNormalization()
            
            
            self.conv4_1 = DepthwiseConv(in_channels=128, ksize=3, stride=2,
                                   out_channel=256)
            self.bn4_1 = L.BatchNormalization()
            self.conv4_2 = L.Convolution2D(in_channels=256, ksize=1, stride=1,
                                   out_channel=256)
            self.bn4_2 = L.BatchNormalization()
            
            self.fc1 = L.Linear(in_size=256, out_size=100)
            self.fc2 = L.Linear(in_size=100, out_size=out_size)
    
    def __call__(self, x):
        h1 = F.relu(self.bn1_1(self.conv1_1(x)))
        h1 = F.relu(self.bn1_2(self.conv1_2(h1)))
        
        h2 = F.relu(self.bn2_1(self.conv2_1(h1)))
        h2 = F.relu(self.bn2_2(self.conv2_2(h2)))
        
        h3 = F.relu(self.bn3_1(self.conv3_1(h2)))
        h3 = F.relu(self.bn3_2(self.conv3_2(h3)))
        
        h4 = F.relu(self.bn4_1(self.conv4_1(h3)))
        h4 = F.relu(self.bn4_2(self.conv4_2(h4)))
        
        h5 = F.average_pooling_2d(h4)
        
        h6 = F.relu(self.fc1(h5))
        h7 = self.fc2(h6)
