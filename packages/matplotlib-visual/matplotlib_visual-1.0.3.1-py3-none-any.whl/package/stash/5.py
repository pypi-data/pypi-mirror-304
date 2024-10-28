#the R code to implement linear regression using the lm() function:
  # Load libraries (if not already loaded)
library(stats)

# Sample data (replace with your data)
x <- c(1, 2, 3, 4, 5)
y <- c(2, 4, 5, 4, 5)

# Create the model
model <- lm(y ~ x)

# Print the model summary
summary(model)

# Make predictions for new data
new_x <- 6
predicted_y <- predict(model, newdata = data.frame(x = new_x))

# Print the predicted value
cat("Predicted y for x =", new_x, ":", predicted_y)

#This code demonstrates how to create a linear regression model using the lm() function, obtain a summary of the model, and make predictions for new data points.