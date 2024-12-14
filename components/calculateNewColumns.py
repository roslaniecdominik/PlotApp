import numpy as np
def calculate_new_columns(data, selected_datas):
    for selected_data in selected_datas:
        if selected_data == "Satellite Vehicle":
            data["nGNSS"] = data["nE"] + data["nG"] + data["nR"] + data["nC"] + data["nJ"] + data["nS"]
        elif selected_data == "REC dNEU":
            data["RecdN"] = data["RecN"] - data["RecN"].mean()
            data["RecdE"] = data["RecE"] - data["RecE"].mean()
            data["RecdU"] = data["RecU"] - data["RecU"].mean()
        elif selected_data == "Zenith Tropospheric Delay":
            data["mZTD+"] = data["ZTD"] + data["mZTD"]
            data["mZTD-"] = data["ZTD"] - data["mZTD"]
        elif selected_data == "PRN":
            data["PRN_GPS"] = data["PRN"].apply(lambda x: x if x < 40 else np.nan)
            data["PRN_Galileo"] = data["PRN"].apply(lambda x: x if x > 40 else np.nan)
            data["Bad IFree"] = np.where(data["Typ"] == "BIF", data["PRN_sign"], np.nan)
            data["No Clock"] = np.where(data["Typ"] == "NCL", data["PRN_sign"], np.nan)
            data["No Orbit"] = np.where(data["Typ"] == "NOR", data["PRN_sign"], np.nan)
            data["Cycle Slips"] = np.where(data["Typ"] == "CSL", data["PRN_sign"], np.nan)
            data["Outliers"] = np.where(data["Typ"] == "OUT", data["PRN_sign"], np.nan)
            data["Eclipsing"] = np.where(data["Typ"] == "ECL", data["PRN_sign"], np.nan)
        elif selected_data == "Phase Ambiguity":
            list_GPS = ["N_IF GPS", "N_L1 GPS", "N_L2 GPS", "N_L3 GPS", "N_L4 GPS", "N_L5 GPS", "N_L6 GPS", "N_L7 GPS", "N_L8 GPS"]
            list_Galileo = ["N_IF Galileo", "N_L1 Galileo", "N_L2 Galileo", "N_L3 Galileo", "N_L4 Galileo", "N_L5 Galileo", "N_L6 Galileo", "N_L7 Galileo", "N_L8 Galileo"]
            for element in list_GPS:
                data[element] = np.where(data["PRN"] < 40, data[element.split()[0]], np.nan)
            for element in list_Galileo:
                data[element] = np.where(data["PRN"] > 40, data[element.split()[0]], np.nan)
        elif selected_data == "m Phase Ambiguity":
            list_GPS = ["mN_L1 GPS", "mN_L2 GPS", "mN_L3 GPS", "mN_L4 GPS", "mN_L5 GPS", "mN_L6 GPS", "mN_L7 GPS", "mN_L8 GPS"]
            list_Galileo = ["mN_L1 Galileo", "mN_L2 Galileo", "mN_L3 Galileo", "mN_L4 Galileo", "mN_L5 Galileo", "mN_L6 Galileo", "mN_L7 Galileo", "mN_L8 Galileo"]
            for element in list_GPS:
                data[element] = np.where(data["PRN"] < 40, data[element.split()[0]], np.nan)
            for element in list_Galileo:
                data[element] = np.where(data["PRN"] > 40, data[element.split()[0]], np.nan)
        elif selected_data == "Code Residuals":
            list_GPS = ["C_Res1 GPS", "C_Res2 GPS", "C_Res3 GPS", "C_Res4 GPS", "C_Res5 GPS", "C_Res6 GPS", "C_Res7 GPS", "C_Res8 GPS", "C_Res_IF GPS"]
            list_Galileo = ["C_Res1 Galileo", "C_Res2 Galileo", "C_Res3 Galileo", "C_Res4 Galileo", "C_Res5 Galileo", "C_Res6 Galileo", "C_Res7 Galileo", "C_Res8 Galileo", "C_Res_IF Galileo"]
            for element in list_GPS:
                data[element] = np.where(data["PRN"] < 40, data[element.split()[0]], np.nan)
            for element in list_Galileo:
                data[element] = np.where(data["PRN"] > 40, data[element.split()[0]], np.nan)
        elif selected_data == "Phase Residuals":
            list_GPS = ["L_Res1 GPS", "L_Res2 GPS", "L_Res3 GPS", "L_Res4 GPS", "L_Res5 GPS", "L_Res6 GPS", "L_Res7 GPS", "L_Res8 GPS", "L_Res_IF GPS"]
            list_Galileo = ["L_Res1 Galileo", "L_Res2 Galileo", "L_Res3 Galileo", "L_Res4 Galileo", "L_Res5 Galileo", "L_Res6 Galileo", "L_Res7 Galileo", "L_Res8 Galileo", "L_Res_IF Galileo"]
            for element in list_GPS:
                data[element] = np.where(data["PRN"] < 40, data[element.split()[0]], np.nan)
            for element in list_Galileo:
                data[element] = np.where(data["PRN"] > 40, data[element.split()[0]], np.nan)
    return data