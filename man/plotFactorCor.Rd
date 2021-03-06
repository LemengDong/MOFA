% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/plotFactors.R
\name{plotFactorCor}
\alias{plotFactorCor}
\title{Plot correlation matrix between latent factors}
\usage{
plotFactorCor(object, method = "pearson", ...)
}
\arguments{
\item{object}{a trained \code{\link{MOFAmodel}} object.}

\item{method}{a character indicating the type of correlation coefficient to be computed:
pearson (default), kendall, or spearman.}

\item{...}{arguments passed to \code{\link[corrplot]{corrplot}}}
}
\value{
Returns a symmetric matrix with the correlation coefficient between every pair of factors.
}
\description{
Function to plot the correlation matrix between the latent factors.
}
\details{
This method plots the correlation matrix between the latent factors. \cr 
The model encourages the factors to be uncorrelated, so this function usually
 yields a diagonal correlation matrix. \cr 
However, it is not a hard constraint such as in Principal Component Analysis and
 correlations between factors can occur, particularly with large number factors. \cr
Generally, correlated factors are redundant and should be avoided, as they make interpretation harder.
 Therefore, if you have too many correlated factors we suggest you try reducing the number of factors.
}
\examples{
# Example on the CLL data
filepath <- system.file("extdata", "CLL_model.hdf5", package = "MOFAdata")
MOFA_CLL <- loadModel(filepath)
plotFactorCor(MOFA_CLL)

# Example on the scMT data
filepath <- system.file("extdata", "scMT_model.hdf5", package = "MOFAdata")
MOFA_scMT <- loadModel(filepath)
plotFactorCor(MOFA_scMT)
}
