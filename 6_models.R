#######
#SETUP
####


getwd()
setwd('C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg/CSVandSHPfiles')
rm(list = ls())


#PACKAGES

library(tidyr)
library(dplyr)
library(lubridate)
library(stargazer)
library(tidyverse)
library(RColorBrewer) 
library(plm)


#import data

df <- read.csv("model_data_revision.csv")

final_merged = df

#checking names
colnames(final_merged)



#conversion to factor variables
final_merged$Party <- as.factor(final_merged$Party)
final_merged$election <- as.factor(final_merged$election)
final_merged$Classification <- as.factor(final_merged$Classification)

#relevel parties to make the Green Party the reference level
final_merged$Party <- relevel(final_merged$Party, ref = " Green Party")

#check levels to make sure it worked
levels(final_merged$Party)

head(final_merged)

#mltiply all columns ending with '_share' by 100 to make interpretation easier
final_merged <- final_merged %>%
  mutate(across(ends_with("_share"), ~ . * 100))

#setting predictors
predictors <- c("Party", "election", "Median_Age", 
                "Total_Rural_Population", "Total_Urban_Population", 
                "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations", 
                "Small_Employers", "Lower_Supervisory", "Semi_Routine", 
                "Routine_Occupations", "Never_Worked", 
                "Long_Term_Unemployed", "Total_Students_Count",
                "overall_weather_std",
                "lib_share",
                "lab_share",                  
                "oth_share",
                "con_share"
)

#setting outcome
outcome <- "mean_environmental_mentions"


#running model
regression_data <- final_merged %>%
  select(all_of(predictors), all_of(outcome))

#perform regression
model <- lm(as.formula(paste(outcome, "~ .")), data = regression_data)

summary(model)


# Fixed Effects Model with only time (election years) fixed effects
model_time_fixed <- plm(
  mean_environmental_mentions ~ Party + Median_Age + Total_Rural_Population + Total_Urban_Population + 
  Higher_Managerial + Lower_Managerial + Intermediate_Occupations + Small_Employers + Lower_Supervisory + 
  Semi_Routine + Routine_Occupations + Never_Worked + Long_Term_Unemployed + Total_Students_Count + 
  overall_weather_std + lib_share + lab_share + oth_share + con_share,
  data = final_merged,
  index = c("election"), # Panel data index, with election years
  model = "within", # 'within' is fixed effects
  effect = "time"  # This specifies we are controlling for time (election year) fixed effects
)

# Summary of the model
summary(model_time_fixed)




# Two-way Fixed Effects Model (both election year and constituency)
model_two_way_fixed <- plm(
  mean_environmental_mentions ~ Party, 
  data = final_merged,
  index = c("election", "constituency"), # Panel data index, with both election years and constituencies
  model = "within", # 'within' is fixed effects
  effect = "twoways"  # Control for both time (election years) and constituency fixed effects
)

# Summary of the model
summary(model_two_way_fixed)


stargazer(model)

# Create the LaTeX table for the model with only time fixed effects
stargazer(model_time_fixed, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Fixed Effects Model with Election-Year Controls (Time Only)",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE)


# Create the LaTeX table for the model with only time fixed effects
stargazer(model_two_way_fixed, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Fixed Effects Model with Election-Year Controls (Time and Constituency)",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE)

