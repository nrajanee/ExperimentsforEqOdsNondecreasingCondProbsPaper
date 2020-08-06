import pandas as pd
import matplotlib.pylab as plt
import numpy as np

def get_recid_compas_df():
    entire_df = pd.read_csv("compas-scores-two-years.csv")
    recid_df = entire_df[['id','race','decile_score','score_text','is_recid']]
    recid_df_w_b = recid_df[(recid_df['race'] == 'African-American') | (recid_df['race'] == 'Caucasian')]

    return recid_df_w_b

def get_compas_fpr_tpr(recid_df_w_b):
    decile_thres_range = list(np.arange(1,10.1,0.1))

    fpr_df = pd.DataFrame(columns = ['Black','White'],index = decile_thres_range)
    tpr_df = pd.DataFrame(columns = ['Black','White'],index = decile_thres_range)

    for decile_score in decile_thres_range:
        true_pos_c_b = 0
        false_pos_c_b = 0
        true_pos_c_w = 0
        false_pos_c_w = 0
        total_b_pos = 0
        total_b_neg = 0
        total_w_pos = 0
        total_w_neg = 0
        for index,df_row in recid_df_w_b.iterrows():
            predic_val = df_row['decile_score'] >= decile_score
            if df_row['is_recid'] == 1:
                if df_row['race'] == 'African-American':
                    total_b_pos = total_b_pos + 1
                else:
                    total_w_pos = total_w_pos + 1
                if predic_val == 1:
                    if df_row['race'] == 'African-American':
                        true_pos_c_b = true_pos_c_b + 1
                    else:
                        true_pos_c_w = true_pos_c_w + 1
            else:
                if df_row['race'] == 'African-American':
                    total_b_neg = total_b_neg + 1
                else:
                    total_w_neg = total_w_neg + 1
                if predic_val == 1:
                    if df_row['race'] == 'African-American':
                        false_pos_c_b = false_pos_c_b + 1
                    else:
                        false_pos_c_w = false_pos_c_w + 1

        true_pos_b = true_pos_c_b/(total_b_pos)
        false_pos_b = false_pos_c_b/(total_b_neg)
        true_pos_w = true_pos_c_w/(total_w_pos)
        false_pos_w =  false_pos_c_w/(total_w_neg)
        row_fpr = []
        row_fpr.append(false_pos_b)
        row_fpr.append(false_pos_w)
        row_tpr = []
        row_tpr.append(true_pos_b)
        row_tpr.append(true_pos_w)
        fpr_df.loc[decile_score,:]= row_fpr
        tpr_df.loc[decile_score,:] = row_tpr

    return fpr_df,tpr_df


