#Randomly shuffle the data
yourData<-yourData[sample(nrow(yourData)),]

#Create 10 equally size folds
folds <- cut(seq(1,nrow(yourData)),breaks=10,labels=FALSE)

#Perform 10 fold cross validation
for(i in 1:10){
    #Segement your data by fold using the which() function 
    testIndexes <- which(folds==i,arr.ind=TRUE)
    testData <- yourData[testIndexes, ]
    trainData <- yourData[-testIndexes, ]
    #Use the test and train data partitions however you desire...
}


# split positive and negative separetly
# x: data, y: label
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
  #Use the test and train data partitions however you desire...
}
