# penalty logistic regression and parameter selection using cross validation

from sklearn.datasets import make_classification
x, y = make_classification(n_samples=10000, random_state=133)

# 直接用惩罚系数C=0.01拟合
lr = LogisticRegression(penalty='l1', solver='liblinear', C=0.01)
lr.fit(x, y)

# cv训练出最优惩罚系数为C=0.01，并用训练好的C重新拟合refit
lr_cv = LogisticRegressionCV(penalty='l1', solver='liblinear', Cs=[0.01,0.001],
refit=True)
lr_cv.fit(x, y)

# 惩罚系数一样，非0个数一样
assert lr.C == lr_cv.C_
assert np.count_nonzero(lr.coef_) == np.count_nonzero(lr_cv.coef_)

# coef非常接近 （）注意确实不一样
print lr.coef_
print lr_cv.coef_

# 手动检验predict原始数据结果
score = np.dot(x,lr_cv.coef_.ravel())+lr_cv.intercept_
prob = 1 / (1 + np.exp(-score))
predict_prob = lr_cv.predict_proba(x)[:,1]
# predict_prob == prob
