#######
#SETUP
####

#fixed with new data, now models are fine
#fixed the plots now

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
#install.packages("lfe")
library(lfe)  
#import data


df <- read.csv("CSVandSHPfiles/model_data_revision2.csv")
raw_dat <- read.csv("CSVandSHPfiles/sorted_full_df_july4_5.csv")
#test <- read.csv('CSVandSHPfiles/final_merged_clean_230425.csv')

final_merged = df

#checking names
colnames(final_merged)
colnames(raw_dat)
#colnames(test)

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


colnames(final_merged)

final_merged <- final_merged[!duplicated(final_merged), ]


# Check range of outcome variable
range(final_merged$environment_word_pct)

# Check variance in Party and vote shares
party_variance <- final_merged %>%
  group_by(Party) %>%
  summarise(Variance = var(environment_word_pct, na.rm = TRUE))

vote_share_variance <- final_merged %>%
  summarise(across(ends_with("_share"), var, na.rm = TRUE))

print("Variance by Party:")
print(party_variance)

print("Variance in Vote Shares:")
print(vote_share_variance)

# Define predictors WITHOUT constituency, since it is used only for indexing in plm
predictors <- c("Party", "election", "Median_Age", 
                "Rural_Prop", "Urban_Prop", 
                "Working_Class_Prop", "Intermediate_Prop", "Professional_Prop", 
                "Total_Student_Pct",
                "overall_weather_std",
                "lib_share",
                "lab_share",                  
                "oth_share",
                "con_share")

# Define outcome
outcome <- "environment_word_pct"

# ----------------------
# Create regression data for Model 1 & 2 (NO constituency)
regression_data_no_constituency <- final_merged %>%
  select(all_of(predictors), all_of(outcome)) %>%
  distinct()  # remove exact duplicates

# ----------------------
# Model 1: OLS (no fixed effects)
model <- lm(as.formula(paste(outcome, "~ .")), data = regression_data_no_constituency)
summary(model)


# ----------------------
# Model 2: Fixed Effects on election year only
model_time_fixed <- plm(
  environment_word_pct ~ Party + Median_Age + Rural_Prop + Urban_Prop + 
    Working_Class_Prop + Intermediate_Prop + Professional_Prop + 
    Total_Student_Pct + overall_weather_std + 
    lib_share + lab_share + oth_share + con_share,
  data = regression_data_no_constituency,
  index = c("election"),
  model = "within",
  effect = "time"
)
summary(model_time_fixed)

# ----------------------
# Model 3: Two-way Fixed Effects (election + constituency)


# Define regression_data including constituency
regression_data <- final_merged %>%
  select(all_of(predictors), all_of(outcome), constituency) %>%
  distinct()  # remove exact duplicates

model_two_way_fixed <- felm(
  environment_word_pct ~ Party |
    election + constituency, # fixed effects here
  data = regression_data
)

summary(model_two_way_fixed)



# Create a list to store models for each party
party_models <- list()

# Loop through each party and fit a fixed effects model using regression_data_no_constituency
for (party in levels(regression_data_no_constituency$Party)) {
  # Filter data for the current party
  party_data <- regression_data_no_constituency %>% filter(Party == party)
  
  # Fit the fixed effects model with time (election year) fixed effects
  model_party <- plm(
    environment_word_pct ~ Median_Age + Rural_Prop + Urban_Prop + 
      Working_Class_Prop + Intermediate_Prop + Professional_Prop + 
      Total_Student_Pct + overall_weather_std + lab_share + lib_share +
      oth_share + con_share,
    data = party_data,
    index = c("election"),
    model = "within",
    effect = "time"
  )
  
  # Store the model in the list with the party name as the key
  party_models[[party]] <- model_party
}

# Print summaries of the models for each party
for (party in names(party_models)) {
  cat("Model for Party:", party, "\n")
  print(summary(party_models[[party]]))
  cat("\n")
}


#stargazer

#stargazer for the models for each party
stargazer(party_models, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Fixed Effects Models for Each Party with Election-Year Controls",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE,
          column.labels = names(party_models),  # Use party names as column labels
          dep.var.labels = "Mean Environmental Mentions")  # Label for the dependent variable
#stargazer for the main model
# Create the LaTeX table for the main model
stargazer(model, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Main Model with Election-Year Controls",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE,
          dep.var.labels = "Mean Environmental Mentions")  # Label for the dependent variable
#stargazer for the two-way fixed effects model
# Create the LaTeX table for the two-way fixed effects model
stargazer(model_two_way_fixed, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Two-Way Fixed Effects Model with Election-Year and Constituency Controls",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE,
          dep.var.labels = "Mean Environmental Mentions")  # Label for the dependent variable
#stargazer for the model with only time fixed effects
# Create the LaTeX table for the model with only time fixed effects
stargazer(model_time_fixed, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Fixed Effects Model with Election-Year Controls (Time Only)",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE,
          dep.var.labels = "Mean Environmental Mentions")  # Label for the dependent variable
#stargazer for the model with two-way fixed effects
# Create the LaTeX table for the model with two-way fixed effects
stargazer(model_two_way_fixed, 
          type = "latex",  # Change to "latex" or "html" as needed
          title = "Fixed Effects Model with Election-Year Controls (Time and Constituency)",
          omit.stat = c("f", "ser"),  # Omit F-statistic and residual std. error
          digits = 3,
          no.space = TRUE,
          dep.var.labels = "Mean Environmental Mentions")  # Label for the dependent variable





#stargazer things for simple models


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



# ----- breakdown of leaflets by party and year -----

#making a table of the combined text sorted by party and year and constit


leaflet_summary <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(Total_Leaflets = sum(environment), .groups = 'drop')  

# Print the summary table
print(leaflet_summary)


#now recalculate these columns below
# Calculate total leaflets by year
total_leaflets_by_year <- raw_dat %>%
  group_by(Election) %>%
  summarise(Total_Leaflets = sum(environment), .groups = 'drop')
# Calculate leaflets by party and year
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

# sorted desc stats by env as a total percentage of the text


count_by_year_env <- raw_dat %>%
  filter(environment > 0) %>%
  group_by(Election) %>%
  summarise(Count = n(), .groups = 'drop')
# Count occurrences of each party by year for environmental mentions
count_by_party_and_year_env <- raw_dat %>%
  filter(environment > 0) %>%
  group_by(Election, Party) %>%
  summarise(Count = n(), .groups = 'drop')

count_by_year_env
count_by_party_and_year_env


# Columns representing issues
issue_columns <- c("culture", "economy", "environment", "groups", "institutions", "law_and_order", "rural", "urban", "values")


#counting percentages of text for each category using raw data lenght to do so

#add the issue percent by year variable
issue_percent_by_year_party <- raw_dat %>%
  group_by(Election, Party) %>%
  summarise(across(all_of(issue_columns), ~ sum(.x, na.rm = TRUE) / sum(environment, na.rm = TRUE) * 100, .names = "percent_{col}"), .groups = 'drop')  



issue_percent_table <- issue_percent_by_year_party %>%
  mutate(total = rowSums(across(starts_with("percent_")), na.rm = TRUE)) %>%
  mutate(across(starts_with("percent_"), ~ . / total * 100)) %>%
  select(-total)

# Reshape for stargazer or kable
issue_percent_table_long <- issue_percent_table %>%
  pivot_longer(cols = starts_with("percent_"), names_to = "Issue", values_to = "Percent") %>%
  mutate(Issue = gsub("percent_", "", Issue))

# Wide format for table
issue_percent_table_wide <- issue_percent_table_long %>%
  pivot_wider(names_from = Issue, values_from = Percent)

# Output as LaTeX table for appendix
stargazer(issue_percent_table_wide, type = "latex", summary = FALSE,
          title = "Percentage of Leaflet Text by Issue, Party, and Year (Sums to 100%)",
          out = "tex_files_withallimagesandbib/issue_percent_table.tex")

# 1. Plot: Standard deviation of environmental mentions by constituency
# Calculate standard deviation of environment_word_pct by constituency for each party
env_sd_by_constituency_party <- final_merged %>%
  group_by(Party, constituency) %>%
  summarise(
    sd_environment_word_pct = sd(environment_word_pct, na.rm = TRUE),
    mean_environment_word_pct = mean(environment_word_pct, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) %>%
  arrange(Party, desc(sd_environment_word_pct))

# Plot the standard deviation for each party (black and white, publication style)
ggplot(env_sd_by_constituency_party, aes(x = reorder(constituency, -sd_environment_word_pct), y = sd_environment_word_pct, fill = Party)) +
  geom_col(color = "black") +
  facet_wrap(~ Party, scales = "free_x") +
  scale_fill_grey(start = 0.3, end = 0.8) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Standard Deviation of Environmental Mentions by Constituency and Party",
    x = "Constituency (sorted within Party)",
    y = "SD of Environmental Mentions (%)"
  ) +
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    legend.position = "none",
    plot.title = element_text(size = 16, face = "bold"),
    axis.title.x = element_text(size = 14),
    axis.title.y = element_text(size = 14),
    strip.text = element_text(size = 12)
  )
ggsave("tex_files_withallimagesandbib/plots/sd_env_mentions_by_constituency_party_bw.png", width = 12, height = 6, dpi = 300)

# 2. Table: Top 3 issues by party (black and white, formatted for publication)
top3_issues_by_party <- issue_percent_table_long %>%
  group_by(Party, Issue) %>%
  summarise(mean_percent = mean(Percent, na.rm = TRUE), .groups = "drop") %>%
  group_by(Party) %>%
  slice_max(order_by = mean_percent, n = 3) %>%
  arrange(Party, desc(mean_percent))

# Output as LaTeX table for appendix
stargazer(
  top3_issues_by_party,
  type = "latex",
  summary = FALSE,
  title = "Top 3 Issues by Party (Average Percentage Across Years)",
  rownames = FALSE,
  digits = 2,
  out = "tex_files_withallimagesandbib/top3_issues_by_party_bw.tex"
)
# Output as LaTeX table for appendix
stargazer(issue_percent_table_wide, type = "latex", summary = FALSE,
  title = "Full Breakdown: Percentage of Leaflet Text by Issue, Party, and Year",
  out = "tex_files_withallimagesandbib/full_issue_breakdown_appendix.tex")

# Stacked Issue Composition by Party and Year (colorblind-friendly palette)
ggplot(issue_percent_table_long, aes(x = Party, y = Percent, fill = Issue)) +
  geom_bar(
  stat = "identity", 
  position = "fill", 
  color = "black"
  ) +
  facet_wrap(~ Election) +
  scale_fill_viridis_d(option = "D") +  # Use a colorblind-friendly palette
  theme_minimal(base_size = 12) +
  labs(title = "Issue Composition by Party and Year (100% Stacked)", x = "Party", y = "Proportion of Leaflet Text") +
  theme(
  axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
  panel.grid.major.y = element_line(color = "grey80", linetype = "dashed"),
  panel.grid.minor = element_blank(),
  strip.background = element_rect(fill = "grey90", color = NA),
  legend.position = "bottom",  # Move legend to the bottom for better readability
  legend.title = element_text(size = 12),
  legend.text = element_text(size = 10)
  )
ggsave("tex_files_withallimagesandbib/plots/stacked_issue_composition_colorblind_friendly.png", width = 14, height = 8, dpi = 300)

