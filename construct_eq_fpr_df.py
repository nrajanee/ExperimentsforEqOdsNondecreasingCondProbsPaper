import pandas as pd
import numpy as np

def get_fpr_eq_div(division=0.01):
    return np.arange(0.0,1.0,division) #ended before you hit 1 because at threshold 0 it's almost 1 (0.99994) so you won't find exactly 1

def get_data_fpr_list(sens_attr,fpr_df):
    data_fpr = []
    for index,row in fpr_df.iterrows():
        data_fpr.append(row[sens_attr])
    return data_fpr


def get_data_tpr_list(sens_attr,tpr_df):
    data_tpr = []
    for index,row in tpr_df.iterrows():
        data_tpr.append(row[sens_attr])
    return data_tpr


def get_data_threshold_list(fpr_df):
    threshold = []
    for index,row in fpr_df.iterrows():
        threshold.append(index)

    return threshold

def get_indices_for_fpr(fpr_list,start_fpr_index,end_fpr_index,find_fpr):
    #NOTE: fpr_list is in descending order!!!

    if(start_fpr_index > end_fpr_index):
        print('couldn\'t find find_fpr')
        return None

    mid = (start_fpr_index + end_fpr_index) // 2
    if(fpr_list[mid] == find_fpr):
        return(mid,mid)
    elif mid > 0 and fpr_list[mid - 1] > find_fpr > fpr_list[mid]:
        return(mid-1, mid)

    elif mid < (len(fpr_list) - 1) and fpr_list[mid] > find_fpr > fpr_list[mid+1]:
        return(mid,mid+1)

    elif(fpr_list[mid] > find_fpr):
        return get_indices_for_fpr(fpr_list,mid+1,end_fpr_index,find_fpr)

    elif(fpr_list[mid] < find_fpr):
        return get_indices_for_fpr(fpr_list,start_fpr_index,mid-1,find_fpr)

    else:
        print('Didnt go through any of the above')

def in_between_tpr(fpr_1,fpr_2,find_fpr,tpr_1,tpr_2):
    if(fpr_1 == fpr_2):
        return tpr_1
    m = (tpr_1 - tpr_2)/(fpr_1-fpr_2)
    in_bw_tpr = tpr_1 - m * (fpr_1 - find_fpr)

    return in_bw_tpr

def in_between_threshold(fpr_1,fpr_2,find_fpr,threshold_1,threshold_2):
    if(fpr_1 == fpr_2): #this happens when get_indicies_for_fpr returns mid, mid
        return threshold_1
    m = (threshold_1 - threshold_2)/(fpr_1-fpr_2)
    in_bw_threshold = threshold_1 - m * (fpr_1 - find_fpr)

    return in_bw_threshold

def construct_df_for_eq_div_fpr(fpr_df,tpr_df,division=0.01):
    threshold_list = get_data_threshold_list(fpr_df)
    eq_div_fpr = list(get_fpr_eq_div(division))
    columns = []
    atrr_fpr_tpr_lists = {}
    list_sens_attr = fpr_df.columns
    print(list_sens_attr)
    for sens_attr in list_sens_attr:
        columns.append(sens_attr+'_tpr')
        columns.append(sens_attr+'_threshold')
        fpr_list_attr = get_data_fpr_list(sens_attr,fpr_df)
        tpr_list_attr = get_data_tpr_list(sens_attr,tpr_df)
        atrr_fpr_tpr_lists[sens_attr] = (fpr_list_attr,tpr_list_attr)

    df_eq_div_fpr = pd.DataFrame(columns=columns,index=eq_div_fpr)

    for find_fpr in eq_div_fpr:
        find_fpr_row = []
        for sens_attr in list_sens_attr:
            fpr_list = atrr_fpr_tpr_lists[sens_attr][0]
            tpr_list = atrr_fpr_tpr_lists[sens_attr][1]
            found_index_1, found_index_2 = get_indices_for_fpr(fpr_list, 0, len(fpr_list) - 1, find_fpr)

            #remember descending, so fpr_1 > fpr_2 likewise for tpr

            fpr_1 = fpr_list[found_index_1]
            fpr_2 = fpr_list[found_index_2]

            threshold_1 = threshold_list[found_index_1]
            threshold_2 = threshold_list[found_index_2]

            tpr_1 = tpr_list[found_index_1]
            tpr_2 = tpr_list[found_index_2]

            #TODO: figure out the equation ot find the right threshold and tpr for find_fpr

            in_bw_tpr = in_between_tpr(fpr_1,fpr_2,find_fpr,tpr_1,tpr_2)
            in_bw_threshold = in_between_threshold(fpr_1,fpr_2,find_fpr,threshold_1,threshold_2)
            find_fpr_row.append(in_bw_tpr)
            find_fpr_row.append(in_bw_threshold)

        df_eq_div_fpr.loc[find_fpr,:] = find_fpr_row

    return df_eq_div_fpr