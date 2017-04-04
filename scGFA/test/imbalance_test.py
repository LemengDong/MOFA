"""
Script to test how imbalance in number of features per view affects the results
"""

from __future__ import division
from time import time
import cPickle as pkl
import scipy as s
import os
import scipy.special as special
import scipy.stats as stats
import numpy.linalg  as linalg

# Import manually defined functions
from scGFA.core.simulate import Simulate
from scGFA.core.BayesNet import BayesNet
from scGFA.core.multiview_nodes import *
from scGFA.core.seeger_nodes import *
from scGFA.core.nodes import *
from scGFA.core.sparse_updates import *
from scGFA.core.utils import *
from scGFA.run.run_utils import *

###################
## Generate data ##
###################

# import numpy; numpy.random.seed(4)

# Define dimensionalities
M = 3
N = 100
D = s.asarray([50,1000,20000])
K = 6


## Simulate data  ##
data = {}
tmp = Simulate(M=M, N=N, D=D, K=K)

data['Z'] = s.zeros((N,K))
data['Z'][:,0] = s.sin(s.arange(N)/(N/20))
data['Z'][:,1] = s.cos(s.arange(N)/(N/20))
data['Z'][:,2] = 2*(s.arange(N)/N-0.5)
data['Z'][:,3] = stats.norm.rvs(loc=0, scale=1, size=N)
data['Z'][:,4] = stats.norm.rvs(loc=0, scale=1, size=N)
data['Z'][:,5] = stats.norm.rvs(loc=0, scale=1, size=N)

data['alpha'] = [ s.zeros(K,) for m in xrange(M) ]
data['alpha'][0] = [1,1,1e6,1,1e6,1e6]
data['alpha'][1] = [1,1e6,1,1e6,1,1e6]
data['alpha'][2] = [1e6,1,1,1e6,1e6,1]

theta = [ s.ones(K)*0.5 for m in xrange(M) ]
data['S'], data['W'], data['W_hat'], _ = tmp.initW_spikeslab(theta=theta, alpha=data['alpha'])

data['mu'] = [ s.zeros(D[m]) for m in xrange(M)]
# data['tau']= [ stats.uniform.rvs(loc=1,scale=3,size=D[m]) for m in xrange(M) ]
data['tau']= [ stats.uniform.rvs(loc=0.1,scale=1,size=D[m]) for m in xrange(M) ]

missingness = 0
Y_gaussian = tmp.generateData(W=data['W'], Z=data['Z'], Tau=data['tau'], Mu=data['mu'],
	likelihood="gaussian", missingness=missingness)
# Y_poisson = tmp.generateData(W=data['W'], Z=data['Z'], Tau=data['tau'], Mu=data['mu'],
# 	likelihood="poisson", missingness=missingness)
# Y_bernoulli = tmp.generateData(W=data['W'], Z=data['Z'], Tau=data['tau'], Mu=data['mu'],
# 	likelihood="bernoulli", missingness=missingness)
# Y_binomial = tmp.generateData(W=data['W'], Z=data['Z'], Tau=data['tau'], Mu=data['mu'],
	# likelihood="binomial", min_trials=10, max_trials=50, missingness=0.05)

# data["Y"] = ( Y_gaussian[0], Y_poisson[1], Y_bernoulli[2] )
data["Y"] = ( Y_gaussian[0], Y_gaussian[1], Y_gaussian[2] )

# Replace all observations of some samples with missing values
# missing = ([1,2,3],[4,5,6],[7,8,9])
# for m in xrange(M):
	# data["Y"][m][missing[m],:] = s.ma.masked

data_opts = {}
data_opts['outfile'] = "/Users/bvelten/Documents/CLL_MOFA_data/out/test/model_imbalance.hdf5"
data_opts['view_names'] = ["small", "medium", "large"]

#################################
## Initialise Bayesian Network ##
#################################

# Define initial number of latent variables
K = 15

# Define model dimensionalities
dim = {}
dim["M"] = M
dim["N"] = N
dim["D"] = D
dim["K"] = K


##############################
## Define the model options ##
##############################

model_opts = {}
model_opts['likelihood'] = ['gaussian']* M
model_opts['learnTheta'] = True
model_opts['k'] = K


# Define priors
model_opts["priorZ"] = { 'mean':0., 'var':1. }
model_opts["priorAlpha"] = { 'a':[1e-14]*M, 'b':[1e-14]*M }
model_opts["priorSW"] = { 'Theta':[s.nan]*M, 'mean_S0':[s.nan]*M, 'var_S0':[s.nan]*M, 'mean_S1':[s.nan]*M, 'var_S1':[s.nan]*M }
model_opts["priorTau"] = { 'a':[1e-14]*M, 'b':[1e-14]*M }
if model_opts['learnTheta']:
	model_opts["priorTheta"] = { 'a':[1.]*M, 'b':[1.]*M }

# Define initialisation options
model_opts["initZ"] = { 'mean':"random", 'var':1., 'E':None, 'E2':None }
model_opts["initAlpha"] = { 'a':[s.nan]*M, 'b':[s.nan]*M, 'E':[100.]*M }
model_opts["initSW"] = { 'Theta':[0.5]*M,
                          'mean_S0':[0.]*M, 'var_S0':model_opts["initAlpha"]['E'],
                          'mean_S1':[0]*M, 'var_S1':[1.]*M,
                          'ES':[None]*M, 'EW_S0':[None]*M, 'EW_S1':[None]*M}
# model_opts["initTau"] = { 'a':[1.,1.,None], 'b':[1.,1.,None], 'E':[100.,100.,None] }
model_opts["initTau"] = { 'a':[s.nan]*M, 'b':[s.nan]*M, 'E':[100.]*M }

if model_opts['learnTheta']:
    model_opts["initTheta"] = { 'a':[1.]*M, 'b':[1.]*M, 'E':[None]*M }
else:
    model_opts["initTheta"] = { 'value':[.5]*M }


# Define covariates
model_opts['covariates'] = None

# Define schedule of updates
# model_opts['schedule'] = ("SW","Z","Alpha","Tau","Theta","Y")
model_opts['schedule'] = ("SW", "Z", "Clusters", "Theta", "Alpha", "Tau")


#############################
## Define training options ##
#############################

train_opts = {}
train_opts['elbofreq'] = 1
train_opts['maxiter'] = 1000
train_opts['tolerance'] = 1E-2
train_opts['forceiter'] = True
# train_opts['dropK'] = { "by_norm":0.01, "by_pvar":None, "by_cor":None, "by_r2":0.01 }
train_opts['dropK'] = { "by_norm":None, "by_pvar":None, "by_cor":0.75, "by_r2":0.01 }
train_opts['savefreq'] = s.nan
train_opts['savefolder'] = s.nan
train_opts['verbosity'] = 2
# train_opts['trials'] = 1
cores = 1
keep_best_run = False



####################
## Start training ##
####################

# runMultipleTrials(data_opts, model_opts, train_opts, cores, keep_best_run)
trained_model = runSingleTrial(data["Y"], model_opts, train_opts)
outfile = data_opts['outfile'] 
# sample_names = (data["Y"])[0].index.to0list()
# feature_names = [  data["Y"][m].columns.values.tolist() for m in xrange(len(data)) ]
print "Saving model in %s...\n" % (outfile)
sample_names = [ "sample_%d" % n for n in xrange(N)]
feature_names = [[ "feature_%d" % n for n in xrange(D[m])] for m in xrange(M)]
saveModel(trained_model, outfile=outfile, view_names=data_opts['view_names'],
    sample_names=sample_names, feature_names=feature_names)