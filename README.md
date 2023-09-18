# AirQuality-HF
The Importance of Incorporating Air Quality for Predicting 30-day Hospital Readmission for Patients with Heart Failure


## Repository Structure

- [AHRQ_unions_intersections.xlsx](./AHRQ_unions_intersections.xlsx)
- 
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
