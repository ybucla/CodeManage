# # lda using original equations from blei03
source("lda_func.r")

# parameters
M <- 35		# document number
k <- 10		# topic number
v <- 50		# unique words index length
n <- 100	# words for each document

# simulate initial parameters
sim_p <- sim_para()
ini.alpha <- sim_p$alpha
ini.beta <- sim_p$beta

# simulate observe
corpus <- NULL
for(i in 1:M){
	n <- sample(60:150,1)
	corpus[[i]] <- sim_docu(n)
}

# inference alpha, beta
alpha <- NULL
beta <- NULL
ll <- 0
for(i in 1:1000){
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
