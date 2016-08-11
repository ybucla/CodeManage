data <- read.table("data/parse.HL.out",header=FALSE,sep="\t")
## remove kinase with less than 10 sites
orikina <- unique(data$V7)
for(i in 1:length(orikina)){
  index <- which(data$V7 == orikina[i])
  if(length(index) < 10) data <- data[-index,]
}
## generate corpus
corpus <- NULL
allsite <- paste0(data$V1,'_',data$V3,data$V2)
site <- unique(allsite)
kinase <- unique(data$V7)
dataMatrix <- NULL
for(i in 1:nrow(data)){
  site_index <- which(site == allsite[i])
  kina_index <- which(kinase == data$V7[i])
  counts <- data$V5[i]
  dataMatrix <- rbind(dataMatrix,c(kina_index,site_index,counts))
}

M <- length(kinase)
for(i in 1:M){
  index <- which(dataMatrix[,1]==i)
  d <- dataMatrix[index,]
  document <- matrix(numeric(nrow(d)*length(site)),nrow = nrow(d))
  counts <- d[,2:3]
  for(j in 1:nrow(d)){
    document[j,d[j,2]] <- 1
  }
  corpus[[i]] <- list(document=document,counts=counts)
}

## start runing ##
source("lda_func.r")
## parameters
k <- 10
v <- length(site)
## simulate initial parameters
sim_p <- sim_para(k,v)
ini.alpha <- sim_p$alpha
ini.beta <- sim_p$beta
## inference alpha, beta
alpha <- NULL
beta <- NULL
ll <- 0
for(i in 1:2){
  if(is.null(alpha)) alpha <- ini.alpha
  if(is.null(beta)) beta <- ini.beta
  # print(alpha)
  # e-step
  pg <- e.step(corpus, alpha, beta)
  var_gamma_list <- pg$g
  phi_list <- pg$p
  # m-step
  abl <- m.step(corpus, var_gamma_list, phi_list, alpha, beta)
  alpha <- abl$alpha
  beta <- abl$beta
  new_ll <- abl$ll
  cat("# iter:",i,"\tll:",ll,"\tnew_ll:",new_ll,"\n")
  if(abs(new_ll-ll) < 0.0001) break
  ll <- new_ll
}

save(alpha,file="alpha.RData")
save(beta,file="beta.RData")
save(corpus,file="corpus.RData")
