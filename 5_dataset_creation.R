###################
## This script creates the final dataset for analysis by merging various datasets, including census data, election results, and flood data. ####
## It also performs some data cleaning and transformation to ensure consistency and usability in subsequent analyses.   #####
####################

#R.home('bin')
#install.packages("IRkernel")
#IRkernel::installspec(user = FALSE)
#conda install jupyter



setwd("C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg/CSVandSHPfiles")
rm(list = ls())
df <- read.csv("data_withweather.csv")

head(df)

library(tidyr)
library(dplyr)
library(lubridate)
library(stargazer)



#adding in census data


#age census data
cens_age <- read.csv("cens_age.csv")
cens_educ <- read.csv("cens_educ.csv")

#socioeconomic status datasets
ses_fem <- read.csv("ses_fem.csv")
ses_male <- read.csv("ses_male.csv")

#rural-urban data
rural_urban <- read.csv("rural_urban.csv")

rural_urban$geography <- rural_urban$PCON11NM 

colnames(ses_fem)
colnames(ses_male)

convert_to_numeric <- function(df) {
  df %>%
    mutate(across(-c(date, geography, geography.code), as.numeric))
}

ses_fem <- convert_to_numeric(ses_fem)
ses_male <- convert_to_numeric(ses_male)


#merge datasets
merged_ses <- full_join(ses_fem, ses_male, by = c("date", "geography", "geography.code"))

#fixing x and y stuff
x_cols <- names(merged_ses)[grepl("\\.x$", names(merged_ses))]
y_cols <- names(merged_ses)[grepl("\\.y$", names(merged_ses))]

#base names
processed_base_names <- character()

#getting rid of x's and y columns
for (x_col in x_cols) {
  base_name <- sub("\\.x$", "", x_col)
  y_col <- paste0(base_name, ".y")
  if (y_col %in% y_cols) {
    merged_ses[[paste0(base_name, "_sum")]] <- rowSums(
      merged_ses[c(x_col, y_col)], na.rm = TRUE
    )
    processed_base_names <- c(processed_base_names, base_name)
  }
}

#remove original .x and .y columns
columns_to_remove <- c(paste0(processed_base_names, ".x"), paste0(processed_base_names, ".y"))
merged_ses <- merged_ses %>%
  select(-all_of(columns_to_remove))

#data frames to merge
dfs <- list(cens_age, cens_educ, merged_ses, rural_urban)

#merge all data frames by 'geography', specifying suffixes
census <- Reduce(function(x, y) merge(x, y, by = "geography", suffixes = c("", paste0("_", ncol(x)))), dfs)

print(head(census))
colnames(census)


#subsetting census dataset
census_selected <- census %>%
  rename(
    # General
    Date = date,
    Geography_Code = geography.code,
    Rural_Urban = Rural.Urban,
    constituency = geography,
    
    
    # Age
    All_Residents = `Age..All.usual.residents..measures..Value`,
    Age_0_4 = `Age..Age.0.to.4..measures..Value`,
    Age_5_7 = `Age..Age.5.to.7..measures..Value`,
    Age_8_9 = `Age..Age.8.to.9..measures..Value`,
    Age_10_14 = `Age..Age.10.to.14..measures..Value`,
    Age_15 = `Age..Age.15..measures..Value`,
    Age_16_17 = `Age..Age.16.to.17..measures..Value`,
    Age_18_19 = `Age..Age.18.to.19..measures..Value`,
    Age_20_24 = `Age..Age.20.to.24..measures..Value`,
    Age_25_29 = `Age..Age.25.to.29..measures..Value`,
    Age_30_44 = `Age..Age.30.to.44..measures..Value`,
    Age_45_59 = `Age..Age.45.to.59..measures..Value`,
    Age_60_64 = `Age..Age.60.to.64..measures..Value`,
    Age_65_74 = `Age..Age.65.to.74..measures..Value`,
    Age_75_84 = `Age..Age.75.to.84..measures..Value`,
    Age_85_89 = `Age..Age.85.to.89..measures..Value`,
    Age_90_Plus = `Age..Age.90.and.over..measures..Value`,
    Mean_Age = `Age..Mean.Age..measures..Value`,
    Median_Age = `Age..Median.Age..measures..Value`,
    
    # Qualifications
    All_Qualifications = `Qualifications..All.categories..Highest.level.of.qualification..measures..Value`,
    No_Qualifications = `Qualifications..No.qualifications..measures..Value`,
    Level_1_Qualifications = `Qualifications..Highest.level.of.qualification..Level.1.qualifications..measures..Value`,
    Level_2_Qualifications = `Qualifications..Highest.level.of.qualification..Level.2.qualifications..measures..Value`,
    Apprenticeship = `Qualifications..Highest.level.of.qualification..Apprenticeship..measures..Value`,
    Level_3_Qualifications = `Qualifications..Highest.level.of.qualification..Level.3.qualifications..measures..Value`,
    Level_4_and_Above = `Qualifications..Highest.level.of.qualification..Level.4.qualifications.and.above..measures..Value`,
    Other_Qualifications = `Qualifications..Highest.level.of.qualification..Other.qualifications..measures..Value`,
    School_Age_16_to_17 = `Qualifications..Schoolchildren.and.full.time.students..Age.16.to.17..measures..Value`,
    School_Age_18_and_Over = `Qualifications..Schoolchildren.and.full.time.students..Age.18.and.over..measures..Value`,
    Full_Time_Students_Employed = `Qualifications..Full.time.students..Age.18.to.74..Economically.active..In.employment..measures..Value`,
    Full_Time_Students_Unemployed = `Qualifications..Full.time.students..Age.18.to.74..Economically.active..Unemployed..measures..Value`,
    Full_Time_Students_Inactive = `Qualifications..Full.time.students..Age.18.to.74..Economically.inactive..measures..Value`,
    
    # Socioeconomic Classification
    NS_SeC_All = `NS.SeC..All.categories..NS.SeC..measures..Value_sum`,
    Higher_Managerial = `NS.SeC..1..Higher.managerial..administrative.and.professional.occupations..measures..Value_sum`,
    Lower_Managerial = `NS.SeC..2..Lower.managerial..administrative.and.professional.occupations..measures..Value_sum`,
    Intermediate_Occupations = `NS.SeC..3..Intermediate.occupations..measures..Value_sum`,
    Small_Employers = `NS.SeC..4..Small.employers.and.own.account.workers..measures..Value_sum`,
    Lower_Supervisory = `NS.SeC..5..Lower.supervisory.and.technical.occupations..measures..Value_sum`,
    Semi_Routine = `NS.SeC..6..Semi.routine.occupations..measures..Value_sum`,
    Routine_Occupations = `NS.SeC..7..Routine.occupations..measures..Value_sum`,
    Never_Worked_Unemployed = `NS.SeC..8..Never.worked.and.long.term.unemployed..measures..Value_sum`,
    Never_Worked = `NS.SeC..L14.1.Never.worked..measures..Value_sum`,
    Long_Term_Unemployed = `NS.SeC..L14.2.Long.term.unemployed..measures..Value_sum`,
    Full_Time_Students_NS_SeC = `NS.SeC..L15.Full.time.students..measures..Value_sum`,
    
    # Additional fields
    PCON11CD = PCON11CD,
    PCON11NM = PCON11NM,
    Total_Rural_Population = `Total.Rural.population.2011`,
    Urban_City_Town_Population = `Urban.City.and.Town.population.2011`,
    Urban_Minor_Conurbation_Population = `Urban.Minor.Conurbation.population.2011`,
    Urban_Major_Conurbation_Population = `Urban.Major.Conurbation.population.2011`,
    Total_Urban_Population = `Total.Urban.population.2011`,
    Total_Population = `Total.population.2011`,
    Hub_Towns_Population = `Hub.towns..rural.related..population.included.in.Urban.population.2011`,
    Rural_Hub_Towns_Population = `Rural.including.hub.towns..rural...rural.related..population.2011`,
    Rural_Population_Percentage = `Rural.including.hub.towns..rural...rural.related..population.as...of.Total.population.2011`,
    RUC11CD = RUC11CD,
    RUC11 = RUC11,
    Classification = `Broad.RUC11`
  ) %>%
  select(
    Geography_Code, constituency, Date, Rural_Urban, Median_Age, All_Residents, 
    All_Qualifications, No_Qualifications, Level_1_Qualifications, Level_2_Qualifications, 
    Apprenticeship, Level_3_Qualifications, Level_4_and_Above, Other_Qualifications, 
    School_Age_16_to_17, School_Age_18_and_Over, Full_Time_Students_Employed, 
    Full_Time_Students_Unemployed, Full_Time_Students_Inactive, NS_SeC_All, 
    Higher_Managerial, Lower_Managerial, Intermediate_Occupations, Small_Employers, 
    Lower_Supervisory, Semi_Routine, Routine_Occupations, Never_Worked_Unemployed, 
    Never_Worked, Long_Term_Unemployed, Full_Time_Students_NS_SeC, 
    Total_Rural_Population, Urban_City_Town_Population, Urban_Minor_Conurbation_Population, 
    Urban_Major_Conurbation_Population, Total_Urban_Population, Total_Population, 
    Hub_Towns_Population, Rural_Hub_Towns_Population, Rural_Population_Percentage, 
    RUC11CD, RUC11, Classification
  )


head(census_selected)

#remove duplicates
census_selected <- census_selected %>%
  distinct()

head(census_selected)




#now load election data

election_res <- read.csv("1918-2019election_results.csv")
head(election_res)


# subset by year and country
subset_election_res <- subset(election_res, election >= 2010 & election <= 2019)
subset_election_res$country.region
subset_election_res <- subset(subset_election_res, !country.region %in% c("Scotland", "Wales", "Northern Ireland"))
head(subset_election_res)


if(all(is.na(subset_election_res$natSW_votes)) && all(is.na(subset_election_res$natSW_share))) {
  subset_election_res <- subset_election_res[, !names(subset_election_res) %in% c("natSW_votes", "natSW_share")]
}

head(subset_election_res)

#change name for constistency and merging
colnames(subset_election_res)[which(colnames(subset_election_res) == "constituency_name")] <- "constituency"
subset_election_res$constituency <- tolower(subset_election_res$constituency)
head(subset_election_res)

#convert constituency names to lowercase in the census data frame
colnames(census_selected)[which(colnames(census_selected) == "geography")] <- "constituency"
census_selected$constituency <- tolower(census_selected$constituency)
head(census_selected)

#convert 'election_year' to Date format
df$election_year <- as.Date(df$Election.Date)

#extract year and assign it to a new column
df$election_year <- year(df$election_year)

df$full_elec_date = df$Election 
df$election = df$election_year

df$election <- as.character(df$election)
subset_election_res$election <- as.character(subset_election_res$election)


#merge df and subset_election_res
merged_df <- df %>%
  left_join(subset_election_res, by = c("election", "constituency"))

#change the column name and make values lowercase
census_selected <- census_selected %>%
  mutate(constituency = tolower(constituency))

#merge with census_selected
final_merged <- merged_df %>%
  left_join(census_selected, by = "constituency")


#save the CSV file
file_path <- "final_merged_clean_1707.csv"

# Save the dataframe final_merged as a CSV file
write.csv(final_merged, file = file_path, row.names = FALSE)

# Confirm the file has been saved
cat("CSV file saved at:", file_path, "\n")

#adding flood data

final_floods <- read.csv("final_floods.csv")
head(final_floods)
head(final_merged)

final_floods$pcon22nm <- tolower(final_floods$pcon22nm)


#merge flood data in
merged_data <- merge(final_floods, final_merged, by.x = "pcon22nm", by.y = "constituency", all = TRUE)


#cleaning flood data 

# names are lowercase for consistency
final_floods <- final_floods %>%
  rename(constituency = pcon22nm) %>%
  mutate(constituency = tolower(constituency))

final_merged <- final_merged %>%
  mutate(constituency = tolower(constituency))

#filter and aggregate flood data by election year and the previous year
floods_aggregated <- final_floods %>%
  left_join(final_merged, by = "constituency", relationship = "many-to-many") %>%
  filter(DATE == election_year | DATE == (election_year - 1)) %>%
  group_by(constituency, election_year, TYPE) %>%
  summarise(total_count = sum(count), .groups = 'drop')

#reshape data to have separate columns for each flood type
floods_wide <- floods_aggregated %>%
  pivot_wider(names_from = TYPE, values_from = total_count, values_fill = list(total_count = 0))

#merge with the original election data
model_data <- final_merged %>%
  left_join(floods_wide, by = c("constituency", "election_year"))


#create count variables
model_data <- model_data %>%
  mutate(
    Total_Students_Count = Full_Time_Students_Employed + Full_Time_Students_Unemployed + Full_Time_Students_Inactive
  )

colnames(model_data)



#saving data to use in models
model_data <- model_data[, c("constituency", "Party", "election", "Classification", "Median_Age", 
                              "Total_Rural_Population", "Total_Urban_Population", 
                              "Higher_Managerial", "Lower_Managerial", "Intermediate_Occupations",
                              "Small_Employers",
                              "Lower_Supervisory", "Semi_Routine", "Routine_Occupations", "Never_Worked_Unemployed",
                              "Never_Worked", "Long_Term_Unemployed",
                              "Total_Students_Count", "yearly_avg_tavg", "yearly_avg_tmin", 
                              "yearly_avg_tmax", "yearly_avg_prcp", "yearly_avg_wspd", 
                              "yearly_avg_pres", "yearly_avg_tsun", 
                              "Election", "country.region", "con_share", 
                              "lib_share", "lab_share", "oth_share", "environment",
                              "Flood Alert",                       
                              "Flood Warning",                    
                              "Update Flood Alert",                
                              "Update Flood Warning",              
                              "Severe Flood Warning",              
                              "Update Severe Flood Warning",       
                              "Flood Watch")]


model_data <- unique(model_data)

length(model_data)

write.csv(model_data, file = "model_data.csv", row.names = FALSE)



