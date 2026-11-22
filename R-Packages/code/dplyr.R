library(dplyr)
data(mtcars)

# Filter
mtcars %>% filter(cyl == 4, mpg > 25) %>% head()

# Select
mtcars %>% select(mpg, cyl, hp) %>% head()

# Mutate
mtcars %>% mutate(hp_per_cyl = hp / cyl) %>% head()

# Arrange
mtcars %>% arrange(desc(mpg)) %>% head()

# Summarise
mtcars %>% 
  group_by(cyl) %>% 
  summarise(avg_mpg = mean(mpg), avg_hp = mean(hp), count = n())
