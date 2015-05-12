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
#workingDir = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\algopol-5egos-csa-nolinks\\algopol-5egos-csa-nolink-new\\Sample\\temp\\"
#outputPath = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\writestatuses\\"

setwd(workingDir)
fnames = list.files(workingDir)


for (findex in 1: length(fnames)){
  possibleError <- tryCatch({
    
    
    setwd(paste(workingDir,fnames[findex], sep=""))

  ###############read statuses
  
  statusesFile <- readLines("statuses.jsons.gz")
  
  lengthStatus = length(statusesFile)
  m=matrix(1, 0,lengthStatus)
  
  tempcommentLinkList = matrix(0,0,2)
  
  commentLinkList = matrix(0,0,2)
  
  for (i in 1:lengthStatus)
  {
    statuses = fromJSON( statusesFile[i], method = "C", unexpected.escape = "error" )
    #print(statuses[[i]]$type)
    comment = matrix(0,0,length(statuses$comments))
    
    if(length(statuses$comments )== 0)
    {next}
    
    for(j in 1:length(statuses$comments))
    {
      #comment[j]=statuses[[i]]$comments[[j]]$from$id
      if(length(statuses$comments[[j]]$from$id) != 0)
      {
        tempcommentLinkList[1]= statuses$id
        tempcommentLinkList[2]= statuses$comments[[j]]$from$id
        commentLinkList=rbind(commentLinkList,tempcommentLinkList)
      }
      
      
    }
    
  }
  
  

 
 
  # write dataframe to a file
  setwd(outputPath)
  
  writefile = paste("statuses_", fnames[findex],".csv", sep="")
  write.csv(commentLinkList, writefile, row.names=FALSE)
  
  

  }, error = function(e){e})

      if(inherits(possibleError, "error")){
        #print("error")
        next
      } else{    
        #print("no error")
      }


}



