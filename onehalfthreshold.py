import numpy as np

def get_optimal_fp_tp(loss_fn,loss_fp,pointwise_min_df,eq_fpr):
    pointwise_min_tpr = list(pointwise_min_df)

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

def get_optimal_fp_tp_hardtf(totals,fraction_positives, target_rate,pointwise_min_df,eq_fpr):
    pointwise_min_tpr = list(pointwise_min_df)

    min_loss = float('inf')
    min_loss_fpr = None
    min_loss_tpr = None

    for index in range(0, len(eq_fpr)):
        fpr = eq_fpr[index]
        tpr = pointwise_min_tpr[index]
        function_loss = calc_hardt_profit_function(totals, fraction_positives,target_rate,tpr,fpr)
        if (function_loss < min_loss):
            min_loss = function_loss
            min_loss_fpr = fpr
            min_loss_tpr = tpr
    return (min_loss,min_loss_fpr, min_loss_tpr)

def calc_hardt_profit_function(totals,fraction_positives,target_rate,tpr,fpr):
    loss_fp = (1 - fraction_positives)*fpr*target_rate
    fnr = 1 - tpr
    loss_fn = fraction_positives*(fnr)*(1-target_rate)
    loss_fp_fn = loss_fp + loss_fn
    loss = 0
    for k,v in totals.items():
        loss += loss_fp_fn[k]*v

    return loss

def get_indices_for_a_opt(find_slope,eq_fpr,tpr_a,start_index,end_index):
    if(start_index > end_index):
        return None

    mid = (start_index + end_index) // 2
    calc_slope_mid = tpr_a[mid]/eq_fpr[mid]
    calc_slope_0 = tpr_a[mid-1]/eq_fpr[mid-1]
    calc_slope_1 = None

    if (mid < len(eq_fpr) - 1):
        calc_slope_1 = tpr_a[mid+1]/eq_fpr[mid+1]

    if (calc_slope_mid == find_slope):
        return (mid, mid)

    elif mid > 0 and calc_slope_0 > find_slope > calc_slope_mid:
        return (mid - 1, mid)

    elif mid < (len(eq_fpr) - 1) and calc_slope_mid > find_slope > calc_slope_1:
        return (mid, mid + 1)

    elif (calc_slope_mid > find_slope):
        # if find_slope is smaller than the smallest slope in data then just return the smallest and this happens when:
        if (mid >= len(eq_fpr) - 1):
            return (mid, mid)
        return get_indices_for_a_opt(find_slope, eq_fpr, tpr_a,mid+1,end_index)

    elif (calc_slope_mid < find_slope):
        if (mid <= 0): # if find_slope is larger than the largest slope in data then just return the largest and this happens when:
             return (mid, mid)
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

def equalized_odds_classifer(score,attr,ta_dict,pa_dict):
    t_a = ta_dict[attr]
    p_a = pa_dict[attr]

    s = np.random.binomial(1,p_a) #n=1

    if(s == 0): #w 1-pa
        return 0
    elif(score >= t_a): #w p_a s = 1
        return 1
    else: #w p_a
        return 0

