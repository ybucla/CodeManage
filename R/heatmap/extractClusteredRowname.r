# extract clustered rowname after heatmap.2
hh<-heatmap.2(as.matrix(mydata),dendrogram="row",
    trace="none", margin=c(8,9), 
    hclust=hclustfunc,distfun=distfunc);

sorted <- mydata[match(rev(labels(hh$rowDendrogram)), rownames(mydata)), ]

#view result
head(sorted)
#               mpg cyl  disp  hp drat    wt  qsec vs am gear carb
# Toyota Corona 21.5   4 120.1  97 3.70 2.465 20.01  1  0    3    1
# Porsche 914-2 26.0   4 120.3  91 4.43 2.140 16.70  0  1    5    2
# Datsun 710    22.8   4 108.0  93 3.85 2.320 18.61  1  1    4    1
# Volvo 142E    21.4   4 121.0 109 4.11 2.780 18.60  1  1    4    2
# Merc 230      22.8   4 140.8  95 3.92 3.150 22.90  1  0    4    2
# Lotus Europa  30.4   4  95.1 113 3.77 1.513 16.90  1  1    5    2
