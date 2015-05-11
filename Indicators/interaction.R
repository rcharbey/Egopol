#Author: Mehwish Nasim (University of Konstanz), mehwish.nasim@uni-konstanz.de
#Date: 25 March 2015
#version: 2.1
#changes: 1. updated Adamic Adar zero condition
#         2. damping factor for katz index
#         3. file name convention  
#         4. added cosine similarity
#         - removed. clustering coeff*
#         6. Added Network perturbation*
#         7. added more readable comments after Features names 
#         8. Add gender attribute - in next version
## function for automatically installing and loading of packages
pkgLoad <- function(x)
{
  chooseCRANmirror(ind = 33)
  if (!require(x,character.only = TRUE))
  {
    install.packages(x,dep=TRUE)
    if(!require(x,character.only = TRUE)) stop("Package not found")
  }
  #now load library and suppress warnings
  suppressPackageStartupMessages(library(x, character.only=TRUE))
}




pkgLoad("rjson")
library(rjson)



workingDir = "/home/data/algopol/algopolapp/Raphael/Egopol/Indicators/csa"
outputPath = "/home/data/algopol/algopolapp/Raphael/Egopol/Indicators/Mehwish"
#workingDir = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\algopol-5egos-csa-nolinks\\algopol-5egos-csa-nolink-new\\Sample\\"
#outputPath = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\algopol-5egos-csa-nolinks\\algopol-5egos-csa-nolink-new\\newoutput\\"


setwd(workingDir)
fnames = list.files(workingDir)

result = matrix(0,0,2)
u = matrix (0,1,2)

for (findex in 1: length(fnames)){
  possibleError <- tryCatch({
    
    
    setwd(paste(workingDir,fnames[findex], sep="/"))
    ###############read statuses
    
    statusesFile <- readLines("statuses.jsons.gz")
    
    lengthStatus = length(statusesFile)
    print(lengthStatus)
    m=matrix(1, 0,lengthStatus)
    
    tempcommentLinkList = matrix(0,0,2)
    
    commentLinkList = matrix(0,0,2)
    counter=0
    
    for (i in 1:lengthStatus)
    {
      statuses = fromJSON( statusesFile[i], method = "C", unexpected.escape = "error" )
      
      comment = matrix(0,0,length(statuses$comments))
      
      if(length(statuses$comments )== 0)
      {next}
      
      for(j in 1:length(statuses$comments))
      {
        
        if(length(statuses$comments[[j]]$from$id) != 0)
        {
          counter= counter+1
        }
        
        
      }
      
    }
    u[1,1]=fnames[findex]
    u[1,2] =counter
    
    result = rbind(result,u)
    

    
    
  }, error = function(e){e})
  
  if(inherits(possibleError, "error")){
    #print("error")
    next
  } else{    
    #print("no error")
  }
  
  
}


setwd(outputPath)
write.csv(result, file ="number_of_statuses.csv")

