setwd("c:/work/github/random")

library(rstan)
# these have already been called - seems like once is enough
#rstan_options(auto_write = TRUE)
#options(mc.cores = parallel::detectCores())

schools_dat = list(J = 8,
                   y = c(28, 8, -3, 7, -1, 1, 18, 12),
                   sigma = c(15, 10, 16, 11, 9, 11, 10, 18))

fit = stan(file = "8schools.stan", data = schools_dat,
           iter = 1000, chains = 4)

print(fit)
plot(fit)
pairs(fit, pars = c("mu", "tau", "lp__"))

la = extract(fit, permuted = TRUE) # return a list of arrays
mu = la$mu

### return an array of three dimensions: iterations, chains, parameters
a = extract(fit, permuted = TRUE)

### use S3 functions as.array (or as.matrix) on stanfit objs
a2 = as.array(fit)
m = as.matrix(fit)

print(fit, digits = 1)