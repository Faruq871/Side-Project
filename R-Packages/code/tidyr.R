library(tidyr)
library(dplyr)
data(iris)

# Pivot Longer (Wide to Long)
iris_long <- iris %>% 
  pivot_longer(cols = -Species, names_to = "Measurement", values_to = "Value")
head(iris_long)

# Pivot Wider (Long to Wide)
iris_long %>% 
  pivot_wider(names_from = Measurement, values_from = Value) %>% 
  head()

# Drop NA
df_na <- data.frame(id = 1:4, value = c(10, NA, 30, NA))
df_na %>% drop_na(value)

# Separate / Unite (String manipulation)
df_str <- data.frame(date = c("2026-11-22", "2026-11-23"))
df_str %>% separate(date, into = c("year", "month", "day"), sep = "-")
