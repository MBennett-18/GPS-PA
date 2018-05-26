
# This has to be run on continuous accel. time.

library(PhysicalActivity)

data=read.csv("./data/files")
data$new=strptime(x = as.character(data$DATE__TIME),format = "%Y%m%d %H:%M:%S")
wear = wearingMarking(data,90,12,"new","VECTOR_MAG")

files <- list.files(path="./path/tp/files", pattern="*.csv", full.names=T, recursive=FALSE)
lapply(files, function(x) {
  t <- read.csv(x, header=T) # load file
  # apply function
  data$new=strptime(x = as.as.character(data$DATE__TIME),format = "%Y%m%d %H:%M:%S")
  wear = wearingMarking(data,90,12,"new","VECTOR_MAG")
  write.table(wear, "./out/path", sep="\t", quote=F, row.names=F, col.names=T)
})
