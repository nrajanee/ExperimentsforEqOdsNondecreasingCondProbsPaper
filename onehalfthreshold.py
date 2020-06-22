from pointwise_min import construct_df_for_eq_div_fpr
from pointwise_min import get_fpr_eq_div


#make loss function as parameters to function
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

def get_indices_for_a_opt(find_slope,eq_fpr,tpr_a,start_index,end_index):
    if(start_index >= end_index):
        return None

    mid = (start_index + end_index) // 2

    calc_slope_mid = tpr_a[mid]/eq_fpr[mid]
    calc_slope_0 = tpr_a[mid-1]/eq_fpr[mid-1]
    calc_slope_1 = tpr_a[mid+1]/eq_fpr[mid+1]

    if (calc_slope_mid == find_slope):
        return (mid, mid)

    elif mid != 0 and calc_slope_0 > find_slope >= calc_slope_mid:
        return (mid - 1, mid)

    elif mid != len(eq_fpr) and calc_slope_mid > find_slope > calc_slope_1:
        return (mid, mid + 1)

    elif (calc_slope_mid > find_slope):
        return get_indices_for_a_opt(find_slope, eq_fpr, tpr_a,mid+1,end_index)

    elif (calc_slope_mid < find_slope):
        return get_indices_for_a_opt(find_slope, eq_fpr, tpr_a,start_index,mid-1)

    else:
        print('Didnt go through any of the above')

def get_fpa_opt_tpa_opt_thres_a_opt(fp_1,fp_2,tp_1,tp_2,threshold_1, threshold_2,opt_slope):
    if (fp_1 == fp_2):
        return (fp_1,tp_1,threshold_1)

    slope_curve = (tp_2-tp_1)/(fp_2-fp_1) #eq_fpr and tpr_a are ascending

    fpa_opt = (tp_2 - slope_curve*fp_2)/(opt_slope-slope_curve)
    tpa_opt = fpa_opt*opt_slope

    thresh_fp_ratio = (threshold_2-threshold_1)/(fp_2-fp_1)

    threshold_a_opt = threshold_2 - thresh_fp_ratio*(fp_2-fpa_opt)

    return(fpa_opt,tpa_opt,threshold_a_opt)

