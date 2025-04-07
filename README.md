# MSc_ASDS_Dissertation_Burg

Project starts with 1_imageMetadataScrapeFinal
  This was used to scrape the images and metadata from the OpenElections Webpage

Then the files from clusterFiles follow, these are the scripts ran on HPC to generate an overall dataset

Files then processed in 2_text_analysis-AfterClusterdfCreation
  This code file uses data_0307.csv and leaflet_details.csv
  Files are then cleaned and sorted_full_df_july2.csv is created (changed name later to the final dataset sorted_full_df_july4_5.csv (pretty sure I did this on the cluster and that is what causes the weird name differences)

3_floodsagain and 4_new_mapstuff I am pretty sure are then next in the workflow, floodsagain relies on shapefile data, new_mapstuff is used with geocoder and meteostat
  4_new_mapstuff yields simple_df.csv

3_floodsagain uses:
  Administrative_Areas___Environment_Agency_and_Natural_England.shp"
  westminster-parliamentary-constituencies.shp"
  202404 Historic Flood Warnings - EA.xlsx"


5_dataset_creation.R uses simple_df.csv to merge in census and control data as well as the flood data
  This file yields model_data.csv AND final_merged_clean_1707.csv (model data comes after overall dataset creation)

6_models.R uses model_data.csv to run the models for the report

7_plots_for_paper is used for graphics in the paper
