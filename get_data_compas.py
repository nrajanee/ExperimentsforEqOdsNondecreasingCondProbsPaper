import pandas as pd
import matplotlib.pylab as plt

def get_recid_compas_df():
    entire_df = pd.read_csv("compas-scores-two-years.csv")
    recid_df = entire_df[['id','race','decile_score','score_text','is_recid']]
    recid_df_w_b = recid_df[(recid_df['race'] == 'African-American') | (recid_df['race'] == 'Caucasian')]

    return recid_df_w_b

def get_fpr_tpr(recid_df_w_b):

    thres_fpr_tpr = pd.DataFrame(columns = ['threshold','fpr_Black','tpr_Black','fpr_White','tpr_White'])

    for decile_score in range(1,11):
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
        thres_fpr_tpr = thres_fpr_tpr.append({'threshold': decile_score,'fpr_Black':false_pos_b,'tpr_Black':true_pos_b,'fpr_White':false_pos_w,'tpr_White': true_pos_w},ignore_index=True)
    print(thres_fpr_tpr)
    return thres_fpr_tpr


