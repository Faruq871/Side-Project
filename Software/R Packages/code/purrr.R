library(purrr)
library(dplyr)
data(mtcars)

# map (returns list)
means_list <- mtcars %>% map(mean)
means_list[["mpg"]]

# map_dbl (returns numeric vector)
mtcars %>% map_dbl(mean)

# map_chr (returns character vector)
mtcars %>% map_chr(class)

# map2 (two inputs)
list1 <- list(a = 1:3, b = 4:6)
list2 <- list(a = 10, b = 100)
map2(list1, list2, ~ .x + .y)

# walk (side effects, returns invisible NULL)
list(a = 1, b = 2) %>% walk(print)
