library("foreach")
library("doParallel")
core <- 6 
c1 <- makeCluster(core)
registerDoParallel(c1)

## simulation observe and inference function
sim_docu <- function(k=10, v=50, n=100){
  wordindex <- diag(1,nrow = v)
  counts <- cbind(1:50, rmultinom(1,n,prob=rep(1/v,v)))
  index <- which(counts[,2] > 0)
  document <- matrix(numeric(length(index)*v),ncol=v)
  for(i in 1:length(index)){
	document[i,index[i]] <- 1
  }
  list(document=document,counts=counts[index,])
}

sim_para <- function(k=10,v=50){
  alpha <- runif(k)
  beta <- matrix(runif(k*v),nrow = k)
  rowSums_beta <- rowSums(beta)
  beta <- apply(beta,2,function(x) x/rowSums_beta)
  list(alpha=alpha,beta=beta)
}

## inference variational parameters gamma, phi
vbinfer <- function(doc,alpha, beta, n.iter=5000, e=0.0001){
  document <- doc$document
  counts <- doc$counts
  N <- nrow(document)
  v <- ncol(document)
  k <- length(alpha)
  if(dim(beta)[1]!= k) stop("ERROR: nrow(beta) should equal length(alpha)!")
  if(dim(beta)[2]!= v) stop("ERROR: ncol(beta) should equal dim(docu)[2]!")
  var_gamma <- numeric(k)
  phi <- matrix(numeric(N*k),nrow = N)
  # initialize variational paras
  for(i in 1:k){
    var_gamma[i] <- alpha[i] + N/k
    for(j in 1:N){
      phi[j,i] <- 1/k
    }
  }
  # update variational paras
  oldll <- 0
  var_iter <- 1
  while(TRUE){
    for(i in 1:N){
      for(j in 1:k){
        wn <- which(document[i,] == 1) # wn index of n word of document
        phi[i,j] <- beta[j,wn]*exp(digamma(var_gamma[j])) # update phi[n,k]
      }
      phi[i,] <- phi[i,]/sum(phi[i,]) # normalize sum(phi[n,]) to 1
    }
	tmp_phi <- apply(phi,2, function(x) x * counts[,2])
    var_gamma <- 50/k + colSums(tmp_phi)
    var_iter <- var_iter + 1
    newll <- likelihood(doc,alpha,beta,var_gamma,phi)
    if(var_iter > n.iter || abs(newll-oldll)<e){
      break
    }
    # cat("Iter",var_iter,":\told=",oldll,"\tnew=",newll,"\n",sep="")
    oldll <- newll
  }
 list(g=var_gamma,p=phi,ll=newll)
}

likelihood <- function(doc,alpha,beta,var_gamma,phi){
  # not exactly the likelihood, but the lower bound of likelihood
  # var_gamma: 1*k; phi: n*k; document: n*v; beta: k*v; alpha: 1*k
  document <- doc$document
  counts <- doc$counts
  diga <- digamma(var_gamma)- digamma(sum(var_gamma))
  third <- 0
  for(n in 1:nrow(phi)){
    for(k in 1:ncol(phi)){
      third <- third + counts[n,2]*phi[n,k]*sum(document[n,]*log(beta[k,]))
    }
  }  
  ll  <- lgamma(sum(alpha))-sum(lgamma(alpha)) + sum((alpha-1)*diga) + sum(phi %*% diga * counts[,2]) + third - lgamma(sum(var_gamma)) + sum(lgamma(var_gamma))-sum((var_gamma-1)*diga) - sum(rowSums(phi*log(phi))*counts[,2])
  ll
}

e.step <- function(corpus,alpha, beta, n.iter=5000, e=0.0001){
  # corpus: (list), set of document
  var_gamma_list <- list()
  phi_list <- list()
  ll_list <- list()
  for(i in 1:length(corpus)){
    document <- corpus[[i]]
    para <- vbinfer(document,alpha,beta)
    var_gamma_list[[i]] <- para$g
    phi_list[[i]] <- para$p
    ll_list[[i]] <- para$ll
  }
  list(g=var_gamma_list,p=phi_list,ll=ll_list)
}

e.step.parallel <- function(corpus,alpha, beta, n.iter=5000, e=0.0001, paral=TRUE){
  # corpus: (list), set of document
  var_gamma_list <- list()
  phi_list <- list()
  ll_list <- list()
  paralist <- NULL
  if(paral == TRUE){
	paralist <- foreach(i=1:length(corpus),.export=c('vbinfer','likelihood')) %dopar% {vbinfer(corpus[[i]],alpha,beta)}
  }else{
	paralist <- foreach(i=1:length(corpus),.export=c('vbinfer','likelihood')) %do% vbinfer(corpus[[i]],alpha,beta)
  }
  
  for(i in 1:length(paralist)) {
	para <- paralist[[i]]
	var_gamma_list[[i]] <- para$g
    phi_list[[i]] <- para$p
    ll_list[[i]] <- para$ll
  }
  list(g=var_gamma_list,p=phi_list,ll=ll_list)
}

m.step <- function(corpus, var_gamma_list, phi_list, ini.alpha, ini.beta, n.iter=5000,e=0.0001){
  # var_gamma_list: M length list with each vector length as K
  # phi_list: M length list with each matrix dim as N * K
  # ini.alpha: 1 * K vector;
  # ini.beta: K * V matrix  
  
  # infer beta
  k <- length(ini.alpha)
  v <- ncol(ini.beta)
  beta <- ini.beta
  for(i in 1:k){
    for(j in 1:v){
	  ele <- 0
      for(d in 1:length(corpus)){
		doc <- corpus[[d]]
        document <- doc$document
		counts <- doc$counts
		phi <- phi_list[[d]]
		if(j %in% counts[,1]){
			n <- which(j == counts[,1])
			Wdnj <- counts[n,2] * phi[n,i]
			ele <- ele + Wdnj
		}
      }
      beta[i,j] <- ele
    }
	beta[i,] <- beta[i,]/sum(beta[i,])
  }
  
  # Newton-Raphson method to get alpha
  # use object function of alpha, derivative, and second derivative function
  alpha <- ini.alpha
  for(i in 1:5000){
    alpha_new <- as.vector(alpha - solve(ddla(alpha)) %*% dla(alpha))
    # cat("#",i,"\n")
    # print(abs(sum(alpha_new-alpha)))
    if(abs(sum(alpha_new-alpha)) < e){
      break
    }
    alpha <- alpha_new
  }  
  # all likelihood
  ll <- 0
  for(i in 1:length(corpus)){
	ll <- ll + likelihood(corpus[[i]], alpha, beta, var_gamma_list[[i]], phi_list[[i]])
  }
  
  list(alpha=alpha,beta=beta,ll=ll)
}

## posterior topic distribution
postz <- function(corpus, alpha, beta){
	p <- c()
	for(i in 1:length(alpha)){		
		logp <- log(gamma(sum(alpha)))-log(gamma(sum(alpha)+1)) + log(gamma(1+alpha[i]))- log(gamma(alpha[i]))
		p[i] <- exp(logp)
	}
	p <- p / sum(p)
	pro <- matrix(numeric(length(corpus) * length(alpha)),length(corpus))
	for(n in 1:length(corpus)){	
		counts <- corpus[[n]]$counts
		for(k in 1:length(alpha)){
			logp <- 0
			for(i in 1:nrow(counts)){
				v <- counts[i,1]
				num <- counts[i,2]
				logp <- logp + num*log(beta[k,v])
			}
			pro[n,k] <- exp(logp + log(p[k]))
		}		
	}
	rs <- rowSums(pro)
	apply(pro,2, function(x) x / rs)
}

## likelihood, derivative and second derivative function of alpha parameter from blei paper
## Likelihood alpha
## alhpa: (vector) 1*K (K: topic number)
## var_gamma_list: (list) length, N (the documents number in a corpus), column number: K (K: topic number)

la <- function(alpha,g_list=var_gamma_list){
  M <- length(g_list)
  K <- length(alpha)
  g <- matrix(numeric(M*K),nrow = M)
  for(i in 1:M){
    for(j in 1:K){
      g[i,j] <- g_list[[i]][j]
    }
  }
  rowSums_g <- rowSums(g)
  g <- apply(g,2, function(x) digamma(x) - digamma(rowSums_g))
  for(i in 1:K){
    g[,i] <- (alpha[i] - 1) * g[,i]
  }
  l <- numeric(M)
  for(i in 1:M){
    l[i] <- lgamma(sum(alpha)) - sum(lgamma(alpha)) + sum(g[i,])
  }
  -sum(l)
}

dla <- function(alpha,g_list=var_gamma_list){
  M <- length(g_list)
  K <- length(alpha)
  g <- matrix(numeric(M*K),nrow = M)
  for(i in 1:M){
    for(j in 1:K){
      g[i,j] <- g_list[[i]][j]
    }
  }
  rowSums_g <- rowSums(g)
  g <- apply(g,2, function(x) digamma(x) - digamma(rowSums_g))
  jacobian <- numeric(K)
  for(i in 1:K){
    jacobian[i] <- M*(digamma(sum(alpha)) - digamma(alpha[i])) + sum(g[,i])
  }
  -jacobian
}

ddla <- function(alpha,g_list=var_gamma_list){
  k <- length(alpha)
  M <- length(g_list)
  hessian <- diag(0,k)
  for(i in 1:k){
    for(j in 1:k){
      if(i == j){
        hessian[i,j] <- 1*M*trigamma(alpha[i]) - M*trigamma(sum(alpha))
      }else{
        hessian[i,j] <- -M*trigamma(sum(alpha))
      }
    }
  }
  hessian
}