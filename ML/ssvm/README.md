Multiclass Support Vector Machine
========
*The code are mostly followd on http://cs231n.github.io/ and http://www.mowayao.net/post/machine-learning/linear-classification-cs231n*

(1). Loss function
------------
In Multiclass Support Vector Machine, each class contains a weight parameter, the we predict each data under each class by directly using linear calculation, here, we consider the **linear classifier**, namely ***'wTx'***, the decision methond is based the max score among the classes. In order to make sure the classification is right, thsu the loss function considers the mean error the other class score minus the right class score. The small loss means the higher score for right class and low scores for other classes. Thus, mininum the loss function ***'L'*** would help us get the best parameter ***'W'***.
<p align="center">![](https://github.com/ybucla/CodeManage/blob/master/ML/ssvm/lossfunction.jpg)<p />

(2). Gradient of loss function
------------
The loss function only contains the linear function which could be easily mininum by using the Gradient methond. However, as the exists of ***'max()'***, it is not full differential at some points. But we could still use Gradient descent method. Just ignore these undifferential points.
```python
def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).
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
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train):
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    for j in xrange(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:,y[i]] -= X[i]
        dW[:,j] += X[i]

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train
  dW += reg*W
  # Add regularization to the loss.
  loss += 0.5 * reg * np.sum(W * W)

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW
```
*The result is same with svm_loss_vectorized()*

(3). Train using stochastic gradient descent
------------
Train this linear classifier using stochastic gradient descent. Sample batch_size elements from the training data and their corresponding labels to use in this round of gradient descent. Store the data in X_batch and their corresponding labels in y_batch; after sampling X_batch should have shape (dim, batch_size) and y_batch should have shape (batch_size,)
