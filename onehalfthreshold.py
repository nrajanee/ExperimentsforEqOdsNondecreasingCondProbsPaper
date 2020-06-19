from pointwise_min import construct_df_for_eq_div_fpr
from pointwise_min import get_fpr_eq_div

def get_optimal_fp_tp():
    eq_fpr_df = construct_df_for_eq_div_fpr()
    drop_thresholds_df = eq_fpr_df.drop(
        columns=['Asian_threshold', 'Black_threshold', 'Hispanic_threshold', 'White_threshold'])
    pointwise_min_df = drop_thresholds_df.min(axis=1)
    eq_fpr = list(get_fpr_eq_div())
    pointwise_min_tpr = list(pointwise_min_df)
    loss_fn = 0.3 #cost of a non-defaulter not getting a loan
    loss_fp = 0.2 #cost of a defaulter getting a loan

    min_loss = float('inf')
    min_loss_fpr = None
    min_loss_tpr = None

    for index in range(0,len(eq_fpr)):
        fpr = eq_fpr[index]
        tpr = pointwise_min_tpr[index]
        obj_fn_loss = fpr*loss_fp + (1-tpr)*loss_fn
        if(obj_fn_loss <= min_loss):
            min_loss = obj_fn_loss
            min_loss_fpr = fpr
            min_loss_tpr = tpr

    return (min_loss_fpr,min_loss_tpr)





