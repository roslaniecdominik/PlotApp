import numpy as np
import pandas as pd

def len_availablePRNs_calculation(df):
    result = (
        df.dropna(subset=['AvailablePRNs'])
        .groupby('datetime')['AvailablePRNs']
        .first()
        .reset_index()
    )

    available_prn = result['AvailablePRNs'].apply(lambda x: len(x.split())).sum()
    return available_prn

def calc_statistics(data, selected_datas, filepath):
    if len(filepath) > 0:
        dict = {
            "Crode Residuals": ["C_Res1", "C_Res2", "C_Res3", "C_Res4", "C_Res5", "C_Res6", "C_Res7", "C_Res8", "C_Res_IF"],
            "Pfhase Residuals": ["L_Res1", "L_Res2", "L_Res3", "L_Res4", "L_Res5", "L_Res6", "L_Res7", "L_Res8", "L_Res_IF"],
            "Satellite Vehicle": ["nG", "nE", "nR", "nC", "nJ", "nGNSS"],
            "DOP factors": ["PDop", "TDop", "HDop", "VDop", "GDop"],
            "Receiver Clock Estimation": ["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"],
            "REC dNEU": ["RecN", "RecE", "RecU"],
            "REC mNEU": ["RecmN", "RecmE", "RecmU"],
            "REC mXYZ": ["RecmX", "RecmY", "RecmZ"],
            "Zenith Tropospheric Delay" : ["ZTD"],
            "REC XYZ": ["RecX", "RecY", "RecZ"],
            "REC NEU": ["RecN", "RecE", "RecU"],
            "PRN": ["Outliers"]
        }
        stat_list = []
        for selected_data in selected_datas:


            try:
                data_listnames = [col for col in dict[selected_data] if col in data.columns] #check if they are in data
                data_listnames = [col for col in data_listnames if not (data[col].isna().all() or (data[col].fillna(0) == 0).all())] #removes if 0/NaN in all

                if selected_data == "Satellite Vehicle" or selected_data == "DOP factors":

                    mean_values = [data[data_listname].mean() for data_listname in data_listnames]
                    min_values = [data[data_listname].min() for data_listname in data_listnames]
                    max_values = [data[data_listname].max() for data_listname in data_listnames]
                    stat_text_list = []
                    stat_text_list.append(f"mean: {' '.join([f'{col}:{mean_values[i]:.2f}' for i, col in enumerate(data_listnames)])}")
                    stat_text_list.append(f"min: {' '.join([f"{col}:{min_values[i]:.2f}" for i, col in enumerate(data_listnames)])}")
                    stat_text_list.append(f"max: {' '.join([f"{col}:{max_values[i]:.2f}" for i, col in enumerate(data_listnames)])}")
                    
                    stat_text = ";  ".join(stat_text_list)
                    stat_list.append(stat_text)
                
                if selected_data in ["Receiver Clock Estimation", "REC mNEU", "Zenith Tropospheric Delay", "REC mXYZ"]:
                    data_listnames = [col for col in data_listnames if not (data[col].isna().all() or (data[col].fillna(0) == 0).all())] #removes if 0/NaN in all
                    stat_text_list = []

                    for element in data_listnames:
                        without_nan = data[element].dropna().tolist()
                        stat_text_list.append(f"{element}: \u03BC = {np.mean(without_nan):.3f}   \u03C3 = {np.std(without_nan):.3f}   \u003C{data[element].min():.3f}; {data[element].max():.3f}\u003E")
                    stat_text = ";  ".join(stat_text_list)
                    stat_list.append(stat_text)
                    
                if selected_data == "REC dNEU" or selected_data == "REC NEU" or selected_data == "REC XYZ":
                    inf_filepath = list(filter(lambda x: "Inf" in x, filepath))
                    
                    if selected_data == "REC XYZ":
                        ref_list = ["RefX", "RefY", "RefZ"]
                        d_list = ["RecdX", "RecdY", "RecdZ"]
                    else:
                        ref_list = ["RefN", "RefE", "RefU"]
                        d_list = ["RecdN", "RecdE", "RecdU"]
                    stat_text_list = []

                    if inf_filepath:
                        inf_data = pd.read_csv(inf_filepath[0], sep=';', index_col=False, skipinitialspace=True)
                        for element, ref, d_ in zip(data_listnames, ref_list, d_list):
                            if selected_data == "REC dNEU":
                                stat_text_list.append(f"{element}: \u03BC = {(data[element].mean() - inf_data[ref].mean()):.3f}   \u03C3 = {np.std(data[element]):.3f}   \u003C{data[d_].min():.3f}; {data[d_].max():.3f}\u003E")
                            else:
                                stat_text_list.append(f"{element}: \u03BC = {(data[element].mean() - inf_data[ref].mean()):.3f}   \u03C3 = {np.std(data[element]):.3f}   \u003C{data[element].min():.3f}; {data[element].max():.3f}\u003E")
                    else:
                        for element, ref, d_ in zip(data_listnames, ref_list, d_list):
                            stat_text_list.append(f"{element}: \u03BC = {data[element].mean():.3f}   \u03C3 = {np.std(data[element]):.3f}   \u003C{data[d_].min():.3f}; {data[d_].max():.3f}\u003E")
                        
                    if selected_data == "REC XYZ" or selected_data == "REC NEU":
                        stat_list.extend([i for i in stat_text_list])
                    else:  
                        stat_text = ";  ".join(stat_text_list)
                        stat_list.append(stat_text)
                
                if selected_data == "PRN":
                    length_used = data['PRN'][~data['PRN'].isna() & ~data['PRN'].isin([np.inf, -np.inf])].shape[0]
                    length_available = len_availablePRNs_calculation(data)


                    stat_list.append(f"Used: {length_used};  Available: {length_available}")
                    pd.set_option('display.max_columns', None)
                        
            except:
                stat_list.append("")

    return stat_list