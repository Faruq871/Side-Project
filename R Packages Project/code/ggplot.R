library(ggplot2)
data(mpg)

# Scatter Plot
p1 <- ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(alpha = 0.8) +
  labs(title = "Displacement vs. Highway Mileage") +
  theme_minimal()
print(p1)

# Bar Chart
p2 <- ggplot(mpg, aes(x = manufacturer)) +
  geom_bar(fill = "steelblue") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p2)

# Faceting
p3 <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point() +
  facet_wrap(~ class) +
  theme_light()
print(p3)
