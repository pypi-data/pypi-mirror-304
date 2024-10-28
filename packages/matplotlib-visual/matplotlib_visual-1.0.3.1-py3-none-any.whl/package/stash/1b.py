Factorial = as.integer(readline(prompt = "Enter a number to find factorial: "))
fact=1
for ( i in 1:Factorial){
  fact=fact*i
}
cat("Factorial of",Factorial,"is",fact)