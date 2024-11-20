import matplotlib.pyplot as plt
import customtkinter as ctk
import numpy as np

from dataConfiguration import defining_data, match_data
from matplotlib.ticker import ScalarFormatter
from datetime import datetime
from centerWindow import center_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from solutionGenerator import solution_generator
from frames import plot_frames

data_dict, single_plot, triple_plot = defining_data()


def comparing_window(station2_menu_fullVar, filepaths, selected_data, cut_data, cut_column, selected_station, error_label, 
                     start_time, end_time, station_list, xaxis_set, xaxis_label, app):
            
            data_listname, data_colors = match_data(selected_data)

            selected_station_solution2 = station2_menu_fullVar.get()
            selected_station2 = selected_station_solution2.split(" ")[0]
            selected_solution2 = solution_generator(selected_station_solution2.split("(")[1].split(")")[0])

            filepaths_cut = [filepath for filepath in filepaths if selected_station2 in filepath and selected_solution2 in filepath]
            
            filepath = []
            for key, value in data_dict.items():
                if value == selected_data:
                    for i in filepaths_cut:
                        with open(i, "r") as file:
                            first_row = file.readline()
                            if key in first_row:
                                filepath.append(i)
            import pandas as pd
            from dataConfiguration import merge_data, time_column
            data2 = pd.read_csv(filepath[0], sep=';', index_col=False, skipinitialspace=True)
            data2 = time_column(data2)
            data2 = merge_data(data2, selected_data, filepath)
            cut_data2 = data2[cut_column]
            cut_data2 = cut_data2.copy()
            cut_data2.loc[:, "Sol"] = selected_solution2
            solutions = [solution_generator(selected_station.split("(")[1].split(")")[0]), solution_generator(selected_station_solution2.split("(")[1].split(")")[0])]
            has_common_times = not set(cut_data['datetime']).isdisjoint(cut_data2['datetime'])
            
            if has_common_times:
                error_label.delete("1.0", "end")
                error_label.see("end")
                
                #Empty cell
                all_times = pd.DataFrame({'datetime': pd.concat([cut_data['datetime'], cut_data2['datetime']]).unique()})

                if cut_data["Sol"].iloc[0] == cut_data2["Sol"].iloc[0]:
                    cut_data1_full = pd.merge(all_times, cut_data, on='datetime', how='left').assign(Stat=selected_station)
                    cut_data2_full = pd.merge(all_times, cut_data2, on='datetime', how='left').assign(Stat=selected_station_solution2)
                else:
                    cut_data1_full = pd.merge(all_times, cut_data, on='datetime', how='left').assign(Sol=solutions[0])
                    cut_data2_full = pd.merge(all_times, cut_data2, on='datetime', how='left').assign(Sol=solutions[1])

                cut_data_merged = pd.concat([cut_data1_full, cut_data2_full], ignore_index=True).sort_values(by='datetime').reset_index(drop=True)
                time_data = cut_data_merged.loc[(cut_data_merged['datetime'] >= start_time) & (cut_data_merged['datetime'] <= end_time)]
                time_data = time_data.copy()
                colors2 = ["dodgerblue", "pink", "orange"]

                def solution_dataframe(time_data, data_listname, solutions):
                    sol_df = time_data[time_data["Sol"] == solutions[0]].reset_index(drop=True)

                    if cut_data["Sol"].iloc[0] == cut_data2["Sol"].iloc[0]:
                        
                        for layer_name in data_listname:
                            cords1 = time_data.loc[time_data["Stat"] == selected_station, layer_name].reset_index(drop=True)
                            cords2 = time_data.loc[time_data["Stat"] == selected_station_solution2, layer_name].reset_index(drop=True)
                            sol_df[layer_name] = cords1 - cords2
                            
                    else:
                        for layer_name in data_listname:
                            cords1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name].reset_index(drop=True)
                            cords2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name].reset_index(drop=True)
                            sol_df[layer_name] = cords1 - cords2
                        
                    return sol_df
                
                global canvas_widget, toolbar_widget, layers_widget
                canvas_widget = None
                toolbar_widget = None
                layers_widget = None
                
                def plot_position(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget

                    def layer_buttons(ax, layers_frame_on):
                        def toggle_visibility(name):
                            name.set_visible(not name.get_visible())
                            plt.draw()

                        layer_list = [selected_station, selected_station_solution2, "Difference"]

                        layer_dict = {
                            selected_station: 0,
                            selected_station_solution2: 0,
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

                                layer_frame = ctk.CTkFrame(layers_frame_on, fg_color="#404040")
                                layer_frame.pack(side=ctk.TOP, padx=10, pady=5)

                                toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[j], command=lambda line=ax[j, layer_dict[key]].get_lines()[i]: toggle_visibility(line))
                                toggle_button.grid(row=0, column=0, padx=2, pady=2)
                                toggle_button.select()
                                
                                if key == layer_list[0] or key == layer_list[2]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[j])
                                elif key == layer_list[1]:
                                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=colors2[j])
                                
                                buttons_line.grid(row=0, column=2, padx=(0, 5))


                    clear_plot()

                    fig, ax = plt.subplots(3, 2, figsize=(13,5))

                    for i, layer_name in enumerate(data_listname):
                        if cut_data["Sol"].iloc[0] == cut_data2["Sol"].iloc[0]:
                            sol_df = solution_dataframe(time_data, data_listname, station_list).reset_index(drop=True)
                            cord_time = time_data.loc[time_data["Stat"] == selected_station, "datetime"].reset_index(drop=True)
                            cord1 = time_data.loc[time_data["Stat"] == selected_station, layer_name].reset_index(drop=True)
                            cord2 = time_data.loc[time_data["Stat"] == selected_station_solution2, layer_name].reset_index(drop=True)

                        else:
                            sol_df = solution_dataframe(time_data, data_listname, solutions).reset_index(drop=True)
                            cord_time = time_data.loc[time_data["Sol"] == solutions[0], "datetime"].reset_index(drop=True)
                            cord1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name].reset_index(drop=True)
                            cord2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name].reset_index(drop=True)

                        
                        line, = ax[i, 0].plot(cord_time, cord2, color=data_colors[i])
                        line, = ax[i, 0].plot(cord_time, cord1, color=colors2[i])
                        line, = ax[i, 1].plot(cord_time, sol_df[layer_name], color=data_colors[i])
                        ax[i, 0].set_title(layer_name)
                        ax[i, 0].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                        ax[i, 0].grid(True)

                        ax[i, 0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                        ax[i, 0].ticklabel_format(useOffset=False, axis='y', style='plain')

                        ax[i, 1].set_title(layer_name)
                        ax[i, 1].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                        ax[i, 1].grid(True)

                        ax[i, 1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                        ax[i, 1].ticklabel_format(useOffset=False, axis='y', style='plain')

                    extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                    ax[0,0].text(-0.2, 1.4, f"{selected_station} vs {selected_station_solution2}      {extend_time}", transform=ax[0,0].transAxes, va='top', ha='left', fontsize=11)
                    ax[0,0].text(-0.1, 1.2, '{:>11}'.format('[m]'), transform=ax[0,0].transAxes, va='top', ha='left', fontsize=10)
                    ax[-1,0].set_xlabel(xaxis_label, font="Verdana")

                    fig.subplots_adjust(left=0.099,right=0.98, hspace=0.4, wspace=0.2)
                    
                    layers_widget, canvas_widget, toolbar_widget = plot_frames(fig, plot_frame, layers_frame)
                    layer_buttons(ax, layers_widget)


                
                def plot_ground(plot_frame, layers_frame):
                    global canvas_widget, toolbar_widget, layers_widget
                    
                    clear_plot()

                    fig, ax = plt.subplots(figsize=(12,5))
                    
                    x_ax = time_data.loc[time_data["Sol"] == solutions[0], data_listname[0]]
                    y_ax = time_data.loc[time_data["Sol"] == solutions[0], data_listname[1]]
                    x_ax2 = time_data.loc[time_data["Sol"] == solutions[1], data_listname[0]]
                    y_ax2 = time_data.loc[time_data["Sol"] == solutions[1], data_listname[1]]
                    median_x = np.nanmedian(x_ax)
                    median_y = np.nanmedian(y_ax)
                    ax.grid(True)

                    ax.axhline(median_y, color='black', linewidth=1, linestyle='-', zorder=1)
                    ax.axvline(median_x, color='black', linewidth=1, linestyle='-', zorder=2)
                    ax.scatter(x_ax, y_ax, color="red", zorder=3, s=10)
                    ax.scatter(x_ax2, y_ax2, color="green", zorder=4, s=10)
                    
                    
                    fig.subplots_adjust(hspace=0.4, wspace=0.3)
                    ax.set_title(selected_data, font="Verdana", fontsize=14, fontweight="light")

                    formatter = ScalarFormatter(useOffset=False, useMathText=False)
                    formatter.set_scientific(False) 

                    ax.xaxis.set_major_formatter(formatter)
                    ax.yaxis.set_major_formatter(formatter)

                    layers_widget, canvas_widget, toolbar_widget = plot_frames(fig, plot_frame, layers_frame)

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
                center_window(new_window, 1250, 650)
                
                def new_window_lvl():
                    new_window.attributes("-topmost", False)
                new_window.attributes("-topmost", True)
                new_window.after(500, new_window_lvl)

                plot_frame = ctk.CTkFrame(new_window)
                plot_frame.pack(side=ctk.LEFT, fill="both", expand=True)
                

                right_frame = ctk.CTkFrame(new_window, fg_color="#333333")
                right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

                plot_view_label = ctk.CTkLabel(right_frame, text="View:", font=("Helvetica", 22))
                plot_view_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 10))

                plot_view_variable = ctk.StringVar(value="Position")
                plot_view = ctk.CTkOptionMenu(right_frame, width=150, values=["Position", "Ground track"], variable=plot_view_variable, command=on_option_change)
                plot_view.pack(side=ctk.TOP, pady=(0,20))
                plot_view.set("Position")

                layers_frame = ctk.CTkFrame(right_frame)
                layers_frame.pack(side=ctk.TOP, fill=ctk.Y)


                plot_position(plot_frame, layers_frame)

            else:
                error_label.configure(state="normal")
                text = "The second station doesn't have common time"
                if (len(error_label.get("1.0", "end"))) == 1:
                    error_label.insert("end", text)
                    
                error_label.configure(state="disabled")