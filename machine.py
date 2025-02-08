# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:33:37 2024

@author: Brandon
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def init_params():
  W1 = np.random.rand(5, 784) - 0.5 # this generates random weights for layer 1 in the range of -0.5 to 0.5
  b1 = np.random.rand(5,1) - 0.5 # this generates random biases for layer 1 in the range of -0.5 to 0.5

  # the same is done for layer 2:
  W2 = np.random.rand(10, 5) - 0.5
  b2 = np.random.rand(10, 1) -0.5
  return W1, b1, W2, b2

def ReLU(Z):
  return np.maximum(0,Z) # this goes through elementwise each Z and returns Z if larger than 0, and 0 if less than 0.

def softmax(Z):
  A = np.exp(Z) / sum(np.exp(Z))
  return A

def deriv_ReLU(Z):
  return Z>0

def forward_prop(W1, b1, W2, b2, X):
  Z1 = W1.dot(X) + b1 # calculating the unactivated first layer.
  A1 = ReLU(Z1) # activating layer 1
  Z2 = W2.dot(A1) + b2
  A2 = softmax(Z2) # activating layer 2
  return Z1, A1, Z2, A2

def one_hot(Y): # takes the numerical labels and changes it to a matrix that the NN can compare to for the loss fxn.
  one_hot_Y = np.zeros((Y.size, Y.max() +1))
  one_hot_Y[np.arange(Y.size), Y] = 1
  one_hot_Y = one_hot_Y.T
  return one_hot_Y


def back_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
  m = Y.size
  one_hot_Y = one_hot(Y)
  dZ2 = A2 - one_hot_Y
  dW2 = (1/m)*dZ2.dot(A1.T)
  db2 = 1 / m * np.sum(dZ2, axis=1).reshape(-1, 1) #edited
  dZ1 = W2.T.dot(dZ2) * deriv_ReLU(Z1)
  dW1 = (1/m) * dZ1.dot(X.T)
  db1 = 1 / m * np.sum(dZ1, axis=1).reshape(-1, 1) #edited
  return dW1, db1, dW2, db2

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
  W1 = W1 - alpha*dW1
  b1 = b1 - alpha*db1
  W2 = W2 - alpha*dW2
  b2 = b2 - alpha*db2
  return W1, b1, W2, b2

def get_predictions(A2):
  return np.argmax(A2,0)

def get_accuracy(predictions, Y):
  #print(predictions, Y)
  return np.sum(predictions == Y) / Y.size

def gradient_descent(X, Y, iterations, alpha):
  W1, b1, W2, b2 = init_params()
  for i in range(iterations):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
    W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
    if (i%10 == 0):
      print("Iteration: ", i)
      predictions = get_predictions(A2)
      print("Accuracy: ", get_accuracy(predictions, Y))
  print("Iteration: ", i)
  predictions = get_predictions(A2)
  print("Accuracy: ", get_accuracy(predictions, Y))
  print("W1: ", W1.min(), W1.max(), W1.mean())
  print("b1:", b1.min(), b1.max(), b1.mean())
  print("W2:", W2.min(), W2.max(), W2.mean())
  print("b2:", b2.min(), b2.max(), b2.mean())
  print("Z1: ", Z1.min(), Z1.max(), Z1.mean())
  print("Z2: ", Z2.min(), Z2.max(), Z2.mean())
  return W1, b1, W2, b2

def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
    label = Y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)

    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

data = pd.read_csv('MNIST_train.csv')
data = np.array(data) # make into np array so more operations are available
m, n = data.shape # m is the number of images, and n is the number of features (pixels) + 1 bc of label column
np.random.shuffle(data)

data_dev = data[0:1000].T # transposes the data from 0-1000 examples and saves in data_dev
Y_dev = data_dev[0] # first column of the transposed data, indicates pixel/feature #
X_dev = data_dev[1:n] # every column after the first. Each column holds the 784 grayscale values for that image
X_dev = X_dev / 255.

data_train = data[1000:m].T  # all the examples after 1000 will be used for training.
Y_train = data_train[0] #labels
X_train = data_train[1:n] # greyscale values
X_train = X_train/255.
_,m_train = X_train.shape
X_train[:, 0].shape
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 5000 , 0.4)
    
print("Testing Images 0-20")
for i in range(0,21,1):
  test_prediction(i, W1, b1, W2, b2)
dev_predictions = make_predictions(X_dev,W1,b1,W2,b2)
get_accuracy(dev_predictions, Y_dev)