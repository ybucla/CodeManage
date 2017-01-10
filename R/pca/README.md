PCA相关画图展示
========
PCA 通常用来降维，在原始数据中，每行数据可以用多个feature表示，但是由于这些feature之间存在冗余，在维数巨大的情况下，后续的计算量非常大，因此可以通过降低维数以便后续计算分析，同时降维后的数据要尽量保证新数据保留了尽可能多的原始数据信息，这一点用方差表示。降维后，数据特征较少，当只有2,3个维数时，可以很容易从图中看出这些数据的分布，比如哪些数据在一起，在做后续聚类分析，如kmeans，KNN时可以辅助确定聚类个数。

*注意，在prcomp()命令中，输入矩阵为行向量，及每行代表一个数据，每列代表一个特征* <br>
*在周志华机器学习书中，投影方式为WTX，这里X为列向量，每一列代表一个数据* <br>
*PCA里面标准化一定是同一feature内标准化，因为方差是在同一组（feature）内计算得到的*


1. plot
------------
Directly use plot to visualise the variance proportion of each PC component

Example Usage
-------------

```r
# plot method
plot(ir.pca, type = "l")
```
![](https://github.com/ybucla/CodeManage/blob/master/R/pca/Example-ir.png)

2. ggbiplot
------------

An implementation of the biplot using ggplot2.  The package provides two functions: `ggscreeplot()` and `ggbiplot()`.
`ggbiplot` aims to be a drop-in replacement for the built-in R function `biplot.princomp()` with extended functionality 
for labeling groups, drawing a correlation circle, and adding Normal probability ellipsoids.

*The development of this software was supported in part by NSF Postdoctoral Fellowship DMS-0903120*

Installation
------------

```r
library(devtools)
install_github("vqv/ggbiplot")
```

Example Usage
-------------

```{r wine-example, message = FALSE, warning = FALSE}
library(ggbiplot)
data(wine)
wine.pca <- prcomp(wine, scale. = TRUE)
ggbiplot(wine.pca, obs.scale = 1, var.scale = 1,
  groups = wine.class, ellipse = TRUE, circle = TRUE) +
  scale_color_discrete(name = '') +
  theme(legend.direction = 'horizontal', legend.position = 'top')
```
![](https://github.com/ybucla/CodeManage/blob/master/R/pca/README-wine-example-1.png)
