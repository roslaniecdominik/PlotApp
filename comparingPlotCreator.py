import matplotlib.pyplot as plt
import customtkinter as ctk
import numpy as np
import pandas as pd

from matplotlib.ticker import ScalarFormatter
from datetime import datetime

from components.dataConfiguration import merge_data, time_column
from components.dataConfiguration import defining_data, match_data
from components.centerWindow import center_window
from components.solutionGenerator import solution_generator
from components.frames import plot_frames
from components.layerButtons import layer_buttons

data_dict, single_scatter, single_plot, triple_plot = defining_data()


def comparing_window(secondStation_menu_fullVar, filepaths, selected_data, cut_data, cut_column, selected_station_solution, error_label, 
                     start_time, end_time, station_list, xaxis_set, xaxis_label, app):
        
            data_listname, data_colors = match_data(selected_data)

            selected_secondStation_solution = secondStation_menu_fullVar.get()

            def error_message(text):
                error_label.configure(state="normal")
                
                if (len(error_label.get("1.0", "end"))) == 1:
                    error_label.insert("end", text)
                
                error_label.configure(state="disabled")
                

            if len(selected_secondStation_solution) == 0:
                error_message("Select second solution")
                has_common_times = False
            
            else:
                error_label.configure(state="normal")
                error_label.delete("0.0", "end")
                error_label.configure(state="disabled")
                
                selected_solution_encoded = solution_generator(selected_station_solution.split("(")[1].split(")")[0])
                selected_solution = solution_generator(selected_solution_encoded)

                selected_secondStation = selected_secondStation_solution.split(" ")[0]
                selected_secondSolution_encoded = solution_generator(selected_secondStation_solution.split("(")[1].split(")")[0])
                selected_secondSolution = solution_generator(selected_secondSolution_encoded)

                solutions = [selected_solution_encoded, selected_secondSolution_encoded]

                filepaths_cut = [filepath for filepath in filepaths if selected_secondStation in filepath and selected_secondSolution_encoded in filepath]
                
                filepath = []
                for key, value in data_dict.items():
                    if value == selected_data:
                        for i in filepaths_cut:
                            with open(i, "r") as file:
                                first_row = file.readline()
                                if key in first_row:
                                    filepath.append(i)


                if len(filepath) == 0:
                    error_message("The second station doesn't have same data")
                    has_common_times = False
                    
                else:
                    error_label.configure(state="normal")
                    error_label.delete("0.0", "end")
                    error_label.configure(state="disabled")
                
                    
                    secondData = pd.read_csv(filepath[0], sep=';', index_col=False, skipinitialspace=True)
                    secondData = time_column(secondData)
                    secondData = merge_data(secondData, selected_data, filepath)
                    cut_secondData = secondData[cut_column]
                    cut_secondData = cut_secondData.copy()
                    cut_secondData.loc[:, "Sol"] = selected_secondSolution_encoded
                    has_common_times = not set(cut_data['datetime']).isdisjoint(cut_secondData['datetime'])
            
            if not has_common_times:
                error_message("The second station doesn't have common time")
                
            else:
                error_label.configure(state="normal")
                error_label.delete("0.0", "end")
                error_label.configure(state="disabled")
                
                
                #Empty cell
                all_times = pd.DataFrame({'datetime': pd.concat([cut_data['datetime'], cut_secondData['datetime']]).unique()})

                if cut_data["Sol"].iloc[0] == cut_secondData["Sol"].iloc[0]:
                    cut_data1_full = pd.merge(all_times, cut_data, on='datetime', how='left').assign(Stat=selected_station_solution)
                    cut_secondData_full = pd.merge(all_times, cut_secondData, on='datetime', how='left').assign(Stat=selected_secondStation_solution)
                else:
                    cut_data1_full = pd.merge(all_times, cut_data, on='datetime', how='left').assign(Sol=solutions[0])
                    cut_secondData_full = pd.merge(all_times, cut_secondData, on='datetime', how='left').assign(Sol=solutions[1])

                cut_data_merged = pd.concat([cut_data1_full, cut_secondData_full], ignore_index=True).sort_values(by='datetime').reset_index(drop=True)
                time_data = cut_data_merged.loc[(cut_data_merged['datetime'] >= start_time) & (cut_data_merged['datetime'] <= end_time)]
                time_data = time_data.copy()
                # colors2 = ["dodgerblue", "pink", "orange"]

                def solution_dataframe(time_data, data_listname, solutions):
                    sol_df = time_data[time_data["Sol"] == solutions[0]].reset_index(drop=True)

                    if cut_data["Sol"].iloc[0] == cut_secondData["Sol"].iloc[0]:
                        
                        for layer_name in data_listname:
                            cords1 = time_data.loc[time_data["Stat"] == selected_station_solution, layer_name].reset_index(drop=True)
                            cords2 = time_data.loc[time_data["Stat"] == selected_secondStation_solution, layer_name].reset_index(drop=True)
                            sol_df[layer_name] = cords1 - cords2
                            
                    else:
                        for layer_name in data_listname:
                            cords1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name].reset_index(drop=True)
                            cords2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name].reset_index(drop=True)
                            sol_df[layer_name] = cords1 - cords2
                        
                    return sol_df
                
                global canvas_widget, toolbar_widget, layers_widget#, start_index
                canvas_widget = None
                toolbar_widget = None
                layers_widget = None

                def plot_position(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget
                    start_index = 0
                    def layer_buttons_comp(ax, layers_frame_on):
                        def toggle_visibility(name):
                            name.set_visible(not name.get_visible())
                            plt.draw()

                        layer_list = [selected_solution, selected_secondSolution, "Difference"]

                        layer_dict = {
                            selected_solution: 0,
                            selected_secondSolution: 0,
                            "Difference": 1
                        }
                        
                        i = -1
                        for key in layer_dict:
                            
                            i += 1
                            if i == len(layer_dict)-1:
                                i = 0
                                
                            layer_label = ctk.CTkLabel(layers_frame_on, text=key)
                            layer_label.pack(padx=10, pady=(10,5))
                        
                            for j, layer_name in enumerate(ax):

                                layer_frame = ctk.CTkFrame(layers_frame_on)
                                layer_frame.pack(side=ctk.TOP, padx=10, pady=5)

                                toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[j], command=lambda line=ax[j, layer_dict[key]].get_lines()[i]: toggle_visibility(line))
                                toggle_button.grid(row=0, column=0, padx=2, pady=2)
                                toggle_button.select()
                                
                                if key == layer_list[0]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color="purple")
                                elif key == layer_list[1]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color="orange")
                                elif key == layer_list[2]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[j])
                                
                                
                                buttons_line.grid(row=0, column=2, padx=(0, 5))


                    clear_plot()

                    fig, axs = plt.subplots(3, 2, figsize=(13,5))
                    lines = []
                    for i, layer_name in enumerate(data_listname):
                        if cut_data["Sol"].iloc[0] == cut_secondData["Sol"].iloc[0]:
                            sol_df = solution_dataframe(time_data, data_listname, station_list).reset_index(drop=True)
                            cord_time = time_data.loc[time_data["Stat"][start_index:] == selected_station_solution, "datetime"].reset_index(drop=True)
                            cord1 = time_data.loc[time_data["Stat"][start_index:] == selected_station_solution, layer_name].reset_index(drop=True)
                            cord2 = time_data.loc[time_data["Stat"][start_index:] == selected_secondStation_solution, layer_name].reset_index(drop=True)

                        else:
                            sol_df = solution_dataframe(time_data, data_listname, solutions).reset_index(drop=True)
                            cord_time = time_data.loc[time_data["Sol"] == solutions[0], "datetime"].reset_index(drop=True)
                            cord1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name].reset_index(drop=True)
                            cord2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name].reset_index(drop=True)
                        
                        line1 = axs[i, 0].plot(cord_time, cord1, color="purple")
                        
                        line2 = axs[i, 0].plot(cord_time, cord2, color="orange")
                        lines.append((line1, line2))
                        line, = axs[i, 1].plot(cord_time, sol_df[layer_name], color=data_colors[i])
                        lines.append(line)
                        
                        axs[i, 0].set_title(layer_name)
                        axs[i, 0].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                        axs[i, 0].grid(True)

                        axs[i, 0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                        axs[i, 0].ticklabel_format(useOffset=False, axis='y', style='plain')

                        axs[i, 1].set_title(layer_name)
                        axs[i, 1].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                        axs[i, 1].grid(True)

                        axs[i, 1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                        axs[i, 1].ticklabel_format(useOffset=False, axis='y', style='plain')

                    extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                    station_range_text = axs[0,0].text(-0.2, 1.4, f"{selected_station_solution} vs {selected_secondStation_solution}      {extend_time}", transform=axs[0,0].transAxes, va='top', ha='left', fontsize=11)
                    axs[0,0].text(-0.1, 1.2, '{:>11}'.format('[m]'), transform=axs[0,0].transAxes, va='top', ha='left', fontsize=10)
                    axs[-1,0].set_xlabel(xaxis_label, font="Verdana")

                    fig.subplots_adjust(left=0.099,right=0.98, hspace=0.4, wspace=0.2)
                    
                    layers_widget, canvas_widget, toolbar_widget = plot_frames(fig, plot_frame, layers_frame, time_data, lines, axs, data_listname, station_range_text, selected_station_solution, selected_secondStation_solution, cord_time, cord1, cord2, sol_df, layer_name)
                    layer_buttons_comp(axs, layers_widget)
                
                def plot_ground(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget

                    clear_plot()

                    fig, axs = plt.subplots(figsize=(12,5))

                    x_axs = time_data.loc[time_data["Sol"] == solutions[0], data_listname[0]]
                    y_axs = time_data.loc[time_data["Sol"] == solutions[0], data_listname[1]]
                    x_axs2 = time_data.loc[time_data["Sol"] == solutions[1], data_listname[0]]
                    y_axs2 = time_data.loc[time_data["Sol"] == solutions[1], data_listname[1]]

                    axs.grid(True)
                    
                    line1 = axs.scatter(x_axs, y_axs, color="red", zorder=3, s=10)
                    line2 = axs.scatter(x_axs2, y_axs2, color="green", zorder=4, s=10)
                    lines = [line1, line2]

                    invisible_line1, = axs.plot(x_axs, y_axs, color='none')
                    invisible_line2, = axs.plot(x_axs2, y_axs2, color='none')
                    invisible_lines = [invisible_line1, invisible_line2]
               

                    extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                    station_range_text = axs.text(-0.12, 1.10, f"{selected_station_solution} vs {selected_secondStation_solution}      {extend_time}", transform=axs.transAxes, va='top', ha='left', fontsize=11)
                    
                    
                    fig.subplots_adjust(hspace=0.4, wspace=0.3)
                    axs.set_title(selected_data, font="Verdana", fontsize=14, fontweight="light")

                    formatter = ScalarFormatter(useOffset=False, useMathText=False)
                    formatter.set_scientific(False) 

                    axs.xaxis.set_major_formatter(formatter)
                    axs.yaxis.set_major_formatter(formatter)

                    data_to_slider = time_data.loc[time_data["Sol"] == solutions[0]]
                                                                            
                    layers_widget, canvas_widget, toolbar_widget = plot_frames(fig, plot_frame, layers_frame, time_data, lines, axs, invisible_lines, station_range_text, selected_station_solution, selected_secondStation_solution, data_to_slider, x_axs, y_axs, x_axs2, y_axs2)
                    
                    layer_buttons(fig, axs, [selected_solution, selected_secondSolution], layers_widget, data_colors=["red", "green"])

                def clear_plot():
                    global canvas_widget, toolbar_widget, layers_widget

                    if canvas_widget is not None:
                        canvas_widget.destroy()
                        canvas_widget = None
                    if toolbar_widget is not None:
                        toolbar_widget.destroy()
                        toolbar_widget = None
                    if layers_widget is not None:
                        layers_widget.destroy()
                        layers_widget = None

                

                def on_option_change(choice):
                    if choice == "Ground track":
                        plot_ground(plot_frame, layers_frame)
                        
                    elif choice == "Position":
                        plot_position(plot_frame, layers_frame)

                                      

                new_window = ctk.CTkToplevel(app)
                new_window.title("PLOT")
                center_window(new_window, 1300, 650)
                
                def new_window_lvl():
                    new_window.attributes("-topmost", False)
                new_window.attributes("-topmost", True)
                new_window.after(500, new_window_lvl)

                plot_frame = ctk.CTkFrame(new_window)
                plot_frame.pack(side=ctk.LEFT, fill="both", expand=True)
                

                right_frame = ctk.CTkFrame(new_window, width=500)
                right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

                plot_view_label = ctk.CTkLabel(right_frame, text="View:", font=("Helvetica", 22))
                plot_view_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 10), padx=70)

                plot_view_variable = ctk.StringVar(value="Position")
                plot_view = ctk.CTkOptionMenu(right_frame, width=150, values=["Position", "Ground track"], variable=plot_view_variable, command=on_option_change)
                plot_view.pack(side=ctk.TOP, pady=(0,20))
                plot_view.set("Position")

                layers_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
                layers_frame.pack(side=ctk.TOP, fill=ctk.BOTH)

                
                plot_position(plot_frame, layers_frame)