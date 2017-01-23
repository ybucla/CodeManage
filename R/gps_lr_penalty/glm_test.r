library(glmnet)
library(pROC)
library(doParallel)
registerDoParallel(8)

#  d  <- read.table("data.txt",header=T,sep="\t")
#  dm <- as.matrix(d[,2:ncol(d)])
#  # rownames(dm) <- d$NAME
#  x <- dm[,1:ncol(dm)-1]
#  y <- dm[,ncol(dm)]
#  y[which(y < 0)] <- 0
#  
#  
#  cvfit_m = cv.glmnet(x, y, family = "binomial", lambda = 10^seq(1, -3, -0.1),nfolds = 10, type.measure = "class")
#  r <- predict(cvfit_m, newx = x, s = "lambda.min", type = "class")
#  p <- predict(cvfit_m, newx = x, s = "lambda.min", type = "response")
#  coef(cvfit_m, s = "lambda.min")


#  # wrong, as the smaller lambda, the higher auc, should not use AUC, use cv error
#  fit <- glmnet(x, y, family = "binomial",lambda = 10^seq(1, -3, -0.1))
#  p <- predict(fit, newx = x, type = "response", s = fit$lambda)
#  aucs <- NULL
#  for(i in 1:ncol(p)){
#    auc <- as.numeric(auc(y,p[,i]))
#    aucs <- c(aucs, auc)
#    cat(i,"\t",auc,"\t",fit$lambda[i],"\n",sep="")
#    plot.roc(y,p[,i])
#  }
#  lambda <- fit$lambda[which.max(aucs)]
#  coef(fit, s = lambda)
#  
#  # run cv 20 times and average the lambda.min
#  for(i in 1:20){
#    lambda <- lambda + cv.glmnet(x, y, family = "binomial", lambda = 10^seq(1, -3, -0.1),nfolds = 10, type.measure = "class")$lambda.min
#  }
#  lambda <- lambda/ 20
#  fit <- glmnet(x, y, family = "binomial",lambda = 10^seq(1, -3, -0.1))
#  p <- predict(fit, newx = x, type = "response", s = lambda)
#  coef(fit, s = lambda)
#  plot.roc(y,p[,1])


## run cv 1000 times and record the lambda.min and coefficients
# peptide selection
d  <- read.table("data2.txt",header=T,sep="\t")
dm <- as.matrix(d[,2:ncol(d)])
x <- dm[,1:ncol(dm)-1]
y <- dm[,ncol(dm)]
y[which(y < 0)] <- 0
# start
lambda.min <- NULL
coeff <- NULL
N <- 1000
for(i in 1:N){
  cat('iter:',i,"\n",sep="")
  cvfit <- cv.glmnet(x, y, family = "binomial", nfolds = 10, type.measure = "class")
  lambda.min <- c(lambda.min,cvfit$lambda.min)
  coeff <- cbind(coeff,as.vector(coef(cvfit,s='lambda.min')))
}
plot(density(lambda.min))
# 直接用lambda.min的均值作为最优lambda来计算
fit <- glmnet(x, y, family = "binomial")
p1 <- predict(fit, newx = x, type = "response", s = mean(lambda.min))
# 选择coeffi非0的次数，如果大于某个阈值，则说明出现概率较大，选择这样的coff的均值作为权重，其他为0
nonzero <- apply(coeff,1 , function(x) length(which(x != 0)))
# threshold_1, p / 测试用
for(i in seq(0.9,0.1,by = -0.05)){
  threshold.1 <- sort(nonzero,decreasing = T)[round(length(nonzero[-1]) * i) + 1]
  index <- which(nonzero / dim(coeff)[2] >= threshold.1/N)
  mucoeff <- rowMeans(coeff)
  mucoeff[-index] <- 0
  p2 <- 1/(1+exp(-cbind(1,x) %*% mucoeff))
  r1 <- plot.roc(y,p1[,1])
  r2 <- plot.roc(y,p2[,1])
  lines(r1, type="l", pch=21, col='red', bg="grey")
  lines(r2, type="l", pch=21, col='blue', bg="grey")
  cat(i,"\t",length(index),"\t",as.numeric(r2$auc),"\n",sep="")
}
# use top 10% nonzero positions
threshold.1 <- sort(nonzero,decreasing = T)[round(length(nonzero[-1]) * 0.1) + 1]
index <- which(nonzero / dim(coeff)[2] >= threshold.1/N)
mucoeff <- rowMeans(coeff)
mucoeff[-index] <- 0
print(mucoeff)
write.table(mucoeff,file='weight.txt',sep = "\t",row.names = F,col.names = F)

# matrix mutation
d2 <- read.table("data.txt",header=T,sep="\t")
dm2 <- as.matrix(d2[,2:ncol(d2)])
x2 <- dm2[,1:ncol(dm2)-1]
y2 <- dm2[,ncol(dm2)]
y2[which(y2 < 0)] <- 0
# start
lambda.min2 <- NULL
coeff2 <- NULL
N <- 1000
for(i in 1:N){
  cat('iter:',i,"\n",sep="")
  cvfit2 <- cv.glmnet(x2, y2, family = "binomial", nfolds = 10, type.measure = "class",parallel=TRUE)
  lambda.min2 <- c(lambda.min2,cvfit2$lambda.min)
  coeff2 <- cbind(coeff2,as.vector(coef(cvfit2,s='lambda.min')))
}
plot(density(lambda.min2))

# -------------------------------------------#
cv <- function(x,y,nfold=10){
  pindex <- sample(which(y == 1))
  nindex <- sample(which(y == 0))

  pfolds <- cut(seq(1,length(pindex)),breaks=nfold,labels=FALSE)
  nfolds <- cut(seq(1,length(nindex)),breaks=nfold,labels=FALSE)
  
  score <- numeric(length(y))
  for(i in 1:nfold){
    ## Segement your data by fold using the which() function 
    ptestIndexes <- pindex[which(pfolds==i,arr.ind=TRUE)]
    ntestIndexes <- nindex[which(nfolds==i,arr.ind=TRUE)]
    testIndexes <- c(ptestIndexes,ntestIndexes)
    # test
    xtest <- x[testIndexes, ]
    ytest <- y[testIndexes]
    # train
    xtrain <- x[-testIndexes, ]
    ytrain <- y[-testIndexes]
    ## Use the test and train data partitions however you desire...
    fitnew <- glmnet(xtrain, ytrain, family = "binomial",lambda = 10^seq(1, -3, -0.1))
    p <- predict(fitnew, newx = xtrain, type = "response", s = fitnew$lambda)
    aucs <- NULL
    for(j in 1:ncol(p)){
      auc <- as.numeric(auc(ytrain,p[,j]))
      aucs <- c(aucs, auc)
      # cat(j,"\t",auc,"\t",fitnew$lambda[j],"\n",sep="")
      plot.roc(ytrain,p[,j])
    }
    lambda <- fit$lambda[which.max(aucs)]
    score[testIndexes] <- predict(fitnew, newx = xtest, type = "response", s = lambda)
  }
  plot.roc(y,score)
}

plotroc <- function(x,y,nfolds=c(4,6,8,10)){
  library(doParallel)
  registerDoParallel(4)
  # nfolds <- c(4,6,8,10)
  colours <- c('red','yellow','blue','green')
  rocs <- list()
  for(i in 1:length(nfolds)){
    print(nfolds[i])
    cvfit = cv.glmnet(x, y, family = "binomial", nfolds = nfolds[i], type.measure = "class",parallel=TRUE)
    p <- predict(cvfit, newx = x, s = "lambda.min", type = "response")
    roc <- plot.roc(y,p[,1],type="n")
    rocs[[i]] <- roc
  }
  for(i in 1:length(rocs)){
    lines(rocs[[i]], type="l", pch=21, col=colours[i], bg="grey")
  }
}



# kmeans
for(i in 1:ncol(c)){
  f <- kmeans(c, i)
  ratio <- f$betweenss/f$totss
  cat(i,ratio,"\n",sep="\t")
}

# cor.test
for(i in 1:ncol(c)){
  f <- cor.test(x[,i],y)
  print(f)
}

m2 <- svm(x,as.factor(y),kernel = 'sigmoid',probability = T)
table(predict(m2,x),y)
p <- predict(m2,x,probability = T)
plot.roc(y,attributes(p)$probabilities[,1])


## bagging / bootstrap averaging
pi <- sample(which(y == 1),round(length(which(y == 1)) * 0.9))
ni <- sample(which(y == 0),length(pi))

xnew <- x[c(pi,ni),]
ynew <- y[c(pi,ni)]
cvfit = cv.glmnet(xnew, ynew, family = "binomial",nfolds = 10, type.measure = "class")
coef(cvfit, s = "lambda.min")
