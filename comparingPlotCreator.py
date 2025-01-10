import matplotlib.pyplot as plt
import customtkinter as ctk
import pandas as pd
import numpy as np

from matplotlib.ticker import ScalarFormatter
from datetime import datetime

from components.dataConfiguration import merge_data, time_column, cutting_columns, cutting_rows, defining_data, match_data_before, match_data_after, triple_plot_corrections
from components.centerWindow import center_window
from components.solutionGenerator import solution_generator
from components.frames import plot_frames
from components.statistcs import calc_statistics
from components.calculateNewColumns import calculate_new_columns
from components.axisLabel import yaxis_label

data_dict, single_scatter, single_plot, triple_plot = defining_data()


def comparing_window(secondStation_menu_fullVar, filepaths, selected_data, firstData, selected_station_solution, error_label, 
                     start_time, end_time, station_list, xaxis_set, xaxis_label, app):

            selected_data = ["REC NEU" if item in ['RecN', 'RecE', 'RecU'] else item for item in selected_data]
            selected_data = ["REC XYZ" if item in ['RecX', 'RecY', 'RecZ'] else item for item in selected_data]
            selected_data = list(dict.fromkeys(selected_data))

            data_listnames = match_data_before(selected_data)
            data_colors = 0
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
                    for selected in selected_data:
                        if value == selected:
                            for filepath_cut in filepaths_cut:
                                with open(filepath_cut, "r") as file:
                                    first_row = file.readline()
                                    if key in first_row:
                                        if filepath_cut not in filepath:
                                            if "Eztd" not in filepaths_cut:
                                                filepath.append(filepath_cut)

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
                    secondData = calculate_new_columns(secondData, selected_data, solutions, filepath)
                    secondData.replace([np.inf, -np.inf], np.nan, inplace=True)
                    secondData = cutting_columns(secondData, data_listnames, selected_secondSolution)
                    secondData = cutting_rows(secondData, data_listnames)

                    has_common_times = not set(firstData['datetime']).isdisjoint(secondData['datetime'])

            
            if not has_common_times:
                error_message("The second station doesn't have common time")
                
            else:
                error_label.configure(state="normal")
                error_label.delete("0.0", "end")
                error_label.configure(state="disabled")
                
                
                #Empty cell
                all_times = pd.DataFrame({'datetime': pd.concat([firstData['datetime'], secondData['datetime']]).unique()})

                firstData1_full = pd.merge(all_times, firstData, on='datetime', how='left').assign(Sol=solutions[0])
                secondData_full = pd.merge(all_times, secondData, on='datetime', how='left').assign(Sol=solutions[1])

                data_merged = pd.concat([firstData1_full, secondData_full], ignore_index=True).sort_values(by='datetime').reset_index(drop=True)
                data_merged = data_merged.loc[(data_merged['datetime'] >= start_time) & (data_merged['datetime'] <= end_time)]

                def difference_dataframe(data_merged, data_listnames, solutions):
                    diff_df = data_merged[["datetime"]]
                    diff_df = diff_df.drop_duplicates().reset_index(drop=True)

                    for layer_name in data_listnames:
                        cords1 = data_merged.loc[data_merged["Sol"] == solutions[0], layer_name].reset_index(drop=True)
                        cords2 = data_merged.loc[data_merged["Sol"] == solutions[1], layer_name].reset_index(drop=True)
                        diff_df[layer_name] = cords1 - cords2

                    return diff_df
                
                global canvas_widget, toolbar_widget, layers_widget, entry_widget, toolbar_slider_frame
                canvas_widget = None
                toolbar_widget = None
                layers_widget = None
                entry_widget= None

                data_listnames = match_data_after(selected_data, solutions)
                data_listnames = [item for sublist in data_listnames for item in sublist]
                data_colors = ["red", "green", "blue"]
                diff_df = difference_dataframe(data_merged, data_listnames, solutions).reset_index(drop=True)

            
                def plot_position(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget, entry_widget
                    
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

                                toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listnames[j], command=lambda line=ax[j, layer_dict[key]].get_lines()[i]: toggle_visibility(line))
                                toggle_button.grid(row=0, column=0, padx=2, pady=2)
                                toggle_button.select()
                                
                                if key == layer_list[0]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color="limegreen")
                                elif key == layer_list[1]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color="orange")
                                elif key == layer_list[2]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[j])
                                
                                
                                buttons_line.grid(row=0, column=2, padx=(0, 5))

                    clear_plot()

                    fig, axs = plt.subplots(3, 2, figsize=(13,5))
                    lines = []


                    for data_listname, ax, i in zip(data_listnames, axs, range(len(data_listnames))):
 
                        data_list1 = data_merged.loc[data_merged["Sol"] == solutions[0], data_listname].tolist()
                        data_list2 = data_merged.loc[data_merged["Sol"] == solutions[1], data_listname].tolist()

                        line, = ax[0].plot(diff_df["datetime"], data_list1, color="limegreen", linewidth=1, zorder=2, label=f"{data_listname} {solution_generator(solutions[0])}")
                        lines.append(line,)
                        line, = ax[0].plot(diff_df["datetime"], data_list2, color="orange", linewidth=1, zorder=2, label=f"{data_listname} {solution_generator(solutions[1])}")
                        lines.append(line,)
                        line, = ax[1].plot(diff_df["datetime"], diff_df[data_listname], color=data_colors[i], linewidth=1, zorder=2, label=f"{data_listname} diff")
                        lines.append(line,)
                        
                        for j in range(len(ax)):
                            ax[j].legend()
                            ax[j].grid(True, zorder=1)
                            ax[j].xaxis.set_tick_params(labelbottom=False)
                            ax[j].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                            ax[j].ticklabel_format(useOffset=False, axis='y', style='plain')
                            ax[j].set_ylabel(yaxis_label(data_listnames[i]) + " [m]")
                            ax[j].set_xlim(data_merged["datetime"].min() - 0.01*(data_merged["datetime"].max() - data_merged["datetime"].min()), 
                                        data_merged["datetime"].max() + 0.01*(data_merged["datetime"].max() - data_merged["datetime"].min()))
                            

                    extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                    station_range_text = fig.suptitle(f"{selected_station_solution} vs {selected_secondStation_solution}      {extend_time}", fontsize=11, color='black', y=0.95)

                    axs[0,0].yaxis.set_label_coords(-0.18, 0.5)
                    axs[1,0].yaxis.set_label_coords(-0.18, 0.5)
                    axs[2,0].yaxis.set_label_coords(-0.18, 0.5)
                    axs[0,1].yaxis.set_label_coords(-0.1, 0.5)
                    axs[1,1].yaxis.set_label_coords(-0.1, 0.5)
                    axs[2,1].yaxis.set_label_coords(-0.1, 0.5)
                    

                    axs[-1,0].set_xlabel(xaxis_label, font="Verdana")
                    axs[-1,1].set_xlabel(xaxis_label, font="Verdana")
                    axs[-1,0].xaxis.set_tick_params(labelbottom=True)
                    axs[-1,0].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                    axs[-1,1].xaxis.set_tick_params(labelbottom=True)
                    axs[-1,1].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))

                    fig.subplots_adjust(left=0.099,right=0.98, hspace=0.4, wspace=0.2)
                    invisible_lines = []
                    layers_widget, canvas_widget, toolbar_widget, entry_widget = plot_frames(fig, plot_frame, layers_frame, toolbar_slider_frame, data_merged, lines, axs, data_listnames, station_range_text, selected_station_solution, selected_secondStation_solution, solutions, invisible_lines, diff_df, "entry")
                    layer_buttons_comp(axs, layers_widget)
                
                def plot_ground(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget, entry_widget

                    clear_plot()

                    fig, axs = plt.subplots(figsize=(10,5))

                    x_axs = data_merged.loc[data_merged["Sol"] == solutions[0], data_listnames[0]].reset_index(drop=True)
                    y_axs = data_merged.loc[data_merged["Sol"] == solutions[0], data_listnames[1]].reset_index(drop=True)
                    x_axs2 = data_merged.loc[data_merged["Sol"] == solutions[1], data_listnames[0]].reset_index(drop=True)
                    y_axs2 = data_merged.loc[data_merged["Sol"] == solutions[1], data_listnames[1]].reset_index(drop=True)

                    axs.grid(True)
                    
                    line1 = axs.scatter(x_axs, y_axs, color="limegreen", zorder=3, s=10, label=selected_solution)
                    line2 = axs.scatter(x_axs2, y_axs2, color="orange", zorder=4, s=10, label=selected_secondSolution)
                    lines = [line1, line2]

                    invisible_line1, = axs.plot(x_axs, y_axs, color='none')
                    invisible_lines = [invisible_line1]

                    extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                    station_range_text = fig.suptitle(f"{selected_station_solution} vs {selected_secondStation_solution}      {extend_time}", fontsize=11, color='black', y=0.95)
                    
                    
                    fig.subplots_adjust(left=0.099,right=0.98, hspace=0.4, wspace=0.2)
                    axs.set_title(selected_data[0][:-1] + " [m]", font="Verdana", fontsize=14, fontweight="light")
                    axs.legend(framealpha=0.5)
                    formatter = ScalarFormatter(useOffset=False, useMathText=False)
                    formatter.set_scientific(False) 

                    axs.xaxis.set_major_formatter(formatter)
                    axs.yaxis.set_major_formatter(formatter)

   

                    layers_widget, canvas_widget, toolbar_widget, entry_widget = plot_frames(fig, plot_frame, layers_frame, toolbar_slider_frame, data_merged, lines, axs, data_listnames[:2], station_range_text, selected_station_solution, selected_secondStation_solution, solutions, invisible_lines, diff_df, "entry")
                    
                    def layer_buttons_ground(solutions, layers_frame_on, data_listnames, ax, colors):
                        def toggle_visibility(name):
                            name.set_visible(not name.get_visible())
                            plt.draw()

                        data_listnames = data_listnames[:2]

                        for solution, layer, i, color in zip(solutions, data_listnames, range(len(solutions)), colors):
                            layer_label = ctk.CTkLabel(layers_frame_on, text=solution)
                            layer_label.pack(padx=15, pady=(10,5))
                            
                            layer_frame = ctk.CTkFrame(layers_frame_on)
                            layer_frame.pack(side=ctk.TOP, padx=10, pady=5)

                            toggle_button = ctk.CTkCheckBox(layer_frame, text="      ", width=50, command=lambda line=ax.collections[i]: toggle_visibility(line))
                            toggle_button.pack(side=ctk.LEFT, padx=2, pady=2)
                            toggle_button.select()

                            buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=color)
                            buttons_line.pack(side=ctk.LEFT, padx=(0, 5))

                    layer_buttons_ground([selected_solution, selected_secondSolution], layers_widget, data_listnames, axs, ["limegreen", "orange"])


                def clear_plot():
                    global canvas_widget, toolbar_widget, layers_widget, entry_widget

                    if canvas_widget is not None:
                        canvas_widget.destroy()
                        canvas_widget = None
                    if toolbar_widget is not None:
                        toolbar_widget.destroy()
                        toolbar_widget = None
                    if layers_widget is not None:
                        layers_widget.destroy()
                        layers_widget = None
                    if entry_widget is not None:
                        entry_widget.destroy()
                        entry_widget = None


                def on_option_change(choice):
                    if choice == "Ground track" or choice == "Trajectory":
                        plot_ground(plot_frame, layers_frame)
                        
                    elif choice == "Position":
                        plot_position(plot_frame, layers_frame)

                                      

                new_window = ctk.CTkToplevel(app)
                new_window.title("PLOT")
                center_window(new_window, 1350, 740)
                
                def new_window_lvl():
                    new_window.attributes("-topmost", False)
                new_window.attributes("-topmost", True)
                new_window.after(500, new_window_lvl)


                plot_frame = ctk.CTkFrame(new_window)                

                right_frame = ctk.CTkFrame(new_window, width=200)

                plot_view_label = ctk.CTkLabel(right_frame, text="View:", font=("Helvetica", 22))

                plot_view_variable = ctk.StringVar(value="Position")
                
                if selected_data == ["REC XYZ"]:
                    view_values = ["Position", "Trajectory"]
                elif selected_data == ["REC NEU"]:
                    view_values = ["Position", "Ground track"]
                
                plot_view = ctk.CTkOptionMenu(right_frame, values=view_values, variable=plot_view_variable, command=on_option_change)
                plot_view.set("Position")

                layers_frame = ctk.CTkFrame(right_frame, fg_color="transparent")

                toolbar_slider_frame = ctk.CTkFrame(new_window, fg_color="#F0F0F0", corner_radius=0)

                plot_position(plot_frame, layers_frame)

                toolbar_slider_frame.pack(side=ctk.BOTTOM, fill=ctk.X)
                plot_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
                right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH)
                plot_view_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 10))
                plot_view.pack(side=ctk.TOP, pady=(0,20), padx=20)
                layers_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)