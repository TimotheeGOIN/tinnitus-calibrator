import customtkinter as ctk
import numpy as np
import sounddevice as sd


# appearance settings for the window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Tinnitus Calibrator")
app.geometry("600x420")

# the main frame containing all the elements in the window
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(expand=True, fill="both", padx=30, pady=30)
main_frame.columnconfigure(4, weight=1)

# initialize the labels for the sliders
frequence_var = ctk.StringVar(value="440 Hz")
volume_var = ctk.StringVar(value="-20 dB")

# callback functions for the sliders (keep updating their label value)
def update_frequence():
    pass