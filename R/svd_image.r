# SVD test on image

library(imager)
plot(boats)
boats.g <- grayscale(boats)
plot(boats.g)

rotate <- function(x) t(apply(x, 2, rev))
m <- boats.g[,,,]
m <- rotate(t(m))

r <- svd(m)
par(mfrow=c(3,10))
par(mar=c(0,0,0,0))
for(i in 2:31){
  u <- r$u[,1:i]
  d <- diag(r$d[1:i])
  v <- r$v[,1:i]
  nm <- u %*% d %*% t(v)
  image(nm,col = grey(seq(0,1,length.out = 255)),axes=FALSE)
}
