jls_extract_var = """ 


# Assignment 1:
# Load the in-build dataset from R and draw various basic plot in R using grid (Horizontal bar plot, Vertical bar plot, box plot, multiple box plot, plot with point an lines etc.,)


# Dataset used:  rock  => Top 10 Measurements on Petroleum Rock Samples.



data_ = datasets::rock




# Bar Plots 

# Vertical bar plot:
barplot(
  unique(data_$perm), 
  ylab = "Perimeter (in cm)",
  col = "DarkRed",
  ylim = c(0, max(data_$perm)),
  main = "Barplot of Petroleum Rock Samples measurements",
  sub = "\n Bimal parajuli (20BDS0405)",
  horiz = FALSE #optional argument (default is false).
)

# Horizontal bar plot:
barplot(
  unique(data_$perm), 
  horiz = TRUE,
  xlab = "Perimeter (in cm)",
  col = "DarkRed",
  xlim = c(0, max(data_$perm)),
  main = "Barplot of Petroleum Rock Samples measurements",
  sub = "\n Bimal parajuli (20BDS0405)"
)


# Box Plots:
# Box Plot of surface areas:

boxplot(data_$shape, 
        col = "white", 
        main = "Box plot of surface areas of rocks.",
        sub = "Bimal Parajuli (20BDS0405)",
        ylab = "Area in Sq cm.")
stripchart(data_$shape,
           col = "cyan",
           method = "jitter",
           vertical = TRUE,
           add = TRUE,
           pch = 20)


# Multiple Box Plots:
# Shape attribute excluded because it is extremely small and needs a different scale.

bxplt_data = select(data_, -shape)

boxplot(select(data_, -shape), 
        col = "white",
        main = "Boxplots of Rock area, perimeter and permeability",
        sub = "Bimal Parajuli (20BDS0405) ")

stripchart(select(data_, -shape),
           col = 2:4,
           method = "jitter",
           vertical = TRUE,
           add = TRUE,
           pch = 20)


# Plots with point and a line:
area10 = data_[c(1, 3, 8, 40, 10), 1]
peri10 = data_[c(1, 3, 8, 40, 10), 2]

# Plotting only points:
area10 = data_[1:40, 1]
peri10 = data_[1:40, 2]

plot(x = area10, 
     y = peri10, 
     xlab = "Area in sq. cm",
     ylab = "Perimeter in cm.",
     main = "Scatter plot of area vs perimeter of rocks",
     sub = "Bimal Parajuli (20BDS0405)",
     pch = 15,
     col = 2)



# 2.	Task:
# Load in-build dataset mtcars and visualize data using visualization library (ggplot).




# Factor the gear attribute into 3 levels and assign names to each level:


factor(mtcars$gear,
       levels = c(3, 4, 5),
       labels = c('3gear', '4Gear', '5Gear')
       )



# Plot the weight vs miles per gallon simply using base-R.
plot(mtcars$wt, mtcars$mpg, col = 'orange', 
     main = "Plot of Car's mileage vs Weight.",
     sub = "Bimal Parajuli (20BDS0405)",
     xlab = "Weight of car",
     ylab = "Mileage per gallon")



# Same plot using ggplot2
ggplot2::ggplot(data = mtcars,
       aes(x=wt, y=mpg)) +
  geom_point() + 
  geom_line() + 
  xlab('Weight') + 
  ylab('Mileage') + 
  ggtitle('Weight vs Mileage')



# Use factor of gears 
# To plot the different gear with different colors.

ggplot2::ggplot(data = mtcars,
                aes(x=wt, y=mpg, color = as.factor(gear))) +
  geom_point() + 
  geom_line() + 
  xlab('Weight') + 
  ylab('Mileage') + 
  ggtitle('Weight vs Mileage plot by Bimal Parajuli (20BDS0405)')



# Use factors of Number of Cylinders.
#  To plot different gears cylinder numbers with differen colors.

ggplot2::ggplot(data = mtcars,
                aes(x=wt, y=mpg, color = as.factor(cyl))) + 
  geom_point() + 
  geom_line() +
  xlab('Weight') +
  ylab('Mileage') +
  ggtitle('Weight vs Mileage by Bimal Parajuli (20BDS0405')



# To plot different shapes in the plot for different legends.

ggplot2::ggplot(data = mtcars,
                aes(x=wt, y=mpg, shape = as.factor(cyl))) +
  geom_point() + 
  geom_line() +
  xlab("Weight") + 
  ylab("Mileage") + 
  ggtitle('Weight vs mileage by Bimal Parajuli')



# combining different shapes and colors 
# for different factor levels.

ggplot2::ggplot(data = mtcars,
                aes(x=wt, y=mpg, shape = as.factor(cyl), color = as.factor(cyl))) +
  geom_point() + 
  geom_line() +
  xlab("Weight") + 
  ylab("Mileage") + 
  ggtitle('Weight vs mileage by Bimal Parajuli (20BDS0405)')




# Aim: Statistical Analysis – Univariate, Bivariate, Multivariate – plotting and coloring for maps:

# 1.	Task: Load the gapminder dataset and perform statistical analysis using tidyverse and dplyr libraries.


install.packages('gapminder')

library(gapminder)

# View(gapminder)

library(tidyr)
library(dplyr)
library(ggplot2)


# Extract the data of continent 'Asia'.
gapminder_asia = filter(gapminder, continent=='Asia')
gapminder_asia


# Extract the data of the year 1957.
gapminder_1957 = gapminder %>% filter(year == 1957)
gapminder_1957


# Extract the data from china of the year 2002.
gapminder_2002_china = gapminder %>% filter(year == 2002) %>% filter(country == "China")
gapminder_2002_china




# Sort the life Expectancy in descending order. 

sorted_lifeExp = arrange(gapminder, desc(lifeExp))
sorted_lifeExp


# Year 1957 and pop in desc order.

sorted_1957_pop_desc = gapminder %>% filter(year == 1957) %>% arrange(desc(pop))
sorted_1957_pop_desc


# Life Expectancy in Months.

# Mutate adds new columns by preserving existing ones. 
lifeExpectancy_months = gapminder %>% mutate(lifeExp_months = lifeExp * 12)
lifeExpectancy_months

# Transmutate adds columns and drops existing ones.
lifeExpectancy_months_only = gapminder %>% transmute(lifeExpMonths = lifeExp * 12)
lifeExpectancy_months_only



# Extract all the records from the year 1952.

gapminder_1952 = gapminder %>% 
                          filter(year == 1952)




# Visualize the scatter plot between population and gdp Per capita for gapminder_1952.

plot(gapminder_1952$pop, gapminder_1952$gdpPercap,
     xlab = "Population in the year 1952",
     ylab = "GDP Per capita in the year 1952",
     col = 'green',
     main = "Population vs GDP in 1952",
     sub = "Bimal Parajuli (20BDS0405)"
     )



# OR using ggplot,
ggplot(data = gapminder_1952, 
       aes(x = pop,
           y = gdpPercap))+
  geom_point() +
  ggtitle("By Bimal Parajuli (20BDS0405)")


# Data is concentrated towards the origin with very few outliers in the extreme end. 
# So, the scale can be readjusted in the logarithmic scale.
# Eg:

ggplot(data = gapminder, 
       aes(x = pop, 
           y = gdpPercap))+
  geom_point() + 
  scale_y_log10() +
  scale_x_log10() +
  ggtitle("By Bimal Parajuli (20BDS0405)")



# Draw a tabulated graph for people by year on adjusted logarithmic scale. 
# with color indexed on Continents.

ggplot(data = gapminder,
       aes(x = pop,
           y = gdpPercap,
           color = continent)) + 
  geom_point() + 
  scale_x_log10() + 
  scale_y_log10() +
  facet_wrap(~ year) +
  ggtitle("By Bimal Parajuli (20BDS0405)")



# Draw a tabulated graph for people by year on adjusted logarithmic scale. 
# with color indexed on Continents and size of circles based on population.
ggplot(data = gapminder,
       aes(x = pop,
           y = gdpPercap,
           color = continent, 
           size = pop)) + 
  geom_point() + 
  scale_x_log10() + 
  scale_y_log10() +
  facet_wrap(~ year) +
  ggtitle("By Bimal Parajuli (20BDS0405)")



# Summarize funtions

# Display the median Life Expectancy and maximum gdpPercapita for the yearr 1957

summary_1 = gapminder %>% 
              filter(year == 1957) %>% 
              summarise(MedianLifeExp =
                          median(lifeExp), 
                        MaxGDP = 
                          max(gdpPercap))
# Display the Median Life Expectancy by year for each distinct year.

summary_2 = gapminder %>%
              group_by(year) %>%
              summarise(MedianLifeExpectancy = 
                          median(lifeExp))

# Visualize the Median Life expectancy for each year, in a scatter plot. 

ggplot(data = summary_2,
       aes(x = year,
           y = MedianLifeExpectancy)) +
  geom_point()


# Summarize the median, gdpPercapita by year and Continent 
# and Save it in by_year_continent

by_year_continent = gapminder %>% 
                      group_by(year, continent) %>% 
                      summarise(MedianGdpPerCap = 
                                  median(gdpPercap))


# Visualize year vs median GDP
# Line Plot. 

ggplot(data = by_year_continent,
       aes(x = year,
           y = MedianGdpPerCap,
           color = continent,
           size = MedianGdpPerCap)) +
  geom_line() +
  ggtitle("By Bimal Parajuli (20BDS0405)")




# 2.	Task: Using RClolorBrewer visualize mpg data.

# Coloring the plots in R: 

set.seed(444)
x <- rnorm(45)
y <- rnorm(45)
plot(x, y)

# Set some color in the plot.

# Col, defines the color of plot.

# Note: 
# rep(a: b, times = c) creates a repetition of numbers form a to b for c times.
# rep(a: b, each = c) creates a repetition of numbers from a to b by repeating each number for c times consecutively. 

# pch, symbols/icons used in plotting.

plot(x, y, 
     col = rep(1:27), 
     pch = 25)



# Legend function is used to put legend onto the figures. 
# legend, the text used in the legend.
# col, the color displayed in the legend. (use the same one as in plot)
# pch, the symbol displayed in the legend (use the same one as in plot)
# bty, "y" or "n" whether the boundary line on legend is visible or not.

legend("bottomright", 
       legend = paste("Group", 1:3),
       # col = 1:3,
       pch = 25, 
       bty = "y")



# Colors with ggplot.

# Import the libraries,
library(RColorBrewer)
library(viridis)
library(ggplot2)

# =================================


ggplot(data = mpg,
       aes(x = cty)) +
  geom_density()





# Density plots having different color of plot for different number of cylinders.
ggplot(data = mpg,
       aes(x = cty)) +
  geom_density(aes(fill = factor(cyl), 
                   alpha = 1.5)) +
  labs(title = "Bimal Plot",
       x = "City Mileage",
       fill = 'Number of Cylinders')


# Use a particular color palette to make the plots uniform and consistent.

ggplot(data = mpg,
       aes(x = cty)) +
  geom_density(aes(fill = factor(cyl), 
                   alpha = 1.5)) +
  labs(title = "Bimal Plot",
       x = "City Mileage",
       fill = 'Number of Cylinders') +
  scale_fill_brewer(palette = "Purples")



# Display in a grid the same plot with different color palettes.
p1 = p2 = p3 = p4 = ggplot(data = mpg,
                           aes(x = cty)) +
  geom_density(aes(fill = factor(cyl), 
                   alpha = 1.5)) +
  labs(title = "Bimal Plot",
       x = "City Mileage",
       fill = 'Number of Cylinders')

p1 = p1 + scale_fill_brewer(palette = "Oranges")
p2 = p2 + scale_fill_brewer(palette = "Blues")
p3 = p3 + scale_fill_brewer(palette = "Purples")
p4 = p4 + scale_fill_brewer(palette = "Greens")

library('gridExtra')
# For displaying grids of graphs.

grid.arrange(p1, p2, p3, p4, nrow = 2, top = "Grid of Plots")




# 3.	Task: Load USArrests in-build dataset and correlate in the maps with anyone fields. Display the maps using colormapping.

View(USArrests)

arrests_us <- USArrests

arrests_us$region = tolower(rownames(arrests_us))
View(arrests_us)

View(map_data("state"))

state_data <- map_data("state")

# dplyr package for left_join().
library(dplyr)
arrest_map <- left_join(arrests_us, state_data, by = "region")

View(arrest_map)



# Create the map
ggplot(
  data = arrest_map,
  aes(
    x = long, 
    y = lat, 
    group = group
  )
) + geom_polygon()+
  ggtitle("By Bimal Parajuli (20BDS0405)")




ggplot(
  data = arrest_map,
  
  aes(
    x = long, 
    y = lat, 
    group = group)) + 
  
  geom_polygon(
    aes(fill = Assault),
    color = "white") + 
  
  scale_fill_viridis(
    option = "B", 
    direction = -1) +
  
  ggtitle("Map Showing Assault cases over USA By Bimal Parajuli (20BDS0405)")




ggplot(
  data = arrest_map,
  
  aes(
    x = long, 
    y = lat, 
    group = group)) + 
  
  geom_polygon(
    aes(fill = Murder),
    color = "white") + 
  
  scale_fill_viridis(
    option = "B", 
    direction = -1) +
  
  ggtitle("Map Showing Murder cases over USA By Bimal Parajuli (20BDS0405)")




# Assignment 2:

# Create a Simple dashboard using Shiny.

# -	Write both frontend and backend codes for a Shiny Web app in R that provide the option to the user to enter the parameters for binomial distributions and exponential distributions.
# -	On the backend, fetch user’s input and generate randomized value fitting the received distribution parameters.
# -	Return the generated data and visualize it on the front end as histograms.
# Code:
# UI Code:


library(shiny)
library(shinydashboard)

shinyServer(
  pageWithSidebar(
    headerPanel("20BDS0405 (Bimal Parajuli) - Shiny App - DataViz LAB Assignment"),
    sidebarPanel(
      selectInput("Distribution",
                  "pls. Select Distribution Type",
                  choices = c("Normal", "Exponential")),
      
      sliderInput("SampleSize",
                  "Pls. Select Sample Size",
                  min = 100,
                  max = 5000,
                  value = 1000,
                  step = 100),
      
      conditionalPanel(condition = "input.Distribution == 'Normal'",
                       textInput("mean",  "Pls select mean:", 10),
                       textInput("sd", "Pls. select SD: ", 3)),
      

      conditionalPanel(
        condition = "input.Distribution == 'Exponential'",
        textInput("lambda", "Pls> Select lambda", 1)
    )
  ),
  
  mainPanel(
    plotOutput(
      "myPlot"
    )
  )
)
)

# Server Code:

# Server Portion.

shinyServer(
  function(input, output, session){
    
    output$myPlot <- renderPlot({
      
      distType <- input$Distribution
      size <- input$sampleSize
      
      if(distType == "Normal"){
        
          randomVec <- rnorm(size, 
                             mean = as.numeric(input$mean),
                             sd = as.numeric(input$sd)
                          )
      } else{
        randomVec <- rexp(size,
             rate = 1/as.numeric(input$lambda)
             )
      }
      
      hist(randomVec, col = "Blue")
    })
    
  }
  
)





# Draw Various Plots for the given dataset:

# DataSet: Mouse Protein DataSet
# Plots:
# 1.	Barplots
# 	with ggplot2
# 	with coordinate flip
# 	with error bars
# 	Stacked barplots

# 2.	Scatter Plot
# 	With shape empty/blank diamond
# 	with shape filled 180 degree rotated triangle

# 3.	Heatmap
# 	with scalar
# 	with divergence

# 4.	3D Piechart

# 5.	Dashboard using Looker Studio
# 1.	Barplots:
# Reading data:
dataset <- readxl::read_xls( 'D:\\Academics\\VIT_Academics\\6th_sem\\DataViz\\LAB\\LAB6\\Data_Cortex_Nuclear.xls')

barplot_dataset <- dataset %>% select(c(4, 5, 8))

# With ggplot2:
# Code:
# Barplot of BDNF_N vs NR1_N
ggplot(data = barplot_dataset,
       aes(
         x= BDNF_N,
         y=NR1_N,
         fill = BDNF_N )) + 
  geom_bar(stat = 'identity') +
  scale_x_binned(n.breaks = 10) + 
  ggtitle('Plot of BDNF_N vs NR1_N by Bimal Parajuli by 20BDS0405')
# Output:
 
# Code:
# Another bar plot:

barplot_dataset2 <- select(dataset, c('SYP_N', 'Treatment', 'class', 'Behavior'))
barplot_dataset2$class = factor(barplot_dataset2$class)
barplot_dataset2$Treatment = factor(barplot_dataset2$Treatment)
barplot_dataset2$Behavior = factor(barplot_dataset2$Behavior)

ggplot(barplot_dataset2, 
       aes(x = class, 
           fill = Behavior)) + 
  geom_bar() +
  labs(x = "Class", 
       y = "Number of records", 
       fill = "Behavior") +
  ggtitle('Barplot of no. of records of different classes and behaviour by Bimal Parajuli (20BDS0405)')

 
# With coordinate flip:

# Code:
ggplot(barplot_dataset2, 
       aes(x = class,
           fill = Behavior)) + 
  geom_bar() +
  labs(x = "Class", 
       y = "Number of records", 
       fill = "Behavior") +
  ggtitle('Barplot of no. of records of different classes and behaviour by Bimal Parajuli (20BDS0405)') +
  coord_flip()


# Output:
 

# With error bars:
# Code:

ggplot(data = head(barplot_dataset, 20),
       aes(x = NR1_N)) + 
  geom_bar() +
  geom_errorbar(
    aes(ymin = NR1_N - sd(NR1_N), ymax = NR1_N + sd(NR1_N)),
    width = 0.2
  ) +
  scale_x_binned(n.breaks = 10) + 
  ggtitle('Plot of BDNF_N vs NR1_N by Bimal Parajuli by 20BDS0405')

# Output:

 

# Stacked bar plots:
# Code:

# Stacked bar chart

ggplot(barplot_dataset2, 
       aes(x = SYP_N, 
           fill = Behavior)) + 
  geom_bar() +
  labs(x = "measure of SYP_N", 
       y = "Number of records", 
       fill = "Behavior") +
  ggtitle('Stacked Barplot of no. of records of different classes and behaviour by Bimal Parajuli (20BDS0405)') +
  scale_x_binned()

# Output:





# 2.	Scatter Plots

# With Shape empty/blank diamond


# Code:

scatter_dataset = select(dataset, c('DYRK1A_N', 'ITSN1_N', 'BDNF_N'))
scatter_dataset <- drop_na(scatter_dataset)

scatter_dataset <- scatter_dataset %>% 
                    mutate(
                      BDNF_N_quartile = as.character(ntile(
                        BDNF_N, n = 4))
)

ggplot(data = scatter_dataset,
       aes(x=DYRK1A_N,
           y=ITSN1_N,
           color = BDNF_N_quartile
           )
       ) + 
  geom_point(shape=23, size = 2) +
  scale_colour_brewer(palette = "Greens") +
  scale_x_log10() + 
  scale_y_log10() + 
  labs( x="Measure of BYRK1A_N", y="Measure of ITSN1_N", color="BDNF_N\nQuartiles") +
  ggtitle('Plot of DYRK1a_N vs ITSN1_N by Bimal Parajuli (20BDS0405)')






# Output:


# With shape filled 180 degree rotated triangle
# Code:
ggplot(data = scatter_dataset,
       aes(x=DYRK1A_N,
           y=ITSN1_N,
           color = BDNF_N_quartile
       )) + 
  geom_point(shape=17, size = -2) +
  scale_x_log10() + 
  scale_y_log10() + 
  labs(x = "Measure of DYRK1A_N", y="Measure of ITSN1_N", color = "BDNF_N\nQuartiles") +
  ggtitle('Plot of DYRK1a_N vs ITSN1_N by Bimal Parajuli (20BDS0405)') +
  scale_color_brewer(type = "div")

# Output:
 
# 3.	Heat-Map

# With Scalar
# Code:
# With Scalar
ggplot(
  dataset,
  aes(
    x=ITSN1_N,
    y=BDNF_N
  )
) + geom_tile(aes(fill=class)) + scale_y_binned() + scale_x_binned() + 
  ggtitle("Heatmap of BDNF_N and ITSN1_N by Bimal Parajuli (20BDS0405)")

# Output:
 

# With Divergence
# Code:
# With divergence

ggplot(
  head(dataset, 25),
  aes(
    x=ITSN1_N,
    y=BDNF_N
  )
) + geom_tile(aes(fill=factor(ITSN1_N), color = factor(BDNF_N))) + scale_y_binned() + scale_x_binned() + 
  ggtitle("Heatmap of BDNF_N and ITSN1_N by Bimal Parajuli (20BDS0405)")

# Output:
 
# 4.	3D-Piechart
# Code:
# 3D pie chart
library(plotrix, pie3D)
pie_data <- select(dataset, 'class')
pie_data <- na.omit(pie_data)

aaaaa <- pie_data %>% group_by(class) %>% count()
x_123 <- aaaaa$n
y_123 <- aaaaa$class

pie3D(x=x_123, 
      labels = y_123, 
      shade = 0.5, 
      border = "white", 
      theta = pi/4, 
      main = "Pie Chart of class atribute by Bimal Parajuli (20BDS0405)",
      explode = 0.15
      
)

# Output:



# 5.	Dashboard Using Looker Studio

# Link to Looker DashBoard: https://lookerstudio.google.com/reporting/4286d2ce-8c2c-4b09-a28a-87d67c1c1368/page/r84FD

# Dataset Used: Flight Passengers Data (From Moodle)

 






 # nolint






# Assignment 4:

# Market Basket Analysis:

# Code and Visualizations:
library(arules)
library(arulesViz)


# Load the Market Basket Optimization dataset and convert the data to a sparse matrix
df_trans = read.transactions(file = "Market_Basket_Optimisation.csv",
                              sep = ",",
                              rm.duplicates = T)

itemFrequencyPlot(df_trans,
topN=20,
type="absolute")
 
# Perform the apriori algorithm to find association rules
rules = apriori(data = df_trans,
                parameter = list(support = 0.004,
                                 confidence = 0.2))

plot(rules, method="graph")

 




# Sort the rules by lift and display the top 10 rules
top_rules = sort(rules, by = 'lift')[1:10]
inspect(top_rules)

# Output:
 


# Create a scatter plot of the support and confidence of the rules
plot(top_rules, 
     method = "scatterplot", 
     measure = c("support", "confidence"),
     main = "Confidence vs Support for top 10 rules by Bimal Parajuli 20BDS0405")


# Output:
 

# Create a matrix plot of the rules
plot(top_rules, 
method = "matrix", 
measure = "lift", 
shading = "confidence")

# Output:
 








# Create a network plot of the rules
plot(top_rules, 
method = "graph", 
control = list(type = "items"))

# Output:
 




# Mall Customer Clustering:

# Code and screenshots:
# Load libraries
library(tidyverse)
library(cluster)

# Load data
mall_data <- read.csv("Mall_Customers.csv")

# Explore data
head(mall_data)
summary(mall_data)

# Select relevant columns
mall_data_select <- select(mall_data, -CustomerID, -Gender)

# Scale the data
mall_data_scale <- scale(mall_data_select)

# Determine optimal number of clusters using elbow method
wss <- sapply(1:10, function(k){kmeans(mall_data_scale, k, nstart = 10 )$tot.withinss})
plot(1:10, wss, type="b", xlab="Number of Clusters", ylab="Within groups sum of squares")
 

# Fit K-means model with 5 clusters
k <- 5
set.seed(123)
kmeans_fit <- kmeans(mall_data_scale, centers = k, nstart=25)

# Add cluster labels to data
mall_data_select$cluster <- as.factor(kmeans_fit$cluster)

# Visualize clusters using scatter plot
ggplot(mall_data_select, aes(x=Annual.Income..k.., y=Spending.Score..1.100., color=cluster)) +
  geom_point() +
  scale_color_manual(values=c("blue", "red", "green", "purple", "orange")) +
  labs(title = "Mall Customer Clustering",
       x = "Annual Income (k$)",
       y = "Spending Score (1-100)")


 

# Visualize clusters using parallel coordinate plot
library(GGally)
ggparcoord(mall_data_select, columns = c(1,2,3), groupColumn = 5) + 
  labs(title = "Mall Customer Clustering",
       x = "Attribute",
       y = "Value")



# Text based Sentiment Analysis:

# Code and visualizations:


#1. Load shakespeare.rda into R environment
load('shakespeare.rda')




#2. Pipe the shakespeare data frame to the next line
# Use count to find out how many titles/types there are

library(dplyr)
shakespeare %>%
  count(type)

shakespeare %>% 
  count(title)

 






#3. Load tidytext/tidyverse
library(tidytext)
library(tidyverse)





#4. Create an object tidy_shakespeare
# Group by the titles of the playsa
# Define a new column line number
# Transform the non-tidy text data to tidy text data
tidy_shakespeare <- shakespeare %>%
  group_by(title) %>%
  mutate(line = row_number()) %>%
  unnest_tokens(word, text)





#5. Pipe the tidy Shakespeare data frame to the next line
# Use count to find out how many times each word is used
tidy_shakespeare %>%
  count(word) 





#6. Sentiment analysis of tidy_shakespeare assign to object shakespeare_sentiment
# Implement sentiment analysis with the "bing" lexicon
shakespeare_sentiment <- tidy_shakespeare %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  group_by(title, sentiment) %>%
  summarise(count = n()) %>%
  pivot_wider(names_from = "sentiment", values_from = "count", values_fill = 0)

 


#7. shakespeare_sentiment
# Find how many positive/negative words each play has
shakespeare_sentiment %>%
  group_by(title) %>%
  summarise(total_positive = sum(positive),
            total_negative = sum(negative))


 

#8. Tragedy or comedy from tidy_shakespeare assign to sentiment_counts
# Implement sentiment analysis using the "bing" lexicon
# Count the number of words by title, type, and sentiment
sentiment_counts <- tidy_shakespeare %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(word,title, sentiment, sort = TRUE)

 

#9. From sentiment_counts
# Group by the titles of the plays
# Find the total number of words in each play
# Calculate the number of words divided by the total
# Filter the results for only negative sentiment then arrange percentages in ASC order
sentiment_counts %>%
  group_by(title) %>%
  mutate(total_words = sum(n)) %>%
  filter(sentiment == "negative") %>%
  mutate(percentage = n/total_words*100) %>%
  arrange(percentage)

 

#10. Most common positive and negative words and assign to word_counts
# Implement sentiment analysis using the "bing" lexicon
# Count by word and sentiment
word_count <- tidy_shakespeare %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(word, sentiment, sort = TRUE)

 



#11. Extract the top 10 words from word_counts and assign to top_words
# Group by sentiment
# Take the top 10 for each sentiment and ungroup it
# Make word a factor in order of n
top_words <- word_count %>%
  group_by(sentiment) %>%
  top_n(10, n) %>%
  ungroup() %>%
  mutate(word = factor(word, levels = rev(unique(word))))

 

#12. Use aes() to put words on the x-axis and n on the y-axis
# Make a bar chart with geom_col()
# facet_wrap for sentiments and apply scales as free
# Move x to y and y to x

library(ggplot2)
ggplot(top_words, 
       aes(x = word, 
           y = n, 
           fill = sentiment)
       ) + 
  geom_col() +
  ggtitle("Barplots of most repeated words and their sentiments by Bimal Parajuli (20BDS0405)")

 






ggplot(top_words, 
       aes(x = word, 
           y = n, 
           fill = sentiment)
) + 
  geom_col() +
  facet_wrap(vars(sentiment)) +
  ggtitle("Barplots with facet_wrap by Bimal Parajuli (20BDS0405)")


 








# Moving x to y and y to x with coord_flip()
ggplot(top_words, 
       aes(x = word, 
           y = n, 
           fill = sentiment)
) + 
  geom_col() +
  facet_wrap(vars(sentiment)) +
  coord_flip() +
  ggtitle("Barplots with facet_wrap and coord_flip by Bimal Parajuli (20BDS0405)")


 




13. 

# Load required libraries
library(tidyverse)
library(tm)
library(wordcloud)
library(SnowballC)
library(tidytext)



# Create word cloud
layout(matrix(c(1, 2), nrow=2), heights=c(1, 4))
par(mar=rep(0, 4))
plot.new()
text(x=0.5, y=0.5, "Shakespeare wordcloud by Bimal Parajuli (20BDS0405)")
wordcloud(words = word_freq$word, 
          freq = word_freq$n, 
          min.freq = 50,
          max.words=200, 
          random.order=FALSE, 
          rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


 

# Count by title and word
word_count <- tidy_shakespeare %>%
  count(title, word, sort = TRUE) 



# Implement sentiment analysis using the "afinn" lexicon
afinn <- get_sentiments("afinn")
sentiment_score <- tidy_shakespeare %>%
  inner_join(afinn) %>%
  group_by(title) %>%
  summarize(sentiment = sum(value)) 



# Create a contribution score
contribution_score <- word_count %>%
  inner_join(sentiment_score, by = "title") %>%
  mutate(contribution = n * sentiment) %>%
  arrange(desc(contribution))

 
# Shiny Application using Gapminder Dataset:

# I have deployed the application at:
# https://bimalparajuli.shinyapps.io/Gapminder-Visualization_Bimal-20BDS0405/

# Code and Screenshots:
library(shiny)
library(dplyr)
library(gapminder)
library(plotly)

ui <- fluidPage(
  
  # Application title
  titlePanel("GapMinder Visualization by Bimal Parajuli - 20BDS0405"),
  
  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins",
                  "Number of bins:",
                  min = 1,
                  max = 200,
                  value = 30)
    ),
    
    # Show plots of the generated distribution
    mainPanel(
      plotOutput("distPlot"),
      plotlyOutput("pieChart")
    )
  )
)

server <- function(input, output, session) {
  
  output$distPlot <- renderPlot({
    
    # generate bins based on input$bins from ui.R
    x <- as.data.frame(gapminder::gapminder) %>% filter(year == '1952') %>% select ('pop')
    x <- x$pop
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    # draw the histogram with the specified number of bins
    hist(x, breaks = bins, col = 'darkred', border = 'white',
         xlab = 'Number of people',
         main = 'Population Distribution')
    
  })
  
  output$pieChart <- renderPlotly({
    
    # create a new data frame with continent-wise population data
    continent_pop <- gapminder %>% filter(year == '1952') %>% group_by(continent) %>% 
      summarise(total_pop = sum(pop))
    
    # calculate percentage of world population by continent
    continent_pop$percent_pop <- continent_pop$total_pop/sum(continent_pop$total_pop)*100
    
    # create a pie chart using plotly
    plot_ly(continent_pop, labels = ~continent, values = ~percent_pop, type = 'pie',
            text = ~paste(round(percent_pop, 2), '%')) %>%
      layout(title = "Percentage of World's Population by Continent (1952)")
    
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)

 













# Another visualization containing a Bar-plot and a histogram:

library(shiny)
library(dplyr)
library(gapminder)

# Define UI for application that draws a histogram and barplot
ui <- fluidPage(
  
  # Application title
  titlePanel("GapMinder Visualization by Bimal Parajuli - 20BDS0405"),
  
  # Sidebar with inputs for number of bins and attribute for barplot
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins",
                  "Number of bins:",
                  min = 1,
                  max = 200,
                  value = 30),
      selectInput("bar_attr", "Attribute for barplot:",
                  choices = c("gdpPercap", "lifeExp", "pop"),
                  selected = "gdpPercap")
    ),
    
    # Show a plot of the generated distribution and barplot
    mainPanel(
      plotOutput("distPlot"),
      plotOutput("barPlot")
    )
  )
)

# Define server logic for the histogram and barplot
server <- function(input, output, session) {
  
  # Render histogram
  output$distPlot <- renderPlot({
    
    # Generate bins based on input$bins from ui.R
    x <- as.data.frame(gapminder::gapminder) %>% filter(year == '1952') %>% select ('pop')
    x <- x$pop
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    # Draw the histogram with the specified number of bins
    hist(x, breaks = bins, col = 'darkred', border = 'white',
         xlab = 'Number of people',
         main = 'Population Distribution')
    
  })
  
  # Render barplot
  output$barPlot <- renderPlot({
    
    # Subset data by selected attribute
    data <- as.data.frame(gapminder::gapminder) %>% 
      filter(year == '1952') %>% 
      select(country, input$bar_attr) %>% 
      arrange(desc(input$bar_attr)) %>% 
      head(10)
    
    # Draw the barplot
    barplot(data[,2], names.arg = data[,1], 
            col = 'darkred', border = 'white',
            ylim = c(0, max(data[,2])*1.2),
            xlab = 'Country',
            ylab = input$bar_attr,
            main = paste0('Top 10 Countries by ', input$bar_attr))
    
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)



 
Time Series Analysis of Flight Customer Dataset:

Code and Screenshots:

data(AirPassengers) 
AirPassengers 
str(AirPassengers) 
class(AirPassengers) 

#Check for missing values 
sum(is.na(AirPassengers)) 

start(AirPassengers) 
end(AirPassengers) 
frequency(AirPassengers) 

summary(AirPassengers) 

# par(mfrow=c(3,3)) 
plot(AirPassengers, main = "Plot of AirPassengers over time by Bimal Parajuli 20BDS0405") 

 

plot.ts(AirPassengers, main = "Plot of AirPassengers over time by Bimal Parajuli 20BDS0405") 
# This will fit in a line 
abline(reg=lm(AirPassengers~time(AirPassengers)), main = "Plot with regression line of AirPassengers over time by Bimal Parajuli 20BDS0405") 
 

#This will print the cycle across years 
cycle(AirPassengers) 


#Step 3: Make it stationary 


#stationary means there should be consitant mean and variance 
plot(log(AirPassengers), main = "Log scale Plot of AirPassengers over time by Bimal Parajuli 20BDS0405")
 















plot(diff(log(AirPassengers)), main = "Diferential Plot of log scale of AirPassengers over time by Bimal Parajuli 20BDS0405") 


 



















#This will aggregate the cycles and display a year on year trend 
plot(aggregate(AirPassengers,FUN=mean), main = "Plot of average AirPassengers over time by Bimal Parajuli 20BDS0405") 
 















#Box plot across months will give us a sense on seasonal effect 
boxplot(AirPassengers~cycle(AirPassengers), main = "BoxPlot of AirPassengers over 12 months by Bimal Parajuli 20BDS0405") 
 














plot(diff(log(AirPassengers))) 
#Time Series Decomposition 
#Decomposition break data into trend, seasonal, regular and random 
plot(decompose(AirPassengers))
title(sub = "Decomposed Plots of AirPassengers over time by Bimal Parajuli 20BDS0405")
 



# time series decomposition 
#The above figure shows the time series decomposition into trend, seasonal and random (noise) . It is clear that the time series is non-stationary (has random walks) because of seasonal effects and a trend (linear trend). 














#Step 5: Model Identification and Estimation 
#Autocorrelation function and partial autocorrelation function to determine value of p and q 
#AR I MA - Auto Regression Moving Average Integration 
#p d q 
acf(AirPassengers)
title(sub ="ACF Plots of AirPassengers over time by Bimal Parajuli 20BDS0405")

 









acf(diff(log(AirPassengers))) 
title(sub ="ACF Plots of differentials of log scale of AirPassengers over time by Bimal Parajuli 20BDS0405")


 











pacf(diff(log(AirPassengers))) 
title(sub ="ACF Plots of differentials of log scale of AirPassengers over time by Bimal Parajuli 20BDS0405")

 






#It determine value of p (value we got as 0) 
#d is number of time you do the differentiations to make the mean 
#We do diff only one time so value of d is 1 
plot(diff(log(AirPassengers)))





#Stepn 6: ARIMA Model Prediction 
fit <- arima(log(AirPassengers),c(0,1,1),seasonal = 
               list(order=c(0,1,1),period=12)) 
fit 
#Predict for next 10 years 
pred <- predict(fit,n.ahead=10*12) #10 years * 12 months 
pred 
#2.718 is e value and round them to 0 decimal 
pred1<-round(2.718^pred$pred,0) 
pred1 #give op of 1960 to 1970 
#plot this model 
#line type (lty) can be specified using either text ("blank", "solid", "dashed", "dotted", "dotdash", "longdash", "twodash") or number (0, 1, 2, 3, 4, 5, 6). Note that lty = "solid" is identical to lty=1. 

ts.plot(AirPassengers,
        pred1,
        log="y",
        lty=c(1,3),
        main = "Predictions over next 10 years by Bimal parajuli 20BDS0405") 

 


#Compare predicted values with original values 

#Get only 1961 values 
data1<-head(pred1,12) 
data1 


#Predicted Values 
predicted_1960 <- round(data1)#head of Predicted 
predicted_1960 


#Original 
original_1960 <- tail(AirPassengers,12) #tail of original 
original_1960 


#Lets Test this Model we are going to take a dataset till 1959, and then we predict value of 1960, then validate that 1960 from alredy existing value we have it in dataset #Recreate model till 1959 

datawide <- ts(AirPassengers, frequency = 12, start=c(1949,1), end=c(1959,12)) 
datawide 


#Create model 
fit1 <- arima(log(datawide),c(0,1,1),seasonal = list(order=c(0,1,1),period=12)) 

pred <- predict(fit1,n.ahead=10*12) # predictfor now 1960 to 1970 
pred1<-2.718^pred$pred 
pred1 
#give op of 1960 to 1970 

data11=round(head(pred1,12),0) #head of Predicted 
data22=round(tail(AirPassengers,12),0) #tail of original 


plot(data11,col="red", type="l", main = "Bimal Parajuli 20BDS0405") 
lines(data22,col="blue") 
 






#Step 7: Check normality using Q-Q plot 
#qqnorm is a generic function the default method of which produces a normal QQ plot of the values in y. qqline adds a line to a “theoretical”, by default normal, quantile-quantile plot which passes through the probs quantiles, by default the first and third quartiles. 
qqnorm(residuals(fit)) 
title(sub = "Normal Q-Q plot by Bimal Parajuli")

qqline(residuals(fit)) 
title(sub = "Normal Q-Q plot by Bimal Parajuli")

 



"""
