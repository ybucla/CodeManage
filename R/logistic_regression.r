simu.obs <- function(w){
  PN <- 200
  NN <- 1000
  Pmu <- 2
  Nmu <- -2
  pos <- rnorm(PN,Pmu,1)
  num <- sort(sample(1:PN,70,replace = FALSE))
  start <- c(1,num+1)
  end <- c(num,PN)
  datalist <- NULL
  for(i in 1:70){
    p <- pos[start[i]:end[i]]
    n <- rnorm(NN-length(p),Nmu,1)
    d <- c(p,n)
    l <- c()
    for(j in 1:NN){
      prob <- 1/(1+exp(-w[1]*d[j]-w[2]))
      l[j] <- rbinom(1,1,prob)
    }
    # datalist[[i]] <- cbind(d,l,c(rep(1,length(p)),rep(0,length(n))))
    datalist[[i]] <- cbind(d,c(rep(1,length(p)),rep(0,length(n))))
    colnames(datalist[[i]]) <- c('d','l')
  }
  datalist
}

train.glmnet <- function(datalist,nfold=4){
  set.seed(7)
  testi <- sample(1:70,10,replace = F)
  traini <- sample(which(!1:70 %in% testi),70-length(testi))
  newd <- NULL
  for(i in 1:nfold){
    s <- 1 + length(traini)/nfold*(i-1)
    e <- s + 15 -1
    # print(traini[s:e])
    d  <- NULL
    for(j in 1:length(traini[s:e])){
      index <- traini[s:e][j]
      d <- rbind(d,datalist[[index]])
    }
    newd[[i]] <- d 
  }
  # train
  for(i in 1:length(newd)){
    train.d <- newd[[i]]
    cvfit <- cv.glmnet(cbind(train.d[,1],1),train.d[,2],alpha=1,family = "binomial")
    Sn <- 0
    Sp <- 0
    TP <- 0
    TN <- 0
    P <- 0
    N <- 0
    for(j in 1:length(newd)){
      if(i == j) next
      fitted.prob <- predict(cvfit,newx = cbind(newd[[j]][,1],1),type = 'response',s='lambda.min')
      fitted.labe <- ifelse(fitted.prob > 0.5,1,0)
      for(k in 1:nrow(newd[[j]])){
        if(newd[[j]][k,2] == 1 & fitted.labe[k] == 1){ TP <- TP+1}
        if(newd[[j]][k,2] == 0 & fitted.labe[k] == 0){ TN <- TN + 1} 
      }
      P <- P + sum(newd[[j]][,2])
      N <- N + nrow(newd[[j]]) - sum(newd[[j]][,2])
    }
    co <- as.vector(coef(cvfit, s = "lambda.min"))
    cat(i,"\tcoefficients:[",co[1],"\t",co[2],"\t",co[3],"]\tTP=",TP,"\t",P,"\tSn=",TP/P,"\tTN=",TN,"\tSp=",TN/N,"\n",sep="")
    
  }
  # newd
}


train.glm <- function(datalist,nfold=4){
  set.seed(7)
  testi <- sample(1:70,10,replace = F)
  traini <- sample(which(!1:70 %in% testi),70-length(testi))
  newd <- NULL
  for(i in 1:nfold){
    s <- 1 + length(traini)/nfold*(i-1)
    e <- s + 15 -1
    # print(traini[s:e])
    d  <- NULL
    for(j in 1:length(traini[s:e])){
      index <- traini[s:e][j]
      d <- rbind(d,datalist[[index]])
    }
    newd[[i]] <- d 
  }
  # train
  for(i in 1:length(newd)){
    train.d <- newd[[i]]
    r <- glm(l~d,data=as.data.frame(train.d),family='binomial')
    Sn <- 0
    Sp <- 0
    TP <- 0
    TN <- 0
    P <- 0
    N <- 0
    for(j in 1:length(newd)){
      if(i == j) next
      fitted.prob <- predict(r,newdata = as.data.frame(newd[[j]]),type = 'response')
      fitted.labe <- ifelse(fitted.prob > 0.5,1,0)
      for(k in 1:nrow(newd[[j]])){
        if(newd[[j]][k,2] == 1 & fitted.labe[k] == 1){ TP <- TP+1}
        if(newd[[j]][k,2] == 0 & fitted.labe[k] == 0){ TN <- TN + 1} 
      }
      P <- P + sum(newd[[j]][,2])
      N <- N + nrow(newd[[j]]) - sum(newd[[j]][,2])
    }
    cat(i,"\tcoefficients:[",r$coefficients[1]," ",r$coefficients[2],"]\tTP=",TP,"\t",P,"\tSn=",TP/P,"\tTN=",TN,"\tSp=",TN/N,"\n",sep="")

  }
  # newd
}
  
p<-predict(lgst,type='response')
qplot(seq(-2,2,length=length(p)),sort(p),col='predict')
