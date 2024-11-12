import matplotlib.pyplot as plt
import customtkinter as ctk

def layer_buttons(fig, ax, data_listname, layers_frame, data_colors):
    def toggle_visibility(name):
        name.set_visible(not name.get_visible())
        plt.draw()

    for i, layer_name in enumerate(data_listname):
        layer_frame = ctk.CTkFrame(layers_frame)
        layer_frame.pack(anchor="w", padx=10, pady=5)
        if len(fig.get_axes()) == 1:
            toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[0], command=lambda line=ax.get_lines()[i]: toggle_visibility(line))
        else:
            toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax[i].get_lines()[0]: toggle_visibility(line))
        
        toggle_button.grid(row=0, column=0)
        toggle_button.select()
        
        # Buttons line
        buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
        buttons_line.grid(row=0, column=1, padx=(5, 5))