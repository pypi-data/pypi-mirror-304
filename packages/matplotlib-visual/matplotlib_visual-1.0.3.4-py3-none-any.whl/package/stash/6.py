if (!require(ISLR)) install.packages("ISLR")
if (!require(MASS)) install.packages("MASS")
if (!require(ROCR)) install.packages("ROCR")

library(ISLR)
library(MASS)
library(ROCR)

data <- ISLR::Default
set.seed(1)
train_indices <- sample(seq_len(nrow(data)), size = 0.7 * nrow(data))
train <- data[train_indices, ]
test <- data[-train_indices, ]

model <- glm(default ~ student + balance + income, family = "binomial", data = train)

mcfadden_r2 <- 1 - (logLik(model) / logLik(glm(default ~ 1, family = "binomial", data = train)))
print(mcfadden_r2)

predicted_probs <- predict(model, test, type = "response")
test$default <- ifelse(test$default == "Yes", 1, 0)

pred <- prediction(predicted_probs, test$default)
perf <- performance(pred, "tpr", "fpr")
roc_auc <- performance(pred, "auc")@y.values[[1]]
print(roc_auc)

plot(perf, col = "blue", lwd = 2)
abline(a = 0, b = 1, lty = 2, col = "gray")

threshold <- 0.5
conf_matrix <- table(Predicted = ifelse(predicted_probs > threshold, 1, 0), Actual = test$default)
print(conf_matrix)

sensitivity_value <- conf_matrix[2,2] / sum(conf_matrix[2,])
specificity_value <- conf_matrix[1,1] / sum(conf_matrix[1,])
print(sensitivity_value)
print(specificity_value)
