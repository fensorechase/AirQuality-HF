import json
import sklearn.metrics as skm


def read_json(infile):
    """
    Load a json file
    """
    with open(infile, 'r') as ifile:
        return json.load(ifile)


def evaluate_results(model, test_x, test_y):
    # evaluate on test
    y_hat = model.predict_proba(test_x)[:, 1]
    auc = skm.roc_auc_score(test_y, y_hat)
    aps = skm.average_precision_score(test_y, y_hat)
    return auc, aps, y_hat


def get_train_test(df, i, label="readmit30bin"):
    test_mask = df[label+"_folds"] == i
    train_df = df[~test_mask]
    test_df = df[test_mask]
    # setup y
    train_y = train_df[label]
    test_y = test_df[label]
    return train_df, test_df, train_y, test_y
