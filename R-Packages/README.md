# R Packages

This directory contains documentation, usage guides, and reproducible code snippets for standard R packages frequently utilized in data manipulation, visualization, and analysis workflows.

## Directory Structure

- `code/`: Contains subdirectories for each R package.
  - Each subdirectory (e.g., `dplyr/`, `ggplot2/`) includes an `.Rmd` file.
  - These RMarkdown files serve as interactive cheat sheets, demonstrating core functions, syntax, and best practices for the respective package.

## Prerequisites

To execute the code chunks within these documents, ensure the following packages are installed in your R environment:

```r
install.packages(c("dplyr", "ggplot2", "tidyr", "knitr", "rmarkdown"))
