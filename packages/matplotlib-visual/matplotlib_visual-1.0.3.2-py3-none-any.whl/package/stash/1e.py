Prime = as.integer(readline(prompt = "Enter a number to find Prime or not: "))
is_prime=TRUE
if(Prime <= 1){
  is_prime=False
}else{
  for (i in 2:sqrt(Prime)){
    if(Prime %% i == 0){
      is_prime=FALSE
      break
    }
  }
}
if(is_prime){
  cat(Prime,"is prime number")
}else{
  cat(Prime,"is not a prime number")
}