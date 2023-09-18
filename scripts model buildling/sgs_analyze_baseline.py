import argparse
import datetime
import pandas as pd
from pymongo import MongoClient
import urllib.parse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-output", help="output file",
                        default="__INPUT FEATS CSV__") 
    # subgroups: results_clean_tract_ahrq_AQIimp1_baseline_SGs_2.csv
    # Sep subgroups: results_clean_tract_ahrq_AQIimp1_baseline_sep_SGs.csv
    username = urllib.parse.quote_plus('__MONGO UN__')
    password = urllib.parse.quote_plus('__MONGO PW__')
    parser.add_argument("-mongo_url", default = '__MONGO LOCAL URL__')
    parser.add_argument("-mongo_db",
                        default="__MONGO DB NAME__")
    parser.add_argument("-mongo_col",
                        default="__MONGO COLLECTION NAME__",
                        help="collection_type") # For subgroup results, set default="subgroups_baseline", for entire dataset, default="baseline"
    args = parser.parse_args()

    # setup the mongo stuff
    mclient = MongoClient(args.mongo_url)
    mdb = mclient[args.mongo_db]
    mcol = mdb[args.mongo_col]

    pipe_list = [{
    "$group":
            {
                "_id":
                {
                    "feat": "$feat",
                    "model": "$model",
                    "file": "$file",
                    "endpoint": "$endpoint",
                    "subgroup": "$subgroup"
                },
                "auc":
                {
                    "$avg": "$auc"
                },
                "auc_sd":
                {
                    "$stdDevSamp": "$auc"
                },
                "auprc":
                {
                    "$avg": "$aps"
                },
                "auprc_sd":
                {
                    "$stdDevSamp": "$aps"
                },
                "n_runs": 
                {
                    "$sum": 1
                },
                "test_samp_size": 
                {
                    "$avg": "$test_samp_size"
                }
            }
    },
    {"$project":
            {
                "model": "$_id.model",
                "feat": "$_id.feat",
                "file": "$_id.file",
                "endpoint": "$_id.endpoint",
                "auc": "$auc",
                "auc_sd": "$auc_sd",
                "auprc": "$auprc",
                "auprc_sd": "$auprc_sd",
                "n_runs": "$n_runs",
                "_id": 0,
                "subgroup": "$_id.subgroup",
                "test_samp_size": "$test_samp_size"
            }
            }
    ]


    tmp = list(mcol.aggregate(pipe_list))
    tmp_df = pd.DataFrame.from_records(tmp)
    #print(tmp_df)
    mclient.close()

    tmp_df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()

