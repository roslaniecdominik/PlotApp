import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkinter import messagebox
import customtkinter as ctk
from dataConfiguration import match_data, defining_data
from matplotlib.ticker import ScalarFormatter
from centerWindow import center_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from solutionGenerator import solution_generator
from layerButtons import layer_buttons
from comparingPlotCreator import comparing_window

data_dict, single_plot, triple_plot = defining_data()

def create_plot(start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, data, selected_data, selected_station, station_list, filepaths, app):
    global loading_check

    start_time = f"{start_year_entry.get()} {start_hour_entry.get()}"
    end_time = f"{end_year_entry.get()} {end_hour_entry.get()}"

    if start_time > end_time:
        messagebox.showinfo("Message", "Starting time must be less than end time")

    else:
        time_data = data.loc[(data['datetime'] >= start_time) & (data['datetime'] <= end_time)]
        data_listname, x = match_data(selected_data)
        cut_column = data_listname
        cut_column.insert(0, "datetime")

        cut_data = time_data[cut_column]
        cut_data = cut_data.copy()
        cut_data.loc[:, "Sol"] = solution_generator(selected_station.split("(")[1].split(")")[0])

        time_diff = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        def xaxis_config (time_diff):
            if (time_diff > timedelta(days=365*2)):
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
            return xaxis_set, xaxis_label
        
        xaxis_set, xaxis_label = xaxis_config(time_diff)
        

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
                ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                ax.ticklabel_format(useOffset=False, axis='y', style='plain')
                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax.text(-0.12, 1.10, f"{selected_station}, {extend_time}", transform=ax.transAxes, va='top', ha='left', fontsize=11)
                fig.subplots_adjust(left=0.15)

                return plot_objects, fig, ax

        elif selected_data in triple_plot:
            def plot():
                fig, ax = plt.subplots(3, 1, figsize=(10,6))
                
                for i, layer_name in enumerate(data_listname):

                    line, = ax[i].plot(cut_data["datetime"], cut_data[layer_name], color=data_colors[i], linewidth=1, label=layer_name)
                    ax[i].set_title(layer_name)
                    ax[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                    ax[i].grid(True)
                    ax[i].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                    ax[i].ticklabel_format(useOffset=False, axis='y', style='plain')

                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax[0].text(-0.1, 1.5, f"{selected_station}, {extend_time}", transform=ax[0].transAxes, va='top', ha='left', fontsize=11)
                ax[0].text(-0.1, 1.2, '{:>22}'.format('[m]'), transform=ax[0].transAxes, va='top', ha='left', fontsize=10)
                ax[-1].set_xlabel(xaxis_label, font="Verdana")
                fig.subplots_adjust(left=0.01)
                fig.tight_layout()
                plot_objects = []
                return plot_objects, fig, ax

        data_listname, data_colors = match_data(selected_data)

        plot_objects, fig, ax = plot()
        data_list = plot_objects

        new_window = ctk.CTkToplevel(app)
        new_window.title("PLOT")

        center_window(new_window, 1200, 650)

        def stop():
            new_window.attributes("-topmost", False)
        
        new_window.attributes("-topmost", True)
        new_window.after(500, stop)

    
        
        right_frame = ctk.CTkFrame(new_window)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)
        


        layers_label = ctk.CTkLabel(right_frame, text="Layers", font=("Helvetica", 22))
        layers_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 50))

        layer_buttons(fig, ax, data_listname, right_frame, data_colors)

        

        if selected_station in station_list:
            station2_list = station_list.copy()
            station2_list.remove(selected_station)


        secondStation_label = ctk.CTkLabel(right_frame, text="Compare data \nwith another solution", font=("Helvetica", 16))
        secondStation_label.pack(side=ctk.TOP, fill=ctk.X, pady=(50, 20))
        
        def station2_fun(event):
            def shorten_label(text, max_length=14):
                if len(text) > max_length:
                    return text[:max_length] + "..."
                return text
            station2_menu_fullVar.set(event)
            station2_menu.set(shorten_label(event)) 

        station2_menu_fullVar = ctk.StringVar(right_frame)
        station2_menu_variable = ctk.StringVar(value="Select station ...")
        station2_menu = ctk.CTkOptionMenu(right_frame, width=150, values=[], variable=station2_menu_variable, command=station2_fun)
        station2_menu.pack(side=ctk.TOP, pady=(0, 20))
        station2_menu.configure(values=station2_list)


        
        def comparing_window_fun():
            comparing_window(
                station2_menu_fullVar,
                filepaths,
                selected_data,
                cut_data,
                cut_column,
                selected_station,
                error_label,
                start_time,
                end_time,
                station_list,
                xaxis_set,
                xaxis_label,
                app
            )

        compare_button = ctk.CTkButton(right_frame, text="Compare", command=comparing_window_fun)

        if selected_data == "DOP factors":
            compare_button.configure(state="disabled")
            
        compare_button.pack(side=ctk.TOP)

        error_label = ctk.CTkTextbox(right_frame, font=("Helvetica", 14), text_color="red", wrap="word", fg_color="transparent", cursor="arrow")
        error_label.pack(side=ctk.TOP, fill="both", pady=10)
        error_label.configure(state="disabled")

        canvas_plot = FigureCanvasTkAgg(fig, master=new_window)
        canvas_plot.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas_plot, new_window)
        toolbar.update()