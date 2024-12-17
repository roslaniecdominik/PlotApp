import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import re
                
from datetime import datetime, timedelta
from tkinter import messagebox
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D

from components.dataConfiguration import match_data_after, defining_data, data_filtering, triple_plot_corrections
from components.centerWindow import center_window
from components.layerButtons import layer_buttons
from components.axisLabel import xaxis_config, yaxis_label
from components.sliderEvent import plot_updater_slider
from comparingPlotCreator import comparing_window

data_dict, single_scatter, single_plot, triple_plot = defining_data()

def create_plot(start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, filepaths, station_list, selected_station, data, selected_datas, app, stat_list):
    global loading_check

    start_time = f"{start_year_entry.get()} {start_hour_entry.get()}"
    end_time = f"{end_year_entry.get()} {end_hour_entry.get()}"

    if start_time > end_time:
        messagebox.showinfo("Message", "Starting time must be less than end time")

    else:
        data_listnames, data_colors = match_data_after(selected_datas)
        data, data_listnames, data_colors = data_filtering(data, data_listnames, data_colors)
        time_data = data.loc[(data['datetime'] >= start_time) & (data['datetime'] <= end_time)]
        cut_data = time_data.reset_index(drop=True)
        time_diff = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        xaxis_set, xaxis_label = xaxis_config(time_diff, timedelta)    
        start_index = 0


        def plot(data_listnames, data_colors, selected_datas):
            if len([item for item in selected_datas if selected_datas.count(item) > 1]) > 0:
                selected_datas = list(set(selected_datas))
            common = [el for el in selected_datas if el in triple_plot]
            const = 2 * len(common)

            fig, axs = plt.subplots((len(selected_datas) + const), 1, figsize=(10,10))
            lines = []
            scatters_test = []
            invisible_lines = []
            if len(selected_datas) == 1:
                if selected_datas in single_plot:
                    axs = [axs]
            if selected_datas.count(selected_datas[0]) < 2:
                data_listnames, data_colors, selected_datas = triple_plot_corrections(data_listnames, data_colors, selected_datas, triple_plot)


            axs = [axs] if not isinstance(axs, np.ndarray) else axs
            i = 0

            for data_listname, data_color, ax in zip(data_listnames, data_colors, axs):
                legend_elements = []
                if selected_datas[i] in single_plot or selected_datas[i] in triple_plot:
                    for layer_name, color in zip(data_listname, data_color):
                        line, = ax.plot(cut_data["datetime"], cut_data[layer_name], color=color, linewidth=1, zorder=2)
                        lines.append(line,)
                        legend_elements.append(Line2D([0], [0], color=color, lw=2, label=layer_name))
                        # ax.set_ylim(cut_data[layer_name].min(), (cut_data[layer_name].max())*1.3)
                elif selected_datas[i] in single_scatter:
                    
                    shapes_data = ["Bad IFree", "No Clock", "No Orbit", "Cycle Slips", "Outliers", "Eclipsing"]
                    shapes = ["s", "x", "+", "^", "o", "D"]
                    
                    for layer_name, color in zip(data_listname, data_color):
                     
                        if layer_name == data_listname[0]:
                            invisible_data = [0 for _ in range(cut_data[start_index:].shape[0])]
                            invisible_data[0] = cut_data[[col for col in cut_data.columns if col.startswith(layer_name[:2])]].min().min()
                            invisible_data[-1] = cut_data[[col for col in cut_data.columns if col.startswith(layer_name[:2])]].max().max()
                        if layer_name in shapes_data:
                            index = shapes_data.index(layer_name)
                            scatter = ax.scatter(cut_data["datetime"], cut_data[layer_name], color=color, s=20, zorder=3, marker=shapes[index])
                            lines.append(scatter)
                            legend_elements.append(Line2D([0], [0], marker=shapes[index], color="white", markerfacecolor=color, markersize=10, label=layer_name))
                            
                        else:
                            std = cut_data[layer_name] - cut_data[layer_name].mean()
                            scatter = ax.scatter(cut_data["datetime"], cut_data[layer_name], color=color, s=1, zorder=2)
                            lines.append(scatter)
                            if "PRN_" in layer_name:
                                legend_elements.append(Line2D([0], [0], color=color, lw=2, label=layer_name))
                            else:
                                legend_elements.append(Line2D([0], [0], marker="o", color="white", markerfacecolor=color, markersize=7, label=layer_name))
                    
                    invisible_line, = ax.plot(cut_data["datetime"], invisible_data, color='none')
                    invisible_lines.append(invisible_line)
                
                t = ax.text(0.02, 0.99, stat_list[i], fontsize=7, color='black', ha='left', va='bottom', transform=ax.transAxes)
                t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='white', pad=0.2, boxstyle="round"))
                
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_elements)
                ax.grid(True, zorder=1)
                ax.xaxis.set_tick_params(labelbottom=False)
                ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                ax.ticklabel_format(useOffset=False, axis='y', style='plain')
                ax.set_ylabel(yaxis_label(selected_datas[i]))
                ax.set_xlim(cut_data["datetime"].min() - 0.01*(cut_data["datetime"].max() - cut_data["datetime"].min()), 
                            cut_data["datetime"].max() + 0.01*(cut_data["datetime"].max() - cut_data["datetime"].min()))
                
                if "RecX" in selected_datas or "RecN" in selected_datas:
                    ax.yaxis.set_label_coords(-0.09, 0.5)
                else:
                    ax.yaxis.set_label_coords(-0.06, 0.5)
                i += 1
            axs[-1].xaxis.set_tick_params(labelbottom=True)
            axs[-1].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
            
            extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"

            station_range_text = fig.suptitle(f"{selected_station}, {extend_time}", fontsize=11, color='black', y=0.95)
            fig.subplots_adjust(left=0.1, right=0.88)

            try:
                invisible_lines
            except:
                invisible_lines = []
            return fig, axs, lines, station_range_text, scatters_test, invisible_lines, data_listnames, data_colors, selected_datas
        
        fig, axs, lines, station_range_text, scatters, invisible_lines, data_listnames, data_colors, selected_datas = plot(data_listnames, data_colors, selected_datas)
        
        new_window = ctk.CTkToplevel(app)
        new_window.title("PLOT")

        center_window(new_window, 1350, 740)

        def stop():
            new_window.attributes("-topmost", False)
        
        new_window.attributes("-topmost", True)
        new_window.after(500, stop)

        canvas_frame = ctk.CTkFrame(new_window, corner_radius=0)
        canvas_plot = FigureCanvasTkAgg(fig, master=canvas_frame)
        

        toolbar_slider_frame = ctk.CTkFrame(new_window, fg_color="#F0F0F0", corner_radius=0)
        toolbar_slider_frame.pack(side=ctk.BOTTOM, fill=ctk.X)

        toolbar = NavigationToolbar2Tk(canvas_plot, toolbar_slider_frame)
        toolbar.update()
        toolbar.pack(side=ctk.LEFT)
        toolbar._message_label.config(width=22)

        def data_entry_event(event):
            if (cut_data['datetime'] == data_entry.get()).any():
                value = cut_data[cut_data['datetime'] == data_entry.get()].index[0]
                data_slider.set(value)
                plot_updater_slider(value, lines, axs, data_listnames, canvas_plot, cut_data, station_range_text, selected_station, "", invisible_lines, single_scatter, selected_datas, "", data_entry)
            else:
                label = data_entry.get()
                data_entry.delete(0, ctk.END)
                default_color = data_entry.cget("text_color")
                data_entry.configure(text_color="red")
                data_entry.insert(0, "value out of range")
                
                def update_entry():
                    data_entry.delete(0, ctk.END)
                    data_entry.configure(text_color=default_color)
                    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
                    matches = re.findall(pattern, str(station_range_text))
                    data_entry.insert(0, matches[0])
                data_entry.after(2000, update_entry)
                
        
        data_entry = ctk.CTkEntry(toolbar_slider_frame, width=198, justify="center")
        data_entry.pack(side=ctk.RIGHT, padx=(0,2))
        data_entry.insert(0, cut_data.loc[start_index, "datetime"])
        data_entry.bind("<Return>", data_entry_event)

        data_slider = ctk.CTkSlider(toolbar_slider_frame, from_=0, to=cut_data.shape[0]-1, number_of_steps=cut_data.shape[0]-1, width=500, height=20, command=lambda value: plot_updater_slider(value, lines, axs, data_listnames, canvas_plot, cut_data, station_range_text, selected_station, "", invisible_lines, single_scatter, selected_datas, "", data_entry))
        data_slider.set(start_index)
        data_slider.pack(side=ctk.RIGHT, expand=True, padx=5)
        
        if any(item in single_scatter for item in selected_datas):
            data_slider.configure(state="disabled")


        right_frame = ctk.CTkFrame(new_window)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)
        

        canvas_frame.pack(side=ctk.TOP, fill="both", expand=True)
        canvas_plot.get_tk_widget().pack(fill=ctk.BOTH, expand=True)


        layers_label = ctk.CTkLabel(right_frame, text="Layers", font=("Helvetica", 22))
        layers_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 10))

        if sum(len(sublist) for sublist in data_listnames) > 19:
            scrollable_frame = ctk.CTkScrollableFrame(right_frame)
            scrollable_frame.pack(padx=5, pady=(0,5), fill="both", expand=True)
            layer_buttons(fig, axs, data_listnames, scrollable_frame, data_colors)
        else:
            layer_buttons(fig, axs, data_listnames, right_frame, data_colors)

        if selected_datas == ['RecX', 'RecY', 'RecZ'] or selected_datas == ['RecN', 'RecE', 'RecU']:
            if selected_station in station_list:
                secondStation_list = station_list.copy()
                secondStation_list.remove(selected_station)
                secondStation_list = [item for item in secondStation_list if item.split(" ")[0] == (selected_station.split(" ")[0])]


            secondStation_label = ctk.CTkLabel(right_frame, text="Compare data \nwith another solution", font=("Helvetica", 16))
            secondStation_label.pack(side=ctk.TOP, fill=ctk.X, pady=(30, 20))
            
            def shorten_label(event):
                def shorten_label(text, max_length=14):
                    if len(text) > max_length:
                        return text[:max_length] + "..."
                    return text
                secondStation_menu_fullVar.set(event)
                secondStation_menu.set(shorten_label(event)) 

            secondStation_menu_fullVar = ctk.StringVar(right_frame)
            secondStation_menu_variable = ctk.StringVar(value="Select solution ...")
            secondStation_menu = ctk.CTkOptionMenu(right_frame, width=150, values=[], variable=secondStation_menu_variable, command=shorten_label)
            secondStation_menu.pack(side=ctk.TOP, pady=(0, 20))
            secondStation_menu.configure(values=secondStation_list)

            
            def comparing_window_fun():
                comparing_window(
                    secondStation_menu_fullVar,
                    filepaths,
                    selected_datas,
                    cut_data,
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

            if selected_datas in single_plot:
                compare_button.configure(state="disabled")
                
            compare_button.pack(side=ctk.TOP)

            error_label = ctk.CTkTextbox(right_frame, font=("Helvetica", 14), text_color="red", wrap="word", fg_color="transparent", cursor="arrow")
            error_label.pack(side=ctk.TOP, fill="both", pady=10)
            error_label.configure(state="disabled")        