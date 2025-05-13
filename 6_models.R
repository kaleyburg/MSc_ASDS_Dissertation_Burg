#######
#SETUP
####


getwd()
setwd('C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg')
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

df <- read.csv("CSVandSHPfiles/model_data_revision.csv")
raw_dat <- read.csv("CSVandSHPfiles/sorted_full_df_july4_5.csv")

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

#Descriptive stats graphs and things

colnames(raw_dat)

# Calculate the total number of leaflets by year
total_leaflets_by_year <- raw_dat %>%
  group_by(Election) %>%
  summarise(Total_Leaflets = sum(environment), .groups = 'drop')

# Calculate the number of leaflets by party for each year
leaflets_by_party_and_year <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(Total_Leaflets = sum(environment), .groups = 'drop')

# Check data frames
print(total_leaflets_by_year)
print(leaflets_by_party_and_year)

# Create a summary table for total leaflets by year
stargazer(total_leaflets_by_year, 
          type = "latex", 
          title = "Total Number of Leaflets by Year", 
          summary = FALSE, 
          out = "tex_files_withallimagesandbib/total_leaflets_by_year.tex")

# Create a summary table for leaflets by party and year
stargazer(leaflets_by_party_and_year, 
          type = "latex", 
          title = "Number of Leaflets by Party and Year", 
          summary = FALSE, 
          out = "tex_files_withallimagesandbib/leaflets_by_party_and_year.tex")

#other descriptive stats

# Count occurrences of each year
count_by_year <- raw_dat %>%
  group_by(Election) %>%
  summarise(Count = n(), .groups = 'drop')

# Count occurrences of each party by year
count_by_party_and_year <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(Count = n(), .groups = 'drop')

# Output LaTeX table for count by year
stargazer(count_by_year, 
          type = "latex", 
          title = "Count of Observations by Year", 
          summary = FALSE, 
          out = "tex_files_withallimagesandbib/count_by_year.tex")

# Output LaTeX table for count by party and year
stargazer(count_by_party_and_year, 
          type = "latex", 
          title = "Count of Observations by Party and Year", 
          summary = FALSE, 
          out = "tex_files_withallimagesandbib/count_by_party_and_year.tex")

# Columns representing issues
issue_columns <- c("culture", "economy", "environment", "groups", "institutions", "law_and_order", "rural", "urban", "values")

# Summarize total mentions for each issue by party and year
issue_mentions <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(across(all_of(issue_columns), sum, .names = "total_{.col}"), .groups = 'drop')

# Calculate the total mentions for all issues combined for each party and year
issue_mentions <- issue_mentions %>%
  mutate(total_mentions = rowSums(across(starts_with("total_")), na.rm = TRUE))

# Calculate the percentage of mentions for each issue
issue_mentions <- issue_mentions %>%
  mutate(across(starts_with("total_"), ~ . / total_mentions * 100, .names = "percent_{.col}"))

# Remove the percent_total_mentions column if it exists
if ("percent_total_mentions" %in% colnames(issue_mentions)) {
  issue_mentions <- issue_mentions %>%
    select(-percent_total_mentions)
}

# Identify the most mentioned issue by percentage for each party and year
most_mentioned_issue <- issue_mentions %>%
  rowwise() %>%
  mutate(most_mentioned = names(which.max(c_across(starts_with("percent_total_"))))) %>%
  ungroup()

# Correcting the assignment of most_mentioned
most_mentioned_issue <- issue_mentions %>%
  rowwise() %>%
  mutate(most_mentioned = issue_columns[which.max(c_across(starts_with("percent_total_")))]) %>%
  ungroup()

# Select relevant columns
most_mentioned_issue <- most_mentioned_issue %>%
  select(Election, Party, most_mentioned)

# Print the result
print(most_mentioned_issue)

# List unique election years
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
    out = paste0("tex_files_withallimagesandbib/issue_mentions_", year, ".tex")
  )
}

# Prepare the data for stargazer
env_percentage_table <- issue_mentions %>%
  select(Election, Party, percent_total_environment) %>%
  arrange(Election, Party)

# Output LaTeX table using stargazer
stargazer(
  env_percentage_table,
  type = "latex",
  title = "Percentage of Environment Mentions by Party and Year",
  summary = FALSE,
  rownames = FALSE,
  out = "tex_files_withallimagesandbib/environment_mentions_percentage.tex"
)

# Ensure the plots directory exists
if (!dir.exists("tex_files_withallimagesandbib/plots")) {
  dir.create("tex_files_withallimagesandbib/plots", recursive = TRUE)
}

#graphs

# Plot for percentage of environment mentions by party and year (black and white, publication style)
ggplot(env_percentage_table, aes(x = Party, y = percent_total_environment, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  scale_fill_grey(start = 0.3, end = 0.8) +
  theme_minimal(base_size = 14) +
  labs(title = "Percentage of Environment Mentions by Party and Year",
       x = "Party",
       y = "Percentage") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold"))

output_path <- "tex_files_withallimagesandbib/plots/env_mentions_percentage_bw.png"
ggsave(output_path, width = 12, height = 8, dpi = 300)
cat("Saved plot to:", output_path, "\n")

# Plot for count of observations total each election (black and white, publication style)
ggplot(count_by_year, aes(x = Election, y = Count, fill = Election)) +
  geom_bar(stat = "identity", color = "black") +
  scale_fill_grey(start = 0.3, end = 0.8) +
  theme_minimal(base_size = 14) +
  labs(title = "Total Count of Observations by Election",
       x = "Election Year",
       y = "Total Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold"))

output_path <- "tex_files_withallimagesandbib/plots/total_count_by_election_bw.png"
ggsave(output_path, width = 12, height = 8, dpi = 300)
cat("Saved plot to:", output_path, "\n")

# Plot for count of environment mentions by party and year (black and white, publication style)
env_count_table <- issue_mentions %>% 
  select(Election, Party, total_environment) %>% 
  arrange(Election, Party)

ggplot(env_count_table, aes(x = Party, y = total_environment, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  scale_fill_grey(start = 0.3, end = 0.8) +
  theme_minimal(base_size = 14) +
  labs(title = "Count of Environment Mentions by Party and Year",
       x = "Party",
       y = "Count") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold"))

output_path <- "tex_files_withallimagesandbib/plots/env_mentions_count_bw.png"
ggsave(output_path, width = 12, height = 8, dpi = 300)
cat("Saved plot to:", output_path, "\n")

# Plot for total mentions of any topic by party and year (black and white, publication style)
total_mentions_table <- issue_mentions %>% 
  select(Election, Party, total_mentions) %>% 
  arrange(Election, Party)

ggplot(total_mentions_table, aes(x = Party, y = total_mentions, fill = Election)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  scale_fill_grey(start = 0.3, end = 0.8) +
  theme_minimal(base_size = 14) +
  labs(title = "Total Mentions of Any Topic by Party and Year",
       x = "Party",
       y = "Total Mentions") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold"))

output_path <- "tex_files_withallimagesandbib/plots/total_mentions_by_party_year_bw.png"
ggsave(output_path, width = 12, height = 8, dpi = 300)
cat("Saved plot to:", output_path, "\n")
