library(glmnet)
library(pROC)
library(doParallel)
registerDoParallel(8)

train <- function(x,y,outfile,N=500){  
  # start
  lambda.min <- NULL
  coeff <- NULL
  name <- NULL
  for(i in 1:N){
    cat('iter:',i,"\n",sep="")
    cvfit <- cv.glmnet(x, y, family = "binomial", nfolds = 10, type.measure = "class",parallel=TRUE)
    lambda.min <- c(lambda.min,cvfit$lambda.min)
    c.best <- coef(cvfit,s='lambda.min')
    coeff <- cbind(coeff,as.vector(c.best))
    name <- rownames(c.best)
  }
  rownames(coeff) <- name
  write.table(as.data.frame(t(coeff)),file=paste('coeff',outfile,sep="_"),sep="\t",row.names = F,quote = F)
  save(x,y,coeff,lambda.min,file=paste('coeff_lambda',outfile,"out.RData",sep="_"))
  # number of nonzero coefficients
  nonzero <- apply(coeff,1 , function(x) length(which(x != 0)))
  # use top 10% nonzero positions
  threshold <- sort(nonzero,decreasing = T)[round(length(nonzero[-1]) * 0.1) + 1]
  index <- which(nonzero / dim(coeff)[2] >= threshold/N)
  mucoeff <- rowMeans(coeff)
  mucoeff[-index] <- 0
  write.table(mucoeff,file=paste('weight',outfile,sep="_"),sep = "\t",row.names = T,col.names = F,quote = F)
  mucoeff
}

## run cv 1000 times and record the lambda.min and coefficients
# create dir
Args <- commandArgs()
famName <- Args[6]
codName <- Args[7]
dirName <- gsub('/','_',famName)
print(dirName)
dir.create(dirName)
setwd(dirName)
system(paste("java -jar ../getPN/GetPosNegPeptide.jar ",famName," ", codName," ../getPN/index.txt ../getPN/new.elm",sep = ""))
# peptide selection
cat('\n# 1. Start Peptide Length Selection\n')
system("python ../2numd-PLS.py")
d  <- read.table("data2.txt",header=T,sep="\t")
dm <- as.matrix(d[,2:ncol(d)])
x <- dm[,1:ncol(dm)-1]
y <- dm[,ncol(dm)]
y[which(y < 0)] <- 0
c1 <- train(x,y,'PLS.txt')
p1 <- 1/(1+exp(-cbind(1,x) %*% c1))
# matrix mutation
cat('\n# 1. Start Matrix Mutation\n')
system("python ../2numd-MM.py")
d2 <- read.table("data.txt",header=T,sep="\t")
dm2 <- as.matrix(d2[,2:ncol(d2)])
x <- dm2[,1:ncol(dm2)-1]
y <- dm2[,ncol(dm2)]
y[which(y < 0)] <- 0
c2 <- train(x,y,'MM.txt')
p2 <- 1/(1+exp(-cbind(1,x) %*% c2))
# plot
png('roc.png')
r1 <- plot.roc(y,p1[,1])
r2 <- plot.roc(y,p2[,1])
lines(r1, type="l", pch=21, col='red', bg="grey")
lines(r2, type="l", pch=21, col='blue', bg="grey")
text(0.4,0.2,paste('AUC',round(r1$auc,3),sep="="),col = 'red')
text(0.4,0.1,paste('AUC',round(r2$auc,3),sep="="),col = 'blue')
dev.off()

