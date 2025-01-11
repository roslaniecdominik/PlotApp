def center_window(window=None, width=None, height=None, info=None):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    scale_factor = window._get_window_scaling()

    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/2))*0.9)
    if info:
        x = int(((screen_width/2) + 370) * scale_factor)
        y = int(((screen_height/2) - (250))*0.9)

    window.geometry(f"{width}x{height}+{x}+{y}")