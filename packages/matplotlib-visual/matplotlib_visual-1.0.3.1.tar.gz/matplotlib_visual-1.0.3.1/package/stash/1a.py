Armstrong = as.integer(readline(prompt = "Enter a number to find Armstrong or not: "))
temp = Armstrong
sum=0
while(temp>0){
  digits=temp%%10
  sum=sum+(digits^nchar(as.character(Armstrong)))
  temp=floor(temp/10)
}
if(Armstrong==sum){
  cat(Armstrong,"is a Armstrong number")
}else{
  cat(Armstrong,"is not a Armstrong number")
}