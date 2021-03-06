## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, stride=1)
        nn.init.xavier_normal_(self.conv1.weight)
        self.conv_bn1 = nn.BatchNorm2d(16)
        self.dropout1 = nn.Dropout(0.1)
        
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1)
        nn.init.xavier_normal_(self.conv2.weight)
        self.conv_bn2 = nn.BatchNorm2d(32)
        self.dropout2 = nn.Dropout(0.1)
        
        self.conv3 = nn.Conv2d(32, 48, kernel_size=3, stride=1)
        nn.init.xavier_normal_(self.conv3.weight)
        self.conv_bn3 = nn.BatchNorm2d(48)
        self.dropout3 = nn.Dropout(0.2)
        
        self.conv4 = nn.Conv2d(48, 64, kernel_size=3, stride=1)
        nn.init.xavier_normal_(self.conv4.weight)
        self.conv_bn4 = nn.BatchNorm2d(64)
        self.dropout4 = nn.Dropout(0.2)
        
        self.conv5 = nn.Conv2d(64, 128, kernel_size=3, stride=1)
        nn.init.xavier_normal_(self.conv5.weight)
        self.conv_bn5 = nn.BatchNorm2d(128)
        self.dropout5 = nn.Dropout(0.3)
        
        self.dense1 = nn.Linear(128*5*5, 1024)
        nn.init.xavier_normal_(self.dense1.weight)
        self.dropout6 = nn.Dropout(0.2)
        
        self.dense2 = nn.Linear(1024, 512)
        nn.init.xavier_normal_(self.dense2.weight)
        self.dropout7 = nn.Dropout(0.2)
        
        self.dense3 = nn.Linear(512, 136)
        #nn.init.xavier_normal_(self.dense3.weight)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        #first convolution changes the size from (1, 224, 224) to (16, 220, 220)
        #maxpooling the feature maps changes the size from (16, 220, 220) to (16, 110, 110)

        x = F.max_pool2d(F.relu(self.conv_bn1(self.conv1(x))), 2)
        
        #dropout layer
        x = self.dropout1(x)
        
        #second convolution changes the size from (16, 110, 110) to (32, 108, 108)
        #maxpooling the feature maps changes the size from (32, 108, 108) to (32, 54, 54)
        
        x = F.max_pool2d(F.relu(self.conv_bn2(self.conv2(x))), 2)
        #dropout layer 
        x = self.dropout2(x)
        
        #third convolution changes the size from (32, 54, 54) to (48, 52, 52)
        #maxpooling the feature maps changes the size from (48, 52, 52) to (48, 26, 26)
        
        x = F.max_pool2d(F.relu(self.conv_bn3(self.conv3(x))), 2)
        #dropout layer
        x = self.dropout3(x)
        
        #fourth convolution changes the size from (48, 26, 26) to (64, 24, 24)
        #maxpooling the feature maps changes the size from (64, 24, 24) to (64, 12, 12)
        
        x = F.max_pool2d(F.relu(self.conv_bn4(self.conv4(x))), 2)
        #dropout layer
        x = self.dropout4(x)
        
        #fifth convolution changes the size from (64, 12, 12) to (128, 10, 10)
        #maxpooling the feature maps changes the size from (128, 10, 10) to (128, 5, 5)
        
        x = F.max_pool2d(F.relu(self.conv_bn5(self.conv5(x))), 2)
        #dropout layer
        x = self.dropout5(x)

        
        #flatten
        x = x.view(-1, 128*5*5)
        
        x = F.relu(self.dense1(x))
        #dropout
        x = self.dropout6(x)
        
        x = F.relu(self.dense2(x))
        x = self.dropout7(x)
        
        x = self.dense3(x)
     
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
        