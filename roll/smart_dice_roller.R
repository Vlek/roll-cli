final <- rep(NA, 100000)
for (i in 1:length(final)) {
  final[i] <- dice_roller(c(0.25, 0.25, 0.1, .1, .1, .2))
}
table(final)
microbenchmark(dice_roller(c(0.25, 0.25, 0.50)))

dice_roller <- function(probabilities) {

  if (sum(probabilities) != 1) {
    stop("probabilities must == 1!!!!!")
  }
  if (!is.numeric(probabilities)) {
    stop("probabilities must be a number!")
  }

  numbers <- max(nchar(probabilities) - 2)
  probabilities <- probabilities * 10^numbers
  final <- c()
  for (i in 1:length(probabilities)) {
    final <- c(final, rep(i, probabilities[i]))
  }

  dice_roll <- sample(final, 1)
  return(dice_roll)
}
