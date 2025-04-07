#######
#SETUP
####



setwd('C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other')
rm(list = ls())


#PACKAGES

library(tidyr)
library(dplyr)
library(lubridate)
library(stargazer)
library(tidyverse)
library(RColorBrewer) 


#import data

df <- read.csv("model_data.csv")

#removing duplicates and renaming to match code
df <- unique(df)
final_merged = df

#checking names
colnames(final_merged)

#conversion to factor variables
final_merged$Party <- as.factor(final_merged$Party)
final_merged$Election <- as.factor(final_merged$Election)
final_merged$Classification <- as.factor(final_merged$Classification)
final_merged$election_year <- as.factor(final_merged$election)

#relevel parties to make the Green Party the reference level
final_merged$Party <- relevel(final_merged$Party, ref = " Green Party")

#check levels to make sure it worked
levels(final_merged$Party)


#mltiply all columns ending with '_share' by 100 to make interpretation easier
final_merged <- final_merged %>%
  mutate(across(ends_with("_share"), ~ . * 100))

#setting predictors
predictors <- c("Party", "election_year", "Median_Age", 
                "Total_Rural_Population", "Total_Urban_Population", 
                "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations", 
                "Small_Employers", "Lower_Supervisory", "Semi_Routine", 
                "Routine_Occupations", "Never_Worked", 
                "Long_Term_Unemployed", "Total_Students_Count",
                "yearly_avg_tavg",                   
                "yearly_avg_tmin",                  
                "yearly_avg_tmax",                   
                "yearly_avg_prcp",                   
                "yearly_avg_wspd",                   
                "yearly_avg_pres",                   
                "yearly_avg_tsun",
                "lib_share",
                "lab_share",                  
                "oth_share",
                "con_share",
                "Flood.Alert",
                "Flood.Warning",
                "Severe.Flood.Warning",
                "Flood.Watch"
)

#setting outcome
outcome <- "environment"


#running model
regression_data <- final_merged %>%
  select(all_of(predictors), all_of(outcome))

#perform regression
model <- lm(environment ~ ., data = regression_data)

summary(model)


#models by year

#split data into each year
data_2010 <- final_merged %>% filter(election_year == 2010)
data_2015 <- final_merged %>% filter(election_year == 2015)
data_2017 <- final_merged %>% filter(election_year == 2017)
data_2019 <- final_merged %>% filter(election_year == 2019)


#set predictors and outcome
predictors2 <- c("Party", "Median_Age", 
                "Total_Rural_Population", "Total_Urban_Population", 
                "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations", 
                "Small_Employers", "Lower_Supervisory", "Semi_Routine", 
                "Routine_Occupations", "Never_Worked", 
                "Long_Term_Unemployed", "Total_Students_Count",
                "yearly_avg_tavg",                   
                "yearly_avg_tmin",                  
                "yearly_avg_tmax",                   
                "yearly_avg_prcp",                   
                "yearly_avg_wspd",                   
                "yearly_avg_pres",                   
                "yearly_avg_tsun",
                "lib_share",
                "lab_share",                  
                "oth_share",
                "con_share",
                "Flood.Alert",
                "Flood.Warning",
                "Severe.Flood.Warning",
                "Flood.Watch"
)
outcome2 <- "environment"

#Function to run regressions and summaries
run_model <- function(data, year) {
  regression_data <- data %>%
    select(all_of(predictors2), all_of(outcome2))
  
  model <- lm(environment ~ ., data = regression_data)
  
  cat("\nSummary for model of election year", year, ":\n")
  print(summary(model))
  return(model)
}

#Run each model
model_2010 <- run_model(data_2010, 2010)
model_2015 <- run_model(data_2015, 2015)
model_2017 <- run_model(data_2017, 2017)
model_2019 <- run_model(data_2019, 2019)

#view results
summary(model_2010)
summary(model_2015)
summary(model_2017)
summary(model_2019)


#now for each party



#split by party
data_conservative <- final_merged %>% filter(Party == " Conservative Party")
data_labour <- final_merged %>% filter(Party == " Labour Party")
data_libdem <- final_merged %>% filter(Party == " Liberal Democrats")
data_green <- final_merged %>% filter(Party == " Green Party")
data_ukind <- final_merged %>% filter(Party == " UK Independence Party")


#predictors and outcome variable setting
predictors3 <- c("election_year", "Median_Age", 
                "Total_Rural_Population", "Total_Urban_Population", 
                "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations", 
                "Small_Employers", "Lower_Supervisory", "Semi_Routine", 
                "Routine_Occupations", "Never_Worked", 
                "Long_Term_Unemployed", "Total_Students_Count",
                "yearly_avg_tavg",                   
                "yearly_avg_tmin",                  
                "yearly_avg_tmax",                   
                "yearly_avg_prcp",                   
                "yearly_avg_wspd",                   
                "yearly_avg_pres",                   
                "yearly_avg_tsun",
                "lib_share",
                "lab_share",                  
                "oth_share",
                "con_share",
                "Flood.Alert",
                "Flood.Warning",
                "Severe.Flood.Warning",
                "Flood.Watch"
)

outcome3 <- "environment"

#function to run models for the party data
run_model <- function(data, party) {
  regression_data <- data %>%
    select(all_of(predictors3), all_of(outcome3))
  
  model <- lm(environment ~ ., data = regression_data)
  
  cat("\nSummary for model of party", party, ":\n")
  print(summary(model))
  return(model)
}

#running models
model_conservative <- run_model(data_conservative, "Conservative Party")
model_labour <- run_model(data_labour, "Labour Party")
model_libdem <- run_model(data_libdem, "Liberal Democrats")
model_green <- run_model(data_green, "Green Party")
model_ukind <- run_model(data_ukind, " UK Independence Party")

summary(model_conservative)
summary(model_labour)
summary(model_libdem)
summary(model_green)
summary(model_ukind)


#stargazer code


main_model <- model


#main model

stargazer(
  main_model,
  type = "latex",
  title = "Main Model Results",
  omit.stat = c("LL", "ser", "f"),
  single.row = TRUE,
  font.size = "footnotesize",
  digit.separator = "",
  digits = 2,
  out = "main_model_results.tex"
)



#year
stargazer(
  model_2010, model_2015, model_2017, model_2019,
  type = "latex",
  title = "Models Divided by Year",
  omit.stat = c("LL", "ser", "f"),
  single.row = TRUE,
  font.size = "footnotesize",
  digit.separator = "",
  digits = 2,
  out = "models_by_year_results.tex"
)


#party

stargazer(
  model_conservative, model_labour, model_libdem, model_green, model_ukind,
  type = "latex",
  title = "Models Divided by Party",
  omit.stat = c("LL", "ser", "f"),
  single.row = TRUE,
  font.size = "footnotesize",
  digit.separator = "",
  digits = 2,
  out = "models_by_party_results.tex"
)



#descriptive stats for paper

raw_dat <- read.csv("cluster/sorted_full_df_july2.csv")

colnames(raw_dat)

#occurrences for each year
count_by_year <- raw_dat %>%
  group_by(Election) %>%
  summarise(Count = n(), .groups = 'drop')

#occurrences of each party by year
count_by_party_and_year <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(Count = n(), .groups = 'drop')


#LaTeX table for count by year
stargazer(count_by_year, 
          type = "latex", 
          title = "Count of Observations by Year", 
          summary = FALSE, 
          out = "count_by_year.tex")

#LaTeX table for count by party and year
stargazer(count_by_party_and_year, 
          type = "latex", 
          title = "Count of Observations by Party and Year", 
          summary = FALSE, 
          out = "count_by_party_and_year.tex")




#showing most mentioned issues by year and party


issue_columns <- c("culture", "economy", "environment", "groups", "institutions", "law_and_order", "rural", "urban", "values")

#total mentions for each issue by party and year
issue_mentions <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(across(all_of(issue_columns), sum, .names = "total_{.col}"), .groups = 'drop')

#total mentions for all issues combined for each party and year
issue_mentions <- issue_mentions %>%
  mutate(total_mentions = rowSums(across(starts_with("total_")), na.rm = TRUE))


issue_mentions <- issue_mentions %>%
  mutate(across(starts_with("total_"), ~ . / total_mentions * 100, .names = "percent_{.col}"))


if ("percent_total_mentions" %in% colnames(issue_mentions)) {
  issue_mentions <- issue_mentions %>%
    select(-percent_total_mentions)
}


most_mentioned_issue <- issue_mentions %>%
  rowwise() %>%
  mutate(most_mentioned = issue_columns[which.max(c_across(starts_with("percent_total_")))]) %>%
  ungroup()


most_mentioned_issue <- most_mentioned_issue %>%
  select(Election, Party, most_mentioned)


print(most_mentioned_issue)




#unique election years
election_years <- unique(issue_mentions$Election)

# Create a LaTeX table for each election year
for (year in election_years) {
  # Filter data for the specific election year
  year_data <- issue_mentions %>%
    filter(Election == year) %>%
    pivot_longer(cols = starts_with("percent_"), names_to = "Issue", values_to = "Percentage") %>%
    pivot_wider(names_from = Issue, values_from = Percentage) %>%
    arrange(Party)
  
  # Generate LaTeX table using stargazer
  stargazer(
    year_data,
    type = "latex",
    title = paste("Percentage of Mentions by Issue for Election Year", year),
    summary = FALSE,
    rownames = FALSE,
    out = paste0("issue_mentions_", year, ".tex")
  )
}



#stargazer
env_percentage_table <- issue_mentions %>%
  select(Election, Party, percent_total_environment) %>%
  arrange(Election, Party)

#LaTeX table using stargazer
stargazer(
  env_percentage_table,
  type = "latex",
  title = "Percentage of Environment Mentions by Party and Year",
  summary = FALSE,
  rownames = FALSE,
  out = "environment_mentions_percentage.tex"
)



#plots to show this better in paper


# Count of Observations by Year
ggplot(count_by_year, aes(x = Election, y = Count)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  theme_minimal() +
  labs(title = "Count of Observations by Year",
       x = "Election Year",
       y = "Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("count_by_year.png", width = 10, height = 6, dpi = 300)

# Count of Observations by Party and Year
ggplot(count_by_party_and_year, aes(x = Party, y = Count, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(x = "Party",
       y = "Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("count_by_party_year.png", width = 12, height = 8, dpi = 300)

#percentages



#stargazer
env_percentage_table <- issue_mentions %>%
  select(Election, Party, percent_total_environment) %>%
  arrange(Election, Party)

# LaTeX table using stargazer
stargazer(
  env_percentage_table,
  type = "latex",
  title = "Percentage of Environment Mentions by Party and Year",
  summary = FALSE,
  rownames = FALSE,
  out = "environment_mentions_percentage.tex"
)


#  plotting
env_mentions <- issue_mentions %>%
  select(Election, Party, percent_total_environment) %>%
  rename(percent_environment = percent_total_environment) %>%
  arrange(Election, Party)


ggplot(env_mentions, aes(x = Party, y = percent_environment, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(
    #title = "Percentage of Environment Mentions by Party and Year",
    x = "Party",
    y = "Percentage"
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.title = element_blank() # Optional: Removes legend title if not needed
  )


ggsave("env_mentions_percentage.png", width = 12, height = 8, dpi = 300)




#model with datasets for each party and year -----


#fcreate datasets based on unique party-year combinations
create_datasets <- function(final_merged) {
  unique_combinations <- unique(final_merged[, c("Party", "election")])
  for (i in 1:nrow(unique_combinations)) {
    # Extract party and election values
    party <- unique_combinations$Party[i]
    election <- unique_combinations$election[i]
    #name dataset
    dataset_name <- paste0("Dataset_", gsub(" ", "", party), "_", gsub(" ", "", election))
    #subset data
    subset_data <- final_merged[final_merged$Party == party & final_merged$election == election, ]
    if (nrow(subset_data) > 0) {
      #create new dataset
      assign(dataset_name, subset_data, envir = .GlobalEnv)
      print(head(subset_data))  # Print first few rows of the subset
      cat("\n------------------------\n\n")
    } else {
      cat("No data available for Party:", party, "and Election:", election, "\n\n")
    }
  }
}

#creating datasets
create_datasets(final_merged)

regression_results <- list()

#set predictors and outcome
predictors5 <- c("Median_Age", "Total_Rural_Population", "Total_Urban_Population",
                 "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations", 
                 "Small_Employers", "Lower_Supervisory", "Semi_Routine", 
                 "Routine_Occupations", "Never_Worked", 
                 "Long_Term_Unemployed",
                 "Total_Students_Count", "yearly_avg_tavg", "yearly_avg_tmin",
                 "yearly_avg_tmax", "yearly_avg_prcp", "yearly_avg_wspd",
                 "yearly_avg_pres", "yearly_avg_tsun", "lib_share", "lab_share",
                 "oth_share", "con_share", "Flood.Alert", "Flood.Warning",
                 "Severe.Flood.Warning", "Flood.Watch")
outcome5 <- "environment"


dataset_names <- ls(pattern = "^Dataset_")  # Get all dataset names starting with "Dataset_"


for (dataset_name in dataset_names) {
  data <- get(dataset_name)
  if (nrow(data) > length(predictors5)) {
    formula <- as.formula(paste(outcome5, "~", paste(predictors5, collapse = "+")))
    #run regression
    model <- lm(formula, data = data)
    # store model
    regression_results[[results_name]] <- model
    #print summary
    cat("Regression results for", dataset_name, ":\n")
    print(summary(model))
    cat("\n------------------------\n\n")
  } else {
    cat("Not enough data to run regression for", dataset_name, "\n\n")
  }
}


model_names <- names(regression_results)


for (model_name in model_names) {
  model <- regression_results[[model_name]]
  
  cat("Model Name:", model_name, "\n")
  
  print(summary(model))
  
  cat("\n------------------------\n\n")
}


#print only the names of models and their significant variables
print_significant_vars_simple <- function(regression_results, significance_level = 0.1) {

  if (!is.list(regression_results)) {
    stop("regression_results should be a list of model objects.")
  }
  
  for (model_name in names(regression_results)) {
    model <- regression_results[[model_name]]
    model_summary <- summary(model)
    coeff_table <- model_summary$coefficients
    if (!all(c("Estimate", "Pr(>|t|)") %in% colnames(coeff_table))) {
      next
    }
    significant_vars <- coeff_table[coeff_table[, "Pr(>|t|)"] < significance_level, , drop = FALSE]
    
  
    if (nrow(significant_vars) > 0) {
      cat("Model Name:", model_name, "\n")
      for (var_name in rownames(significant_vars)) {
        coef_value <- significant_vars[var_name, "Estimate"]
        p_value <- significant_vars[var_name, "Pr(>|t|)"]
        cat("Variable:", var_name, 
            "- Coefficient:", coef_value,
            "- p-value:", p_value, "\n")
      }
      cat("\n------------------------\n\n")
    }
  }
}

#printing the significant variables for each of these models
print_significant_vars_simple(regression_results)



#interaction effects model


model_int <- lm(environment ~ Party * election_year + 
                  Median_Age + 
                  Total_Rural_Population + 
                  Total_Urban_Population + 
                  Higher_Managerial + 
                  Lower_Managerial + 
                  Intermediate_Occupations + 
                  Small_Employers + 
                  Lower_Supervisory + 
                  Semi_Routine + 
                  Routine_Occupations + 
                  Never_Worked + 
                  Long_Term_Unemployed + 
                  Total_Students_Count +
                  yearly_avg_tavg +                   
                  yearly_avg_tmin +                  
                  yearly_avg_tmax +                   
                  yearly_avg_prcp +                   
                  yearly_avg_wspd +                   
                  yearly_avg_pres +                   
                  yearly_avg_tsun +
                  lib_share +
                  lab_share +                  
                  oth_share +
                  con_share +
                  Flood.Alert +
                  Flood.Warning +
                  Severe.Flood.Warning +
                  Flood.Watch,
                data = regression_data)


summary(model_int)

stargazer(
  model_int,
  type = "latex",
  title = "Interactive Model",
  omit.stat = c("LL", "ser", "f"),
  single.row = TRUE,
  font.size = "footnotesize",
  digit.separator = "",
  digits = 2,
  out = "intmodel.tex"
)








#plots for the paper


#count of obs by year
ggplot(count_by_year, aes(x = Election, y = Count)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  theme_minimal() +
  labs(title = "Count of Observations by Year",
       x = "Election Year",
       y = "Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("count_by_year.png", width = 10, height = 6, dpi = 300)


#better colors and format


primary_colors <- c("red", "blue", "green", "yellow", "orange", "purple", "cyan")

ggplot(count_by_year, aes(x = Election, y = Count, fill = Election)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = Count), vjust = -0.3, size = 5) +  
  scale_fill_manual(values = primary_colors) +  
  labs(title = "Count of Observations by Year",
       x = "Election Year",
       y = "Count") +
  theme(
    plot.title = element_text(size = 16, face = "bold"), 
    axis.title.x = element_text(size = 14),  
    axis.title.y = element_text(size = 14),  
    axis.text.x = element_text(size = 12, angle = 45, hjust = 1),  
    axis.text.y = element_text(size = 12),  
    legend.text = element_text(size = 10),  
    legend.title = element_text(size = 12)  
  )


ggsave(filename = "count_by_year.png", width = 12, height = 8, dpi = 300) 






#count of Observations by Party and Year
ggplot(count_by_party_and_year, aes(x = Party, y = Count, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Count of Observations by Party and Year",
       x = "Party",
       y = "Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("count_by_party_year.png", width = 12, height = 8, dpi = 300)



#better colors and form


ggplot(count_by_party_and_year, aes(x = Party, y = Count, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Count of Observations by Party and Year",
       x = "Party",
       y = "Count") +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 12), 
    axis.title = element_text(size = 14),                     
    plot.title = element_text(size = 16, face = "bold"),          
    legend.text = element_text(size = 12),                       
    legend.title = element_text(size = 14),                      
    legend.position = "right"                                      
  ) +
  scale_fill_brewer(palette = "Set1")  


ggsave("count_by_party_year.png", width = 12, height = 8, dpi = 300)




