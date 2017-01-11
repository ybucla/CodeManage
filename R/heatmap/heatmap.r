# heatmap.2
library('gplots')
d <- read.table("clipboard",header=TRUE,sep="\t")
dmatrix <- data.matrix(d[,2:11])
rownames(dmatrix) = c("GM18486","GM18498","GM18499","GM18909","GM18501","GM18502","GM18504","GM18505","GM18507","GM18508")
heatmap.2(dmatrix,col=rev(redblue(100)),Colv = NA,dendrogram='row',keysize = 0.5,lhei = c(0.8,4.7),lwid=c(1.5,4),key.xlab = NA,key.title = NA,trace = 'none',density.info = "none",srtCol=30,cexCol=1.5,cexRow = 0.8,margins = c(5,8))


# pheatmap
library(pheatmap)
d <- read.table("clipboard",header=TRUE,sep="\t")
dmatrix <- data.matrix(d[,2:11])
rownames(dmatrix) = c("GM18486","GM18498","GM18499","GM18909","GM18501","GM18502","GM18504","GM18505","GM18507","GM18508")
pheatmap(dmatrix,fontsize=20,fontface='bold')
