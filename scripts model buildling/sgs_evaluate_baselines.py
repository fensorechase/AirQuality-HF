import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import argparse
from datetime import datetime
import json
import pandas as pd
from pymongo import MongoClient
import sklearn.ensemble as sken
from sklearn.linear_model import LogisticRegression
import sklearn.model_selection as skms
import sklearn.neighbors as skknn
import sklearn.neural_network as sknn
import sklearn.metrics as skm
import sklearn.tree as sktree
import tqdm
import urllib.parse
import xgboost as xgb
import numpy as np
# from sklearn.inspection import permutation_importance # For feature importance
import shap


from evalHelper import read_json, evaluate_results, get_train_test


# Note: KNN removed from this run.
# Also removed: dt, rf, mlp.
MODEL_PARAMS = {
   
    "xgboost": {
        "model": xgb.XGBClassifier(),
        "params": {"max_depth": [6,7,8],
                   "n_estimators": [10, 20, 30, 40],
                   "learning_rate":[0.01, 0.1],
                   "eval_metric":["logloss"]}
    },
     "rf": {
         'model': sken.RandomForestClassifier(),
         'params': {'max_depth': [5,6,7,8],
                    'min_samples_leaf': [5, 10],
                    'n_estimators': [5, 10, 25]}
    }
}


"""
Returns a Python list of all values from a json object, discarding the keys.
"""
def json_extract_values(obj):
    if isinstance(obj, dict):
        values = []
        for key, value in obj.items():
            values.extend(json_extract_values(value))
        return values
    elif isinstance(obj, list):
        return obj
    else:
        return []
    



def main():
    parser = argparse.ArgumentParser()
    # mongo information
    username = urllib.parse.quote_plus('__MONGO UN__')
    password = urllib.parse.quote_plus('__MONGO PW__')
    parser.add_argument("-mongo_url", default = '__MONGO LOCAL URL__') 
    parser.add_argument("-mongo_db",
                        default="__MOGNO DB NAME__")
    parser.add_argument("-mongo_col",
                        default="__MONGO COL NAME__",
                        help="collection_type") # Used to be subgroups_baseline
    # default information
    # Smaller sample, removed NAs: clean_tract_v2_ahrq.csv: includes select built env, mobility, air quality AHRQ data
    # AHRQ baseline year, removed NAs: clean_tract_v2_ahrq_baseline.csv
    # AHRQ all 30k samples, mean from 2009-2020: clean_tract_v2_ahrq_allsamps.csv
    # AHRQ all 30k samples, baseline year, imputation: clean_tract_v2_ahrq_all_samps_baseline.csv
    # Old input: final_clean_tract_ahrq_AQIimp1_baseline.csv
    parser.add_argument("-data_file", 
                        default="../data/9-6-total_feats.csv", 
                        help="data file") 
    parser.add_argument("-base_feat",
                        default="../data/feat_base.json",
                        help="base_features")
                        
    parser.add_argument("-feat_file", 
                        default="../data/feat_column.json",
                       help="model_features")
    parser.add_argument("-subgroup_file", 
                    default="../data/subgroup_cols.json",
                    help="subgroups_to_test")
    parser.add_argument("-endpoint",
                        default="readmit30bin")
    

    # See if adding AHRQ + EPA_AQS whether 
    #   or not the models would pick up 
    #   the EPA variables before the AHRQ EPAA ones


    # total county medianIMP AHRQ KEEP EPAA medianIMP + EPA_AQS
    # total county medianIMP AHRQ *minus* EPAA + EPA_AQS

    # "county_AHRQ_median_without_EPAA", # total w/o EPAA, already done.

    # total (includes EPAA) + EPA_AQS_median
    # total (includes EPAA) + EPA_AQS_spatial
    # total - EPAA + EPA_AQS_median
    # total - EPAA + EPA_AQS_spatial

    parser.add_argument("--feats", nargs='+', default=[
       

        "tot_county_AHRQ_median_w_EPAA_w_EPA_AQS_median", 
        "tot_county_AHRQ_median_w_EPAA_w_EPA_AQS_spatial",  
                "tot_county_AHRQ_median_w_EPAA_spatial_w_EPA_AQS_spatial",

        
        "tot_county_AHRQ_median_without_EPAA_w_EPA_AQS_median",  
        "tot_county_AHRQ_median_without_EPAA_w_EPA_AQS_spatial", 

        "county_medianIMP_ahrq_1_socialcontext",
            "county_medianIMP_ahrq_2_economiccontext", 
            "county_medianIMP_ahrq_3_education",
            "county_medianIMP_ahrq_4_physicalinfrastructure",
            "county_medianIMP_ahrq_5_healthcarecontext",
        "tract_medianIMP_ahrq_1_socialcontext",
            "tract_medianIMP_ahrq_2_economiccontext",
            "tract_medianIMP_ahrq_3_education",
            "tract_medianIMP_ahrq_4_physicalinfrastructure",
            "tract_medianIMP_ahrq_5_healthcarecontext",


        "hf_with_charlson_AND_tot_county_AHRQ_median",
        "hf_with_charlson_AND_tot_county_AHRQ_median_without_EPAA_or_EPA_AQS",
        "hf_with_charlson_AND_tot_county_AHRQ_median_w_EPAA_w_EPA_AQS_median",
        "hf_with_charlson_AND_tot_county_AHRQ_median_without_EPAA_w_EPA_AQS_median",



        "county_AHRQ_median_without_EPAA",
        "county_AHRQ_mean_without_EPAA",

        "intersect_county_AHRQ_median",
        "intersect_tract_AHRQ_median",

        "intersect_county_AHRQ_median_w_EPAA_spatial",
        "intersect_tract_AHRQ_median_w_EPAA_spatial",

        "intersect_county_AHRQ_median_w_EPA_AQS_spatial",
        "intersect_tract_AHRQ_median_w_EPA_AQS_spatial",

        "tot_county_AHRQ_median",



        "tot_county_AHRQ_mean",
        "tot_tract_AHRQ_median",
        "tot_tract_AHRQ_mean"
        
        ])
    
    """

    
    Additional feature sets run: 

        "age_current",
        "sex",
        "demo",
        "hf_vars",
        "comorb",
        "hf_with_comorb",
        "demo_comorb",
        "charlson",
        "hf_with_charlson",

        "adi_national", "adi_state", 
        "sdi", "sdi_score", 
        "svi",



        "EPA_AQS_median",
        "EPA_AQS_mean",
        "EPA_AQS_spatial",

        "AHRQ_EPAA_median",
        "AHRQ_EPAA_mean",
        "AHRQ_EPAA_spatial",


        "county_AHRQ_median_without_EPAA",
        "county_AHRQ_mean_without_EPAA",


        "intersect_county_AHRQ_median",
        "intersect_tract_AHRQ_median",

        "intersect_county_AHRQ_median_w_EPAA_spatial",
        "intersect_tract_AHRQ_median_w_EPAA_spatial",

        "intersect_county_AHRQ_median_w_EPA_AQS_spatial",
        "intersect_tract_AHRQ_median_w_EPA_AQS_spatial",

        "tot_county_AHRQ_median",
        "tot_county_AHRQ_mean",
        "tot_tract_AHRQ_median",
        "tot_tract_AHRQ_mean"
    
    
    """
    



    args = parser.parse_args()

    # setup mongo
    mclient = MongoClient(args.mongo_url)
    mdb = mclient[args.mongo_db]
    mcol = mdb[args.mongo_col]
    raw_mcol = mdb["9_10_MLH_raw_agnostic"] # Used to be: "raw_baseline"
    logcoeffs_mcol = mdb["9_10_MLH_log_coeffs"] # To save logisitic coeffs.
    #logCI_mcol = mdb["9_10_MLH_log_CI"] # For 95% CI.
    shap_mcol = mdb["9_10_shap_xgb_MLH"] # To save shap for XGBoost.

    df = pd.read_csv(args.data_file)
    base_feat = read_json(args.base_feat)
    feat_info = read_json(args.feat_file)
    subgroups_bins = read_json(args.subgroup_file)

    # determine the feature sets
    feat_cols = {}
    for ft in args.feats:
        colset = set()
        # check if it's a base feature, if so update
        if ft in base_feat:
            colset.update(base_feat[ft])
        else:
            for ftbase in feat_info[ft]:
                colset.update(base_feat[ftbase])
        feat_cols[ft] = list(colset)

    # Determine subgroups within each subgroup bin:
    subgroups = json_extract_values(subgroups_bins)

    for i in tqdm.tqdm(range(1, 11), desc="test-split"):
        train_df, test_df, train_y, test_y = get_train_test(df, i, label=args.endpoint)
        # Reset test_df indices for subgroup indexing
        test_df = test_df.reset_index()

        
        for fname, fcolumns in tqdm.tqdm(feat_cols.items(),
                                         desc="feats", leave=False):
            base_res = {
                "file": args.data_file,
                "feat": fname,
                "endpoint": args.endpoint,
                "fold": i
            }

            # for both train and test get only those columns
            train_x = train_df[fcolumns]

            logr = LogisticRegression(penalty="none", max_iter=2000, solver='liblinear') # Used to be 2000 for 9-6, often didn't converge.
            # Try adjusting logistic hyperparams: maybe add penalty, change solver from lbfgs...
            # Maybe not converging for logistic because of multicollinearity?
            logr.fit(train_x, train_y)

        
            # Loop through test eval for each subgroup
            for curr_subgroup in subgroups:
                # Get indices of rows that match curr_subgroup
                cs_ind = test_df.loc[test_df[curr_subgroup]==1].index
                # For subgroups, select only current 'sg' from test_df & test_y.
                sg_test_df = test_df[test_df[curr_subgroup] == 1]
                sg_test_y = test_y.iloc[cs_ind] # use column indices for test_y, bc no subgroup cols here
                
                # Get only desired feature cols
                test_x = sg_test_df[fcolumns]
                # get the test encounter id
                test_idx = sg_test_df["Encounter"]
  
                auc, aps, y_hat = evaluate_results(logr, test_x, sg_test_y)


                

                perf_res = {
                    "model": "logr",
                    "ts": datetime.now(),
                    "auc": auc,
                    "aps": aps,
                    "subgroup": curr_subgroup,
                    "test_samp_size": len(sg_test_y)
                }
                mcol.insert_one({**base_res, **perf_res})
                tmp = dict(zip(test_idx, y_hat))
                raw_res = {
                    "model": "logr",
                    "pred": json.dumps(tmp)
                }
                raw_mcol.insert_one({**base_res, **raw_res})
                # Save logistic coeffs for: black, white subgroups specifically.
                # Save these for EACH set of feats (track which 'feat' and 'subgroup')
                log_coeffs = {
                    "feat": fname,
                    "subgroup": curr_subgroup,
                    "model": "logr",
                    "logr_feat_names": fcolumns,
                    "logr_coeffs": logr.coef_.tolist(),
                    "logr_intercept": logr.intercept_.tolist()
                }
                # Save logr coefficients. For later comparison btw black, white, & other subgroups.
                logcoeffs_mcol.insert_one({**base_res, **log_coeffs})
                


            for mname, mk_dict in tqdm.tqdm(MODEL_PARAMS.items(),
                                            desc="models", leave=False):
                gs = skms.GridSearchCV(mk_dict["model"],
                                       mk_dict["params"],
                                       cv=5,
                                       n_jobs=4,
                                       scoring='roc_auc')
                gs.fit(train_x, train_y)  
                # Loop through test eval for each subgroup
                for curr_subgroup in subgroups:
                    # Get indices of rows that match curr_subgroup
                    cs_ind = test_df.loc[test_df[curr_subgroup]==1].index
                    # For subgroups, select only current 'sg' from test_df & test_y.
                    sg_test_df = test_df[test_df[curr_subgroup] == 1]
                    sg_test_y = test_y.iloc[cs_ind] # use column indices for test_y, bc no subgroup cols here
                    
                    # Get only desired feature cols
                    test_x = sg_test_df[fcolumns]
                    # get the test encounter id
                    test_idx = sg_test_df["Encounter"]
                    auc, aps, _ = evaluate_results(gs, test_x, sg_test_y)
                    perf_res = {
                        "model": mname,
                        "ts": datetime.now(),
                        "auc": auc,
                        "aps": aps,
                        "subgroup": curr_subgroup,
                        "test_samp_size": len(sg_test_y)
                    }
                    mcol.insert_one({**base_res, **perf_res})
                    
                    # Get SHAP for XGBoost
                    if mname == "xgboost":
                        model = gs.best_estimator_ # Best XGBoost model.
                        explainer = shap.Explainer(model)
                        shap_values = explainer(np.ascontiguousarray(test_x))
                        shap_importance = shap_values.abs.mean(0).values
                        sorted_idx = shap_importance.argsort()
                        ordered_shaps = shap_importance[sorted_idx]
                        names_ordered_shaps = np.array(fcolumns)[sorted_idx]
                        # Save Ordered shaps & names.
                        xg_shap_res = {
                            "model": mname,
                            "ts": datetime.now(),
                            "auc": auc,
                            "aps": aps,
                            "subgroup": curr_subgroup,
                            "test_samp_size": len(sg_test_y),
                            "shap_ordered_names": names_ordered_shaps.tolist(),
                            "shap_ordered_importance": ordered_shaps.tolist()
                        }
                        shap_mcol.insert_one({**base_res, **xg_shap_res})
                        

    mclient.close()


if __name__ == '__main__':
    main()

