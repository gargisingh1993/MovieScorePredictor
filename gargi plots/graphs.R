
setwd("C:/users/gogs/Desktop/R/project")
# Load all the necessary libraries  
install.packages("RColorBrewer")

library(RColorBrewer)
library(tm)
library(wordcloud)
require("reshape2")
require(ggplot2)
require(dplyr)
require(tidyr)
require(gplots)
require(gridExtra)

# loads the movies data into a data frame
data1 <- read.csv("movie_metadata.csv", header = TRUE)

# plots the yearly average income

data2 <- as.data.frame(data1)
data2$new <- (data2$gross - data2$budget)
data3 <- data2[order(data2$title_year),]
data4 <- na.omit(data3)
data5<- aggregate(data4[,29],list(data4$title_year),mean)
plot(data5,xlab="year",ylab="average profits")


# wordcloud

wordcloud(data4$actor_1_name, random.order = T, colors = brewer.pal(8, "Dark2"), max.words = 200,scale = c(1.5,.5))
wordcloud(data4$plot_keywords, random.order = T, colors = brewer.pal(8, "Dark2"), max.words = 200,scale = c(1.5,.5))

# No of movies released each year, shows the increase in number of movies 
data6 = data.frame(table(data3$title_year))
plot(data6,xlab ="years",ylim = c(0,300),xlim = c(0,91))
