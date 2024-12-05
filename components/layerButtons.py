import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
import customtkinter as ctk
import numpy as np

def layer_buttons(fig, axs, data_listnames, layers_frame, data_colors):
    def toggle_visibility(name):
        name.set_visible(not name.get_visible())
        plt.draw()
    for data_listname, data_color, ax in zip(data_listnames, data_colors, axs):
        for i, layer_name in enumerate(data_listname):
            
            if type(ax) != np.ndarray and any(isinstance(coll, PathCollection) for coll in ax.collections):
                
                if any(i in data_listname[0] for i in ["GPS", "GLONASS", "GALILEO", "BeiDou", "IRNSS", "SBAS"]): #ground track

                    layer_label = ctk.CTkLabel(layers_frame, text=data_listname[i])
                    layer_label.pack(side=ctk.TOP, padx=10, pady=(10,2))

                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(side=ctk.TOP, pady=5, padx=15)
                    
                    toggle_button = ctk.CTkCheckBox(layer_frame, text="", width=50, command=lambda line=ax.collections[i]: toggle_visibility(line))
                
                else: #phase
                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(fill=ctk.X, side=ctk.TOP, pady=5, padx=15)
                    toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], width=50, command=lambda line=ax.collections[i]: toggle_visibility(line))

            elif len(fig.get_axes()) == 1: #liniowe pojedyńcze
                layer_frame = ctk.CTkFrame(layers_frame)
                layer_frame.pack(fill=ctk.X, side=ctk.TOP, pady=5, padx=15)
                toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax.get_lines()[i]: toggle_visibility(line))

            else: #liniowe macierzowe 
                layer_frame = ctk.CTkFrame(layers_frame)
                layer_frame.pack(fill=ctk.X, side=ctk.TOP, pady=5, padx=15)
                toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax.get_lines()[i]: toggle_visibility(line))
            
            # toggle_button.grid(row=0, column=0)
            toggle_button.pack(side=ctk.LEFT)
            toggle_button.select()
            
            # Buttons line
            buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_color[i])
            buttons_line.pack(side=ctk.RIGHT, padx=(0,10))