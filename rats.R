library(rstan)

y = read.table('https://raw.github.com/wiki/stan-dev/rstan/rats.txt', header = TRUE)
x = c(8, 15, 22, 29, 36)
xbar = mean(x)
N = nrow(y)
T = ncol(y)
rats_fit = stan(file = 'rats.stan')

print(rats_fit)
plot(rats_fit)
pairs(rats_fit, pars = c("mu_alpha", "mu_beta", "lp__"))

la = extract(rats_fit, permuted = TRUE) # return a list of arrays
mu = la$mu

### return an array of three dimensions: iterations, chains, parameters
a = extract(rats_fit, permuted = TRUE)

### use S3 functions as.array (or as.matrix) on stanfit objs
a2 = as.array(rats_fit)
m = as.matrix(rats_fit)

print(rats_fit, digits = 1)
