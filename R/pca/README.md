PCA相关画图展示
========
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
