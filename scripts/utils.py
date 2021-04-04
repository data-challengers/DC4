import numpy as np
import pandas as pd
def discretize_scale(color_arr):
    new_scale = []
    n = len(color_arr)
    h = 1.0/(n)
    c_order = h * np.arange(n+1)
    for i in range(n):
        new_scale.append([c_order[i], color_arr[i][1]])
        # To have clear boundaries between colors in the colorbar
        if i < (n):
            new_scale.append([c_order[i+1], color_arr[i][1]])

    return new_scale

def classify_ip(ip):
    ip = ip.split(".")
    c = str(None)
    if len(ip) == 4:
        ip = [int(ip[i]) for i in range(len(ip))]
        if ip[0] == 172:
            if ip[2] == 0:
                if (ip[1] == 23 or ip[1] == 25) and ip[3] == 1:
                    c = "Firewall"
                elif (ip[1] == 23 and ip[3] == 2):
                    c = "Log Server"
                elif (ip[1] == 23 and ip[3] == 10):
                    c = "Domain controller/DNS"
                elif ip[1] == 23:
                    c = "Workstation"
            elif ip[1] == 23:
                if (214 <= ip[2] <= 229):
                    c = "BoM Financial Server"
                else:
                    c = "Workstation"                
        elif ip[0] == 10:
            if ip[1] == 32:
                if ip[2] == 0 and (ip[3] == 1 or ip[3] == 100):
                    c = "Firewall"
                elif (ip[2] == 0 and (201 <= ip[3] <= 210)):
                    c = "Website"
                elif (ip[2] == 1 and (ip[3] == 100 or (201 <= ip[3] <= 206))):
                    c = "Website"
                elif (ip[2] == 5 and (1 <= ip[3] <= 254)):
                    c = "Website"
            elif (ip[1] == 99 and ip[2] == 99 and ip[3] == 1):
                c = "Snort Detection"
    return c

def fill_df_nas(df, time_col, group_col, group_arr):
    """
    Expands dataframe to include all x-axis values for every group, and
    fills dataframes with NAs when there are no observations for the specified group.
    Useful for Plotly graphs in mode='lines+markers'
    :param: df: dataframe of interest
    :param: time_col: string name of column that contains time variable (or generally, the x variable)
    :param: group_col: string name of column that contains the groups to plot over different traces
    :param: group_arr: list or numpy array of all unique observations in df['group_col']
    :return: new dataframe
    """
    df = df.sort_values(by=[time_col])
    min_time = df[time_col].min()
    max_time = df[time_col].max()
    time_range = pd.date_range(min_time, max_time, freq='H')
    df_series = pd.Series(np.tile(group_arr, len(time_range)))
    df_idx_series = time_range \
        .repeat(len(group_arr))
    new_df = pd.DataFrame({time_col: df_idx_series,
                          group_col: df_series})
    df_with_nas = pd.merge(new_df, df, on=[time_col, group_col], how='left')
    return df_with_nas