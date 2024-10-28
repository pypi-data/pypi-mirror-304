data <-mtcars

#Descriptive Statistics
mean_data<-mean(data$mpg)
median_data<-median(data$mpg)
sd_data<-sd(data$mpg)
var_data<-var(data$mpg)
fivenum_data<-fivenum(data$mpg) 

cat("Mean:",mean_data,"\n")
cat("Median:",median_data,"\n")
cat("Standard Deviation:",sd_data,"\n")
cat("Variance:",var_data,"/n")
cat("five_number Summary:",fivenum_data,"\n")


#Data visualization
hist(data$mpg,main="Histogram",xlab="MPG",col="blue",border="black")
boxplot(data $mpg,main="Boxplot",Ylab="MPG")
plot(data$mpg,main="scatterplot",Xlab="weight",Ylab="MPG",pch=19)
barplot(table(data$cyl),main = "Barplot",xlab="no of cylinder",Ylab="Frequency",col="green")