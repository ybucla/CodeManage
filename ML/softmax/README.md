Softmax Machine for Multiclass
========
*The code are mostly followd on http://cs231n.github.io/ and http://www.mowayao.net/post/machine-learning/linear-classification-cs231n*. The codes here are only for learning. Please contact me if it is should be authorized first or any question: hust.wangyb@gmail.com.

(1). Loss function
------------
In Softmax Machine for Multiclass, each class contains a weight parameter, the we predict each data under each class by directly using linear calculation, here, we consider the **linear classifier**, namely ***'wTx'***, the decision methond is based the max score among the classes.
<p align="center">![](https://github.com/ybucla/CodeManage/blob/master/ML/softmax/softmax-loss.jpg)<p />

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
Train this linear classifier using stochastic gradient descent. Sample batch_size elements from the training data and their corresponding labels to use in this round of gradient descent. Store the data in X_batch and their corresponding labels in y_batch; after sampling X_batch should have shape (dim, batch_size) and y_batch should have shape (batch_size,).<br />
codes in *linear_classifier.py*
```python
def train(self, X, y, learning_rate=1e-3, reg=1e-5, num_iters=100,
          batch_size=200, verbose=False):
  """
  Train this linear classifier using stochastic gradient descent.

  Inputs:
  - X: A numpy array of shape (N, D) containing training data; there are N
    training samples each of dimension D.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c
    means that X[i] has label 0 <= c < C for C classes.
  - learning_rate: (float) learning rate for optimization.
  - reg: (float) regularization strength.
  - num_iters: (integer) number of steps to take when optimizing
  - batch_size: (integer) number of training examples to use at each step.
  - verbose: (boolean) If true, print progress during optimization.

  Outputs:
  A list containing the value of the loss function at each training iteration.
  """
  num_train, dim = X.shape
  num_classes = np.max(y) + 1 # assume y takes values 0...K-1 where K is number of classes
  if self.W is None:
    # lazily initialize W
    self.W = 0.001 * np.random.randn(dim, num_classes)

  # Run stochastic gradient descent to optimize W
  loss_history = []
  for it in xrange(num_iters):
    X_batch = None
    y_batch = None

    #########################################################################
    # TODO:                                                                 #
    # Sample batch_size elements from the training data and their           #
    # corresponding labels to use in this round of gradient descent.        #
    # Store the data in X_batch and their corresponding labels in           #
    # y_batch; after sampling X_batch should have shape (dim, batch_size)   #
    # and y_batch should have shape (batch_size,)                           #
    #                                                                       #
    # Hint: Use np.random.choice to generate indices. Sampling with         #
    # replacement is faster than sampling without replacement.              #
    #########################################################################
    index = np.random.randint(0, num_train, size=batch_size)
    X_batch = X[index]
    y_batch = y[index]
    #########################################################################
    #                       END OF YOUR CODE                                #
    #########################################################################

    # evaluate loss and gradient
    loss, grad = self.loss(X_batch, y_batch, reg)
    loss_history.append(loss)

    # perform parameter update
    #########################################################################
    # TODO:                                                                 #
    # Update the weights using the gradient and the learning rate.          #
    #########################################################################
    self.W -= grad * learning_rate
    #########################################################################
    #                       END OF YOUR CODE                                #
    #########################################################################

    if verbose and it % 100 == 0:
      print 'iteration %d / %d: loss %f' % (it, num_iters, loss)

  return loss_history
```

(4). prediction
the class with highest score is predicted out.
```python
def predict(self, X):
  """
  Use the trained weights of this linear classifier to predict labels for
  data points.

  Inputs:
  - X: N x D array of training data. Each column is a D-dimensional point.

  Returns:
  - y_pred: Predicted labels for the data in X. y_pred is a 1-dimensional
    array of length N, and each element is an integer giving the predicted
    class.
  """
  y_pred = np.zeros(X.shape[0])
  ###########################################################################
  # TODO:                                                                   #
  # Implement this method. Store the predicted labels in y_pred.            #
  ###########################################################################
  scores = X.dot(self.W)
  y_pred = np.argmax(scores, axis=1)
  ###########################################################################
  #                           END OF YOUR CODE                              #
  ###########################################################################
  return y_pred
```
