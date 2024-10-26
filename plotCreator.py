import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkinter import messagebox
import customtkinter as ctk
from dataConfiguration import match_data
from matplotlib.ticker import ScalarFormatter
from centerWindow import center_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from solutionGenerator import solution_generator

def defining_data():
    global data_dict
    data_dict = {"PDop": "DOP factors", 
                "RecX": "REC XYZ", 
                "RecmX": "RECm XYZ", 
                "mIonDel": "ION"}
    return data_dict

single_plot = ["DOP factors", "ION"]
triple_plot = ["REC XYZ", "RECm XYZ"]



def create_plot(start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, data, selected_data, selected_station, station_list, filepaths, app):
    global loading_check

    def toggle_visibility(name):
        name.set_visible(not name.get_visible())
        plt.draw()

    start_time = f"{start_year_entry.get()} {start_hour_entry.get()}"
    end_time = f"{end_year_entry.get()} {end_hour_entry.get()}"

    if start_time > end_time:
        messagebox.showinfo("Message", "Starting time must be less than end time")

    else:
        time_data = data.loc[(data['datetime'] >= start_time) & (data['datetime'] <= end_time)]
        data_listname, x = match_data(selected_data)
        cut_column = data_listname
        cut_column.insert(0, "Stat")
        cut_column.insert(0, "datetime")
        cut_data = time_data[cut_column]
        cut_data.loc[:, "Sol"] = solution_generator(selected_station.split("(")[1].split(")")[0])
        time_diff = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        if (time_diff > timedelta(days=365*2)): # individual function
            xaxis_set = "%y"
            xaxis_label = "TIME [year]"
        elif (time_diff <= timedelta(days=365*2)) and (time_diff > timedelta(days=6*31)):
            xaxis_set = "%y-%m"
            xaxis_label = "TIME [year-month]"
        elif (time_diff <= timedelta(days=6*31)) and (time_diff > timedelta(days=2*31)):
            xaxis_set = "%m-%d"
            xaxis_label = "TIME [month-day]"
        elif (time_diff <= timedelta(days=2*31)) and (time_diff > timedelta(days=31)):
            xaxis_set = "%m-%d %H"
            xaxis_label = "TIME [month-day hour]"
        elif (time_diff <= timedelta(days=31)) and (time_diff > timedelta(days=1)):
            xaxis_set = "%d %H:%M"
            xaxis_label = "TIME [day hour:min]"
        elif (time_diff <= timedelta(hours=24)) and (time_diff > timedelta(hours=1)):
            xaxis_set = "%H:%M"
            xaxis_label = "TIME [hour:min]"
        elif time_diff < timedelta(minutes=60):
            xaxis_set = "%M:%S"
            xaxis_label = "TIME [min:sec]"
        else:
            xaxis_set = "%Y-%m-%d %H:%M"
            xaxis_label = "TIME [year-month-day hour:min]"

        if selected_data in single_plot:

            def plot():
                fig, ax = plt.subplots(figsize=(10,6))
                
                plots = {}
                plot_objects = []

                for layer_name, color in zip(data_listname, data_colors):
                    plots[layer_name], = ax.plot(cut_data["datetime"], cut_data[layer_name], color=color, linewidth=1, label=layer_name)
                    plot_objects.append(plots[layer_name])

                ax.set_title(selected_data, font="Verdana", fontsize=14, fontweight="light")
                ax.set_xlabel(xaxis_label, font="Verdana")
                ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                ax.grid(True)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                ax.ticklabel_format(useOffset=False, axis='y', style='plain')
                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax.text(-0.12, 1.10, f"{selected_station}, {extend_time}", transform=ax.transAxes, va='top', ha='left', fontsize=11)

                return plot_objects, fig, ax
            
            def layer_buttons(ax):
                for i, layer_name in enumerate(data_listname):
                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(anchor="w", padx=10, pady=5)

                    # Buttons
                    toggle_button = ctk.CTkCheckBox(layer_frame, text=layer_name, command=lambda idx=i: toggle_visibility(data_list[idx]))
                    toggle_button.grid(row=0, column=0)
                    toggle_button.select()

                    # Buttons line
                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
                    buttons_line.grid(row=0, column=1, padx=(5, 5))

        elif selected_data in triple_plot:
            def plot():
                fig, ax = plt.subplots(3, 1, figsize=(10,6))
                
                for i, layer_name in enumerate(data_listname):

                    line, = ax[i].plot(cut_data["datetime"], cut_data[layer_name], color=data_colors[i], linewidth=1, label=layer_name)
                    ax[i].set_title(layer_name)
                    ax[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                    ax[i].grid(True)
                    ax[i].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                    ax[i].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                    ax[i].ticklabel_format(useOffset=False, axis='y', style='plain')

                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax[0].text(-0.2, 1.5, f"{selected_station}, {extend_time}", transform=ax[0].transAxes, va='top', ha='left', fontsize=11)
                ax[0].text(-0.1, 1.2, '{:>13}'.format('[m]'), transform=ax[0].transAxes, va='top', ha='left', fontsize=10)
                ax[-1].set_xlabel(xaxis_label, font="Verdana")

                fig.tight_layout()
                plot_objects = []
                return plot_objects, fig, ax

            def layer_buttons(ax):
                for i, ax in enumerate(ax):
                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(anchor="w", padx=10, pady=5)

                    # Buttons
                    toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax.get_lines()[0]: toggle_visibility(line))
                    toggle_button.grid(row=0, column=0)
                    toggle_button.select()

                    # Buttons line
                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
                    buttons_line.grid(row=0, column=2, padx=(0, 5))

        data_listname, data_colors = match_data(selected_data)

        plot_objects, fig, ax = plot()
        data_list = plot_objects

        new_window = ctk.CTkToplevel(app)
        new_window.title("PLOT")

        center_window(new_window, 1200, 650)

        right_frame = ctk.CTkFrame(new_window,)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

        
        layers_frame = ctk.CTkFrame(right_frame)
        layers_frame.pack(side=ctk.TOP, fill=ctk.Y)

        layers_label = ctk.CTkLabel(layers_frame, text="Layers", font=("Helvetica", 22))
        layers_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 50))

        layer_buttons(ax)

        

        if selected_station in station_list:
            station2_list = station_list.copy()
            station2_list.remove(selected_station)


        secondStation_frame = ctk.CTkFrame(right_frame)
        secondStation_frame.pack(side=ctk.TOP, fill=ctk.X)

        secondStation_label = ctk.CTkLabel(secondStation_frame, text="Compare data \nwith second station", font=("Helvetica", 16))
        secondStation_label.pack(side=ctk.TOP, fill=ctk.X, pady=(50, 20))

        station2_menu_variable = ctk.StringVar(value="Select station ...")
        station2_menu = ctk.CTkOptionMenu(secondStation_frame, width=150, values=[], variable=station2_menu_variable)#, command=read_data_in_thread)
        station2_menu.pack(side=ctk.TOP, pady=(0, 20))
        station2_menu.configure(values=station2_list)

        def comparing_window():
            selected_station_solution2 = station2_menu.get()
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
            data2 = pd.read_csv(filepath[0], sep=';', index_col=False, skipinitialspace=True) #może gdzieś tu usunąć niepotrzebne kolumny
            data2 = time_column(data2)
            data2 = merge_data(data2, selected_data, filepath)

            cut_data2 = data2[cut_column]
            cut_data2.loc[:, "Sol"] = solution_generator(selected_station_solution2.split("(")[1].split(")")[0])
            cut_data_merged = pd.concat([cut_data, cut_data2])
            time_data = cut_data_merged.loc[(cut_data_merged['datetime'] >= start_time) & (cut_data_merged['datetime'] <= end_time)]

            solutions = [solution_generator(selected_station.split("(")[1].split(")")[0]), solution_generator(selected_station_solution2.split("(")[1].split(")")[0])]

            def solution_dataframe(time_data, data_listname, solutions):
                sol_df = time_data[time_data["Sol"] == solutions[0]].reset_index(drop=True)

                for layer_name in data_listname:
                    cords1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name]
                    cords2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name]
                    sol_df[layer_name] = cords1 - cords2

                return sol_df

            def plot():
                fig, ax = plt.subplots(3, 2, figsize=(12,6))
                plot_objects = []

                sol_df = solution_dataframe(time_data, data_listname, solutions)

                for i, layer_name in enumerate(data_listname):
                    cord_time = time_data.loc[time_data["Sol"] == solutions[0], "datetime"]
                    cord1 = time_data.loc[time_data["Sol"] == solutions[0], layer_name]
                    cord2 = time_data.loc[time_data["Sol"] == solutions[1], layer_name]
                    
                    line, = ax[i, 0].plot(cord_time, cord2, color="red")
                    line, = ax[i, 0].plot(cord_time, cord1, color="green")
                    line, = ax[i, 1].plot(cord_time, sol_df[layer_name], color="blue")
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
                ax[0,0].text(-0.2, 1.5, f"{selected_station}, {extend_time}", transform=ax[0,0].transAxes, va='top', ha='left', fontsize=11)
                ax[0,0].text(-0.1, 1.2, '{:>13}'.format('[m]'), transform=ax[0,0].transAxes, va='top', ha='left', fontsize=10)
                ax[-1,0].set_xlabel(xaxis_label, font="Verdana")

                ax[0,0].text(-0.2, 1.5, f"{selected_station}, {extend_time}", transform=ax[0,0].transAxes, va='top', ha='left', fontsize=11)
                ax[0,0].text(-0.1, 1.2, '{:>13}'.format('[m]'), transform=ax[0,0].transAxes, va='top', ha='left', fontsize=10)
                ax[-1,0].set_xlabel(xaxis_label, font="Verdana")

                fig.tight_layout()
                return plot_objects, fig, ax
            
            # def layer_buttons(ax):
            #     for i, ax in enumerate(ax):
            #         layer_frame = ctk.CTkFrame(layers_frame2)
            #         layer_frame.pack(anchor="w", padx=10, pady=5)

            #         toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax.get_lines()[0,0]: toggle_visibility(line))
            #         toggle_button.grid(row=0, column=0)
            #         toggle_button.select()

            #         buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
            #         buttons_line.grid(row=0, column=2, padx=(0, 5))

            
            plot_objects, fig, ax = plot()
            data_list = plot_objects


            new_window2 = ctk.CTkToplevel(app)
            new_window2.title("PLOT")

            center_window(new_window2, 1200, 650)

            right_frame2 = ctk.CTkFrame(new_window2,)
            right_frame2.pack(side=ctk.RIGHT, fill=ctk.Y)

            
            layers_frame2 = ctk.CTkFrame(right_frame2)
            layers_frame2.pack(side=ctk.TOP, fill=ctk.Y)

            layers_label = ctk.CTkLabel(layers_frame, text="Layers", font=("Helvetica", 22))
            layers_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 50))

            # layer_buttons(ax)

            canvas_plot = FigureCanvasTkAgg(fig, master=new_window2)
            canvas_plot.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        
        compare_button = ctk.CTkButton(secondStation_frame, text="Compare", command=comparing_window)
        compare_button.pack(side=ctk.TOP)

        



        canvas_plot = FigureCanvasTkAgg(fig, master=new_window)
        canvas_plot.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas_plot, new_window)
        toolbar.update()