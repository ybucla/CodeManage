import numpy as np

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, vectorized implementation., naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero
  # compute the loss and the gradient
  N, D = X.shape
  M = W.shape[1]

  score = X.dot(W).T
  score -= np.max(score, axis=0)
  f = np.exp(score.T)
  p = (f.T / f.sum(1)).T
  loss = -np.log(p)[range(N),y].sum()

  p[range(N),y] -= 1.0
  for j in range(M):
      dW[:,j] = (X.T * p[:,j]).sum(1)
#      dW[:,j] = (p[range(N),j] - Y[:,j]).reshape((1,N)).dot(X)

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  
  loss = loss / N + 0.5 * reg * np.sum(W*W)
  dW = dW / N + reg * W

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW
