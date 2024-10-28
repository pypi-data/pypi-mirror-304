OddOrEven=as.integer(readline(prompt="Enter a number to find or even : "))
if(OddOrEven %% 2 == 0){
  cat(OddOrEven,"is Even")
}else{
  cat(OddOrEven,"is Odd")
}