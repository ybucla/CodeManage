
heatmap 画图命令
========

*注意，以下命令都是从剪贴板读入数据* <br>

数据为：
```r
            A	B	C	D	E	F	G	H	I	J
GM18486 	6	2	2	2	1	3	2	2	3	1
GM18498 	2	6	3	3	1	3	3	3	2	1
GM18499 	2	3	6	3	1	3	3	4	2	1
GM18909 	2	3	3	8	1	3	3	3	2	1
GM18501 	1	1	1	1	3	1	2	2	1	2
GM18502 	3	3	3	3	1	11	4	3	3	1
GM18504 	2	3	3	3	2	4	5	4	3	1
GM18505 	2	3	4	3	2	3	4	8	3	1
GM18507 	3	2	2	2	1	3	3	3	5	0
GM18508 	1	1	1	1	2	1	1	1	0	2
```

(1). heatmap.2
------------
Directly use plot to visualise the variance proportion of each PC component

Example Usage
-------------

```r
library('gplots')
d <- read.table("clipboard",header=TRUE,sep="\t")
dmatrix <- data.matrix(d[,2:11])
rownames(dmatrix) = c("GM18486","GM18498","GM18499","GM18909","GM18501","GM18502","GM18504","GM18505","GM18507","GM18508")
heatmap.2(dmatrix,col=rev(redblue(100)),Colv = NA,dendrogram='row',keysize = 0.5,lhei = c(0.8,4.7),lwid=c(1.5,4),key.xlab = NA,key.title = NA,trace = 'none',density.info = "none",srtCol=30,cexCol=1.5,cexRow = 0.8,margins = c(5,8))
```
![](https://github.com/ybucla/CodeManage/blob/master/R/heatmap/heatmap.2.png)

(2). pheatmap
------------

```r
# pheatmap
library(pheatmap)
d <- read.table("clipboard",header=TRUE,sep="\t")
dmatrix <- data.matrix(d[,2:11])
rownames(dmatrix) = c("GM18486","GM18498","GM18499","GM18909","GM18501","GM18502","GM18504","GM18505","GM18507","GM18508")
pheatmap(dmatrix,fontsize=20,fontface='bold')
```

![](https://github.com/ybucla/CodeManage/blob/master/R/heatmap/pheatmap.png)
