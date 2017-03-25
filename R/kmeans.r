n = 1000
kk = 10    
x1 = runif(kk)
y1 = runif(kk)
z1 = runif(kk)    
x4 = sample(x1,length(x1))
y4 = sample(y1,length(y1)) 
randObs <- function()
{
  ix = sample( 1:length(x4), 1 )
  iy = sample( 1:length(y4), 1 )
  rx = rnorm( 1, x4[ix], runif(1)/8 )
  ry = rnorm( 1, y4[ix], runif(1)/8 )
  return( c(rx,ry) )
}  
x = c()
y = c()
for ( k in 1:n )
{
  rPair  =  randObs()
  x  =  c( x, rPair[1] )
  y  =  c( y, rPair[2] )
}
z <- rnorm(n)
d <- data.frame( x, y, z )
d <- as.matrix(d)

p <- princomp(d)
mydata <- p$scores[,1:2]
wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))

for (i in 1:100) wss[i] <- sum(kmeans(mydata,centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of Clusters",ylab="Within groups sum of squares")
explained.variance <- 1 - wss / wss[1]
