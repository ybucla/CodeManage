import numpy as np

def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized implementation.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  loss = 0.0
  num_train = X.shape[0]
  num_class = W.shape[1]

  # #############################################################################
  # # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # # Store the loss in loss and the gradient in dW. If you are not careful     #
  # # here, it is easy to run into numeric instability. Don't forget the        #
  # # regularization!                                                           #
  # #############################################################################

  score = X.dot(W).T
  # On rajoute une constant pr ls overflow
  score += - np.max(score , axis=0)
  exp_score = np.exp(score) # matric exponientiel score
  sum_exp_score_col = np.sum(exp_score , axis = 0) # sum des expo score pr chaque column

  loss = np.log(sum_exp_score_col)
  loss = loss - score[y,np.arange(num_train)]
  loss = np.sum(loss) / float(num_train) + 0.5 * reg * np.sum(W*W)

  Grad = exp_score / sum_exp_score_col
  Grad[y,np.arange(num_train)] += -1.0
  dW = Grad.dot(X) / float(num_train) + reg*W.T
  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW.T
