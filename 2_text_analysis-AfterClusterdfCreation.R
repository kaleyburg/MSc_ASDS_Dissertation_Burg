

#set wd for current folder
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
getwd()

rm(list=ls())

## Load packages
pkgTest <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[,  "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg,  dependencies = TRUE)
  sapply(pkg,  require,  character.only = TRUE)
}

#stmBrowser package from github
if(!require(devtools)) install.packages("devtools")
library(devtools)
install_github("mroberts/stmBrowser",dependencies=TRUE)

lapply(c("tidyverse",
         "quanteda",
         "quanteda.textstats",
         "lubridate",
         "stm",
         "wordcloud",
         "stmBrowser",
         "LDAvis"),
       pkgTest)

library(dplyr)

#import dataset of scraped leaflets
dat <- read.csv("C:\\Users\\kburg\\OneDrive\\Documents\\Trinity\\diss_all_other\\data_0307.csv")

#metadata for leaflets
leaf <- read.csv("C:\\Users\\kburg\\OneDrive\\Documents\\Trinity\\diss_all_other\\leaflet_details.csv")


#change all column names to match
dat$Leaflet.Number <- dat$Leaflet_Number 
dat$ElectionParty <- dat$Folder 
dat$Text <- dat$Content


#combine text for each Leaflet.Number while keeping ElectionYear and other relevant columns
new_df <- dat %>%
  group_by(Leaflet.Number, ElectionParty) %>%
  summarise(
    CombinedText = paste(Text, collapse = " "),
    .groups = 'drop'
  )


# erge leaflet scraping with the metadata
merged_df <- merge(leaf, new_df, by = "Leaflet.Number", all.x = TRUE)


#gets rid of missing cases
merged_df <- merged_df[complete.cases(merged_df), ]


#now making the corpus
corp <- corpus(merged_df, 
               docid_field = "Leaflet.Number",
               text_field = "CombinedText")


#prepping things

source("C:\\Users\\kburg\\OneDrive\\Documents\\Trinity\\diss_all_other\\qta\\pre_processing.R")

#prepped_toks <- prep_toks(corp) # basic token cleaning
#collocations <- get_coll(prepped_toks) # get collocations
#toks <- tokens_compound(prepped_toks, pattern = collocations[collocations$z > 10,]) # replace collocations
#super_stops <- c("said", # drop some additional common stopwords
#                 "say",
 #                "also")
#toks <- tokens_remove(toks, super_stops,
 #                     valuetype = "glob")
#toks <- tokens_remove(tokens(toks), "") # let's also remove the whitespace placeholders

#toks <- tokens(toks, 
 #              remove_numbers = TRUE,
  #             remove_punct = TRUE,
   #            remove_symbols = TRUE,
    #           remove_separators = TRUE,
     #          remove_url = TRUE) # remove other uninformative text



# Tokenize each document's CombinedText from all columns
tokens_list <- lapply(docnames(corp), function(docname) {
  combined_text <- unlist(sapply(corp[[docname]], as.character))
  tokens(combined_text, what = "word", remove_punct = FALSE)
})

# Convert tokens_list to a DFM (Document Feature Matrix) if needed
#toks <- dfm(tokens_list)

toks <- tokens_list

# Print or inspect the tokens
#(toks)

# Find tokens related to document "2823"
tokens_2823 <- toks[[2823]]

# Print or inspect the tokens
tokens_2823

# Check if "climate" is mentioned
mentions_climate <- "climate" %in% tokens_2823

# Print the result
mentions_climate


leaflet_2823 <- merged_df[merged_df$Leaflet.Number == 2823, "CombinedText"]

# Print the CombinedText for leaflet 2823
print(leaflet_2823)



#this was getting the dictionary

#install.packages("remotes")
#remotes::install_github("kbenoit/quanteda.dictionaries")

#load the dictionaries
library("quanteda.dictionaries")

data(package = "quanteda.dictionaries")

# Load the LaverGarry dictionary
data("data_dictionary_LaverGarry", package = "quanteda.dictionaries")

# View the structure of the dictionary
str(data_dictionary_LaverGarry)

# View the first few entries in the dictionary
head(data_dictionary_LaverGarry)

#create LG to hold the necessary dictionary
LG <- data_dictionary_LaverGarry



##adding in more words --- add to cluster code


# new words for the 'CLIMATE' sub-category
new_words <- c("climate", "climate change", "global warming", "carbon emissions", "greenhouse gases")

#create a new dictionary object with the updated structure
new_dict <- dictionary(list(
  ENVIRONMENT = list(CLIMATE = new_words)
))

if (!is.null(LG)) {
  new_dict <- c(LG, new_dict)
}


LG <- new_dict

#new_dict' has updated 'ENVIRONMENT' category with 'CLIMATE' sub-category and relevant words.


###

#getting topic count proportions

lg <- unlist(LG, use.names = FALSE)

#convert to lowercase to ensure case insensitivity
lg <- tolower(lg)

#filter tokens using the dictionary
toks_filtered2 <- tokens_select(toks, pattern = lg, selection = "keep")

#convert the tokens back to text format
texts <- as.character(toks_filtered_tokens)

#flatten the dictionary
flatten_dict <- function(dict) {
  flat_dict <- list()
  for (key in names(dict)) {
    if (is.list(dict[[key]])) {
      flat_dict[[key]] <- unlist(dict[[key]], recursive = TRUE, use.names = FALSE)
    } else {
      flat_dict[[key]] <- dict[[key]]
    }
  }
  return(flat_dict)
}

#flatten the dictionary
flat_LG <- flatten_dict(LG)

#convert to quanteda dictionary object
flat_LG_dict <- dictionary(flat_LG)

#lookup tokens in the dictionary
topic_counts <- tokens_lookup(toks_filtered_tokens, dictionary = flat_LG_dict, levels = 1)

#convert counts to a dataframe
topic_counts_df <- convert(dfm(topic_counts), to = "data.frame")


#merge topic_proportions_df with merged_df
topiccountdf <- merge(merged_df, topic_counts_df, by.x = "Leaflet.Number", by.y = "doc_id")

#save dataset
write.csv(topiccountdf, file = "sorted_full_df_july2.csv", row.names = FALSE)
df <- read.csv('sorted_full_df_july2.csv')


# Print the merged dataframe
print(merged_result)


