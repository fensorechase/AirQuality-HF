# AirQuality-HF
The Importance of Incorporating Air Quality for Predicting 30-day Hospital Readmission for Patients with Heart Failure

## Python Packages
- numpy==1.25.2
- pandas==2.0.0
- pymongo==4.5.0
- scikit_learn==1.3.0
- shap==0.42.1
- tqdm==4.65.0
- xgboost==1.7.6

## R Requirements
- RStudio Version 2023.06.1+524 (2023.06.1+524)

## Repository Structure

- [AHRQ_unions_intersections.xlsx](./AHRQ_unions_intersections.xlsx): lists feature names within the AHRQ SDOHD dataset at the county and census tract levels. The intersections and unions of county and census tract feature names from 2009-2020 are given.
- [Air_Quality_ALL_FEAT_NAMES.csv](./Air_Quality_ALL_FEAT_NAMES.csv): lists names and descriptions of air quality features within (i) AHRQ SDOHD databse (ii) EPA AQS database. Note that both sets of features are from the US EPA, but the two databases include different features.
- [requirements.txt](./requirements.txt): includes packages and corresponding versions required to run Python scripts
- **data handling:**
  - **COUNTY_AHRQ:**
    - [y_ahrq_COUNTY_clean_data_baselines.Rmd](./data%20handling/COUNTY_AHRQ/y_ahrq_COUNTY_clean_data_baselines.Rmd)
    - [y_GAonly_AQS_COUNTY_iterative_clean_merge_data.Rmd](./data%20handling/COUNTY_AHRQ/y_GAonly_AQS_COUNTY_iterative_clean_merge_data.Rmd)
    - [y_national_AQS_COUNTY_iterative_clean_merge_data.Rmd](./data%20handling/COUNTY_AHRQ/y_national_AQS_COUNTY_iterative_clean_merge_data.Rmd)
  - **TRACT_AHRQ:**
    - [ahrq_censustract_feat_categories.csv](./data%20handling/TRACT_AHRQ/ahrq_censustract_feat_categories.csv)
    - [ahrq_tract_categories_dedup.csv](./data%20handling/TRACT_AHRQ/ahrq_tract_categories_dedup.csv)
    - [y_ahrq_build_categories.Rmd](./data%20handling/TRACT_AHRQ/y_ahrq_build_categories.Rmd)
    - [y_ahrq_TRACT_clean_data_baselines.Rmd](./data%20handling/TRACT_AHRQ/y_ahrq_TRACT_clean_data_baselines.Rmd)
    - [y_AQI_iterative_clean_merge_data.Rmd](./data%20handling/TRACT_AHRQ/y_AQI_iterative_clean_merge_data.Rmd)
    - [y_generate_feat_plots.Rmd](./data%20handling/TRACT_AHRQ/y_generate_feat_plots.Rmd)
  - [feat_base.json](./data%20handling/feat_base.json)
  - [feat_column.json](./data%20handling/feat_column.json)
  - [subgroup_cols.json](./data%20handling/subgroup_cols.json)
  - [y_agnostic_sgs_generate_plots_model_result.Rmd](./data%20handling/y_agnostic_sgs_generate_plots_model_result.Rmd)
  - [y_AQI_noniterative_clean_merge_data.Rmd](./data%20handling/y_AQI_noniterative_clean_merge_data.Rmd)
  - [y_generate_subgroup_statistics.Rmd](./data%20handling/y_generate_subgroup_statistics.Rmd)
  - [y_merge_all_feats.Rmd](./data%20handling/y_merge_all_feats.Rmd)
  - [y_data_cleaners.R](./data%20handling/y_data_cleaners.R)

- **scripts model building:**
  - [evalHelper.py](./scripts%20model%20building/evalHelper.py)
  - [sgs_analyze_baseline.py](./scripts%20model%20building/sgs_analyze_baseline.py)
  - [sgs_evaluate_baselines.py](./scripts%20model%20building/sgs_evaluate_baselines.py)

AHRQ SDOHD
## Running the Code
1. Download the following public social determinants of health (SDOH) datasets used during preprocessing:
 - [https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html](AHRQ SDOHD): (Years 2009-2020)
 - [EPA AQS]([[url](https://aqs.epa.gov/aqsweb/airdata/download_files.html)]): (Years 2009-2020)
 - [ADI]([[url](https://www.neighborhoodatlas.medicine.wisc.edu/)]): (Year 2015)
 - [SVI]([url](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html)): (Year 2014)
 - [SDI]([[url](https://www.graham-center.org/maps-data-tools/social-deprivation-index.html)]): (Year 2015)
3. Data handling (R): With your own patient data including binary 30-day hospital readmission labels, enter the **data handling** directory.
4. Scripts model building (Python): Given the preprocessed data, run [sgs_evaluate_baselines.py](./scripts model building%20model%20building/sgs_evaluate_baselines.py) to train models. Results will be saved to user-specified MongoDB collection.
5. Model results summary (Python): Once models have finished running and results are stored in the MongoDB collection, run [sgs_analyze_baseline.py](./scripts model building%20model%20building/sgs_analyze_baseline.py)

