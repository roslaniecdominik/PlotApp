import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def minmax_frame(text, MinMax_section): #to
    section = ctk.CTkFrame(MinMax_section, fg_color="transparent")
    section.pack(side=ctk.LEFT, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(section, text=text, font=("Helvetica", 13), text_color="grey")
    label.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    label_value = ctk.CTkLabel(section, text="", font=("Helvetica", 15))
    label_value.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    return label, label_value

def sliders_frame(tab_text, date_text, tabview): #to
    frame = ctk.CTkFrame(tabview.tab(tab_text))
    frame.pack(side=ctk.TOP, pady=5)
    label = ctk.CTkLabel(frame, text=date_text)
    label.pack(side=ctk.LEFT, pady=5)
    entry = ctk.CTkEntry(frame, placeholder_text="", font=("Helvetica", 15), justify="center", border_width=0)
    entry.pack(side=ctk.LEFT, padx=10)
    return entry

def selected_time (parent, text):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(side=ctk.TOP, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 12), text_color="grey")
    label.pack(side=ctk.LEFT, fill=ctk.X, padx=(20,0))
    
    label_date = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_date.pack(side=ctk.LEFT, fill=ctk.X, padx=(15,0))
    
    label_time = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_time.pack(side=ctk.RIGHT, fill=ctk.X, padx=(15,0))
    return label_date, label_time

def plot_frames(fig, plot_frame, layers_frame, cut_data, lines, axs, data_listname, station_range_text, selected_station, selected_secondStation_solution, cord_time, cord1, cord2, sol_df, layer_name):
    from components.sliderEvent import plot_updater_slider
    start_index = 0
    canvas_plot = FigureCanvasTkAgg(fig, plot_frame)
    canvas_plot.draw()
    widget = canvas_plot.get_tk_widget()
    widget.pack(side="top", fill=ctk.BOTH, expand=True)
    
    toolbar_slider_frame = ctk.CTkFrame(plot_frame, fg_color="#F0F0F0", corner_radius=0)
    toolbar_slider_frame.pack(side=ctk.BOTTOM, fill=ctk.X)
    
    toolbar = NavigationToolbar2Tk(canvas_plot, toolbar_slider_frame)
    toolbar.update()
    toolbar.pack(side="left")
    toolbar._message_label.config(width=22)
    
    data_slider = ctk.CTkSlider(toolbar_slider_frame, from_=0, to=cord1.shape[0]-1, number_of_steps=cord1.shape[0]-1, width=700, height=20, command=lambda value: plot_updater_slider(value, lines, axs, data_listname, canvas_plot, cut_data, station_range_text, selected_station, selected_secondStation_solution, cord_time, cord1, cord2, sol_df, layer_name))
    data_slider.set(start_index)
    data_slider.pack(side="right", expand=True, padx=5)

    layers_frame_on = ctk.CTkFrame(layers_frame)
    layers_frame_on.pack(side="bottom", fill=ctk.X)
    layers_label = ctk.CTkLabel(layers_frame_on, text="Layers", font=("Helvetica", 22))
    layers_label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 10))

    return layers_frame_on, widget, toolbar_slider_frame