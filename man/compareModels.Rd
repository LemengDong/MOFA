% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/compareModels.R
\name{compareModels}
\alias{compareModels}
\title{Compare different instances of trained \code{\link{MOFAmodel}}}
\usage{
compareModels(models, show_modelnames = FALSE)
}
\arguments{
\item{models}{a list containing \code{\link{MOFAmodel}} objects.}

\item{show_modelnames}{boolean, whether to indicate the name of each model instance
(names of the list in models) or not}
}
\value{
a ggplot showing the number of factors and
  the ELBO statistics of the given models as a barplot
}
\description{
Different objects of \code{\link{MOFAmodel}} are compared in terms
 of the final value of the ELBO statistics. 
For model selection the model with the highest ELBO value is selected.
 The height of the bar indicates the number of inferred factors and 
 the color of the bar the value of the ELBO statistic.
}
\examples{
### Example on simulated data
# Simulate Data
data <- makeExampleData()
# Create MOFA model
MOFAobject <- createMOFAobject(data)
# Prepare MOFA model
MOFAobject <- prepareMOFA(MOFAobject)
# Train several instances of MOFA models
n_inits <- 3 
MOFAlist <- lapply(seq_len(n_inits), function(i) runMOFA(MOFAobject, outfile=tempfile()))
compareModels(MOFAlist)
}
