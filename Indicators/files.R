library(igraph)



workingDir = "/home/data/algopol/algopolapp/Raphael/Egopol/Indicators/csa"
outputPath = "/home/data/algopol/algopolapp/Raphael/Egopol/Indicators/Mehwish"
#workingDir = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\writestatuses\\"
#outputPath = "C:\\Users\\Mehwish\\Documents\\Link Prediction\\graphml\\"

setwd(workingDir)
fnames = list.files(workingDir)

for (findex in 1: length(fnames)){
  possibleError <- tryCatch({    
    
    setwd(paste(workingDir,fnames[findex],"Graphs",sep="/"))
    print(paste(workingDir,fnames[findex],"Graphs",sep="/"))
    
    file.copy("friends.gml",outputPath )
    
    setwd(outputPath)
    newname = paste(fnames[findex],".gml",sep="")
    file.rename("friends.gml", newname)
    
    
# w=read.graph("friends.gml", format="gml")     
# g <- graph.data.frame(w, directed=FALSE)
# g=simplify(w)# 
# edgelist = get.edgelist
    
    
  }, error = function(e){e})
  
  if(inherits(possibleError, "error")){
    #print("error")
    next
  } else{    
    #print("no error")
  }
  
  
}
