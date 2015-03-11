# Data Fetch!

datafetch = function(dir){
  mat = matrix(0,nrow=length(dir),ncol=5)
  for (a in 1:length(dir)){
    dat = read.csv(dir[a])
    mat[a,1] = dat[nrow(dat),1]
    mat[a,2] = dat[nrow(dat),2]
    mat[a,3] = dat[nrow(dat),3]
    mat[a,4] = dat[nrow(dat),4]
    mat[a,5] = dat[nrow(dat),5]
  }
  return(mat)
}

setwd("~/Documents/adaptive-network/Data/Generic/")
dir = dir()
generic = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/PRER/30 Percent")
dir = dir()
prer30 = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/Restriction//20")
dir = dir()
R20 = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/Generic Run/")
dir = dir()
genrun = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/Undiscovered/UD4/")
dir = dir()
UD4 = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/Restriction/20/")
dir = dir()
restrict = datafetch(dir)
setwd("~/Documents/adaptive-network/Data/Undiscovered/UD4-R20/")
dir = dir()
UD4R20 = datafetch(dir)

boxplot(
  generic[,4]+generic[,5],
  prer30[,4]+prer30[,5],
  genrun[,4]+genrun[,5],
  UD4[,4]+UD4[,5],
  restrict[,4]+restrict[,5],
  UD4R20[,4]+UD4R20[,5],
  ylab = "Total Infected Individuals (N)",
  names = c("Null","Leary30","UNRST","UNRST-UD4","R20","R20-UD4")
  )


