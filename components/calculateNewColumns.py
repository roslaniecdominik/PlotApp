import numpy as np
import pandas as pd

def new_columns_solutions(data_list, solutions, data):
                solution_list = [solution.strip() for solution in solutions.split(",")]

                solution_ranges = {}
                for i, solution in enumerate(solution_list):
                    solution_ranges[solution] = range(i*50+1, i*50+50)

                if "PRN" in data_list:
                     for solution, num_range in solution_ranges.items():
                        for element in data_list:
                            data[f"{element}_{solution}"] = data[element].where(data["PRN"].isin(num_range))
                else:
                    for solution, num_range in solution_ranges.items():
                        for element in data_list:                     
                            data[f"{element} {solution}"] = data[element].where(data["PRN"].isin(num_range))
                return data

def calculate_new_columns(data, selected_datas, solutions, filepath):
    for selected_data in selected_datas:
        if selected_data == "Satellite Vehicle":
            data["nGNSS"] = data["nE"] + data["nG"] + data["nR"] + data["nC"] + data["nJ"] + data["nS"]
        
        elif selected_data == "REC dNEU":
            inf_filepath = list(filter(lambda x: "Inf" in x, filepath))
            if inf_filepath:
                inf_data = pd.read_csv(inf_filepath[0], sep=';', index_col=False, skipinitialspace=True)
                data["RecdN"] = data["RecN"] - inf_data["RefN"].mean()
                data["RecdE"] = data["RecE"] - inf_data["RefE"].mean()
                data["RecdU"] = data["RecU"] - inf_data["RefU"].mean()
                print(data["RecU"].mean())
                print(inf_data)
        
        elif selected_data == "REC dXYZ":
            data["RecdX"] = data["RecX"] - data["RecX"].mean()
            data["RecdY"] = data["RecY"] - data["RecY"].mean()
            data["RecdZ"] = data["RecZ"] - data["RecZ"].mean()
            
        elif selected_data == "Zenith Tropospheric Delay":
            data["mZTD+"] = data["ZTD"] + data["mZTD"]
            data["mZTD-"] = data["ZTD"] - data["mZTD"]
        elif selected_data == "PRN":
            data_list = ["PRN"]
            data = new_columns_solutions(data_list, solutions, data)
            data["Bad IFree"] = np.where(data["Typ"] == "BIF", data["PRN_sign"], np.nan)
            data["No Clock"] = np.where(data["Typ"] == "NCL", data["PRN_sign"], np.nan)
            data["No Orbit"] = np.where(data["Typ"] == "NOR", data["PRN_sign"], np.nan)
            data["Cycle Slips"] = np.where(data["Typ"] == "CSL", data["PRN_sign"], np.nan)
            data["Outliers"] = np.where(data["Typ"] == "OUT", data["PRN_sign"], np.nan)
            data["Eclipsing"] = np.where(data["Typ"] == "ECL", data["PRN_sign"], np.nan)
        
        elif selected_data == "Phase Ambiguity":
            data_list = ["N_IF", "N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8"]
            data = new_columns_solutions(data_list, solutions, data)

        elif selected_data == "m Phase Ambiguity":
            data_list = ["mN_L1", "mN_L2", "mN_L3", "mN_L4", "mN_L5", "mN_L6", "mN_L7", "mN_L8"]
            data = new_columns_solutions(data_list, solutions, data)
        
        elif selected_data == "Code Residuals":
            data_list = ["C_Res1", "C_Res2", "C_Res3", "C_Res4", "C_Res5", "C_Res6", "C_Res7", "C_Res8", "C_Res_IF"]

            data = new_columns_solutions(data_list, solutions, data)

        elif selected_data == "Phase Residuals":
            data_list = ["L_Res1", "L_Res2", "L_Res3", "L_Res4", "L_Res5", "L_Res6", "L_Res7", "L_Res8", "L_Res_IF"]

            data = new_columns_solutions(data_list, solutions, data)

    return data