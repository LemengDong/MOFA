
from __future__ import division
import scipy as s

from nodes import *
from distributions import *


"""
This module is used to define Nodes that undergo variational bayesian inference.

Variational nodes have the following main variables:
    Important methods:
    - precompute: precompute some terms to speed up the calculations
    - calculateELBO: calculate evidence lower bound using current estimates of expectations/params
    - getParameters: return current parameters
    - getExpectations: return current expectations
    - update: general update function that calls the following two methods:
        - updateParameters: update parameters using current estimates of expectations
        - updateExpectations: update expectations using current estimates of parameters

    Important attributes:
    - markov_blanket: dictionary that defines the set of nodes that are in the markov blanket of the current node
    - Q: an instance of Distribution() which contains the specification of the variational distribution
    - P: an instance of Distribution() which contains the specification of the prior distribution
    - dim: dimensionality of the node
"""


"""
to-do: 
- improve bernoulli gaussian
"""

###########################################
## General classes for variational nodes ##
###########################################

class Variational_Node(Node):
    """
    Abstract class for a variational node in a Bayesian probabilistic model.
    Variational nodes can be observed (constant) or unobserved
    """
    def __init__(self, dim):
        Node.__init__(self,dim)

    def calculateELBO(self):
        # General method to calculate the ELBO of the node
        return 0.

###################################################################
## General classes for observed and unobserved variational nodes ##
###################################################################

class Constant_Variational_Node(Variational_Node,Constant_Node):
    """
    Abstract class for an observed/constant variational node in a Bayesian probabilistic model.
    """
    def __init__(self, dim, value):
        # SHOULD WE ALSO INITIALISE VARIATIONAL_NODE ..?
        Constant_Node.__init__(self, dim, value)

class Unobserved_Variational_Node(Variational_Node):
    """
    Abstract class for an unobserved variational node in a Bayesian probabilistic model.
    Unobserved variational nodes contain a prior P(X) and a variational Q(X) distribution,
    which will be stored as instances of Distribution() attributes .P and .Q, respectively.
    The distributions are in turn composed of parameters and expectations
    """
    def __init__(self, dim):
        Variational_Node.__init__(self, dim)
        self.P = None
        self.Q = None
    def updateExpectations(self, dist="Q"):
        # Method to update expectations of the node
        if dist == "Q": self.Q.updateExpectations()

    def getExpectation(self, dist="Q"):
        # Method to get the first moment (expectation) of the node
        if dist == "Q": expectations = self.Q.getExpectations()
        elif dist == "P": expectations = self.P.getExpectations()
        return expectations["E"]

    def getExpectations(self, dist="Q"):
        # Method to get all relevant moments of the node
        if dist == "Q": expectations = self.Q.getExpectations()
        elif dist == "P": expectations = self.P.getExpectations()
        return expectations

    def getParameters(self, dist="Q"):
        # Method to get all parameters of the node
        if dist == "Q": params = self.Q.getParameters()
        elif dist == "P": params = self.P.getParameters()
        return params

#######################################################
## Specific classes for unobserved variational nodes ##
#######################################################

class UnivariateGaussian_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where P(.) and Q(.)
    are both univariate Gaussian distributions.
    """
    def __init__(self, dim, pmean, pvar, qmean, qvar, qE=None):
	    # dim (2d tuple): dimensionality of the node
	    # pmean (nd array): the mean parameter of the P distribution
	    # qmean (nd array): the mean parameter of the Q distribution
	    # pvar (nd array): the variance parameter of the P distribution
	    # qvar (nd array): the variance parameter of the Q distribution
	    # qE (nd array): the initial first moment of the Q distribution
        Unobserved_Variational_Node.__init__(self, dim)

        # Initialise the P and Q distributions
        self.P = UnivariateGaussian(dim=dim, mean=pmean, var=pvar)
        self.Q = UnivariateGaussian(dim=dim, mean=qmean, var=qvar, E=qE)

class MultivariateGaussian_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where P(.) and Q(.)
    are both multivariate Gaussian distributions.
    """
    def __init__(self, dim, pmean, pcov, qmean, qcov, qE=None):
        # dim (2d tuple): dimensionality of the node
        # pmean (nd array): the mean parameter of the P distribution
        # pcov (nd array): the covariance parameter of the P distribution
        # qmean (nd array): the mean parameter of the Q distribution
        # qcov (nd array): the covariance parameter of the Q distribution
        # qE (nd array): the initial first moment of the Q distribution
        Unobserved_Variational_Node.__init__(self, dim)

        # Initialise the P and Q distributions
        self.P = MultivariateGaussian(dim=dim, mean=pmean, cov=pcov)
        self.Q = MultivariateGaussian(dim=dim, mean=qmean, cov=qcov, E=qE)

class Gamma_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where P(x) and Q(x) are both gamma distributions
    """
    def __init__(self, dim, pa, pb, qa, qb, qE=None):
	    # dim (2d tuple): dimensionality of the node
	    # pa (nd array): the 'a' parameter of the P distribution
	    # qa (nd array): the 'b' parameter of the P distribution
	    # qa (nd array): the 'a' parameter of the Q distribution
	    # qb (nd array): the 'b' parameter of the Q distribution
	    # qE (nd array): the initial expectation of the Q distribution
        Unobserved_Variational_Node.__init__(self,dim)

        # Initialise the distributions
        self.P = Gamma(dim=dim, a=pa, b=pb)
        self.Q = Gamma(dim=dim, a=qa, b=qb, E=qE)

class Bernoulli_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where P(.) and Q(.)
    are both bernoulli distributions.
    """
    def __init__(self, dim, ptheta, qtheta, qE=None):
	    # dim (2d tuple): dimensionality of the node
	    # ptheta (nd array): the 'theta' parameter of the P distribution
	    # qtheta (nd array): the 'theta' parameter of the Q distribution
	    # qE (nd array): initial first moment of the Q distribution
        Unobserved_Variational_Node.__init__(self,dim)

        # Initialise the distributions
        self.P = Bernoulli(dim=dim, theta=ptheta)
        self.Q = Bernoulli(dim=dim, theta=qtheta, E=qE)

class BernoulliGaussian_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where P(.) and Q(.)
    are joint gaussian-bernoulli distributions (see paper  Spike and Slab Variational Inference for
    Multi-Task and Multiple Kernel Learning by Titsias and Gredilla)
    """
    def __init__(self, dim, pmean, pvar, ptheta, qmean, qvar, qtheta):
	    # dim (2d tuple): dimensionality of the node
        # pmean (nd array): the mean parameter of the P distribution
        # pvar (nd array): the var parameter of the P distribution
	    # ptheta (nd array): the theta parameter of the P distribution
        # qmean (nd array): the mean parameter of the Q distribution
        # qvar (nd array): the var parameter of the Q distribution
	    # qtheta (nd array): the theta parameter of the Q distribution
        Unobserved_Variational_Node.__init__(self,dim)

        # Initialise the P and Q distributions
        self.P = BernoulliGaussian(dim=dim, theta=ptheta, mean=pmean, var=pvar)
        self.Q = BernoulliGaussian(dim=dim, theta=qtheta, mean=qmean, var=qvar)

    def getParameters(self, dist="Q"):
        if dist == "Q": return { 'theta':self.Q.theta, 'mean':self.Q.mean, 'var':self.Q.var }
        elif dist == "P": return { 'theta':self.P.theta, 'mean':self.P.mean, 'var':self.P.var }

    def getExpectation(self, dist="Q"):
        if dist == "Q": return self.Q.ESW
        elif dist == "P": return self.P.ESW

class Beta_Unobserved_Variational_Node(Unobserved_Variational_Node):
    """
    Abstract class for a variational node where both P(.) and Q(.) are beta
    distributions
    """
    def __init__(self, dim, pa, pb, qa, qb, qE=None):
        # dim (2d tuple): dimensionality of the node
        # pa (nd array): the 'a' parameter of the P distribution
        # qa (nd array): the 'b' parameter of the P distribution
        # qa (nd array): the 'a' parameter of the Q distribution
        # qb (nd array): the 'b' parameter of the Q distribution
        # qE (nd array): the initial expectation of the Q distribution
        super(Beta_Unobserved_Variational_Node, self).__init__(dim)

        # Initialise P and Q distributions
        self.P = Beta(dim, pa, pb)
        self.Q = Beta(dim, qa, qb, qE)

