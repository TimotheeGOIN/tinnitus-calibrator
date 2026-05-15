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
main_frame.columnconfigure(2, weight=1)

# initialize variables
frequency: int = 440
frequency_precision: int = 100
volume: float = -20
volume_precision: float = 5

# initialize the labels for the sliders
frequency_var = ctk.StringVar(value=f"{frequency} Hz")
volume_var = ctk.StringVar(value=f"{volume} dB")


# callback functions for the sliders (keep updating their label value)
def update_frequency(frequency_callback: int) -> None:
    """
    This function is the callback for the frequency's sliders. It updates the current frequency and the frequency label.
    :param frequency_callback: Callback frequency given by a slider.
    :return: Nothing
    """
    global frequency
    # update the global frequency variable and the label
    frequency = round(frequency_callback, 0)
    frequency_var.set(f"{frequency:.0f} Hz")

def update_volume(volume_callback: float) -> None:
    """
    This function is the callback for the volume's sliders. It updates the current volume and the volume label.
    :param volume_callback: Callback volume given by a slider.
    :return: Nothing
    """
    global volume
    # update the global volume variable and the label
    volume = float(round(volume_callback, 1))
    volume_var.set(f"{volume:.1f} dB")


# callback function for each slider (keep updating the sliders)
def on_main_frequency_slider(frequency_callback: int) -> None:
    """
    This function is the callback for the main frequency slider. It updates the small slider.
    :param frequency_callback: Callback frequency given by a slider.
    :return: Nothing
    """

    # update the global frequency variable and the label
    update_frequency(frequency_callback)

    # get the new maximum and minimum values for the small slider (not going out of 20 to 10000 Hz)
    new_max_frequency = min(10_000, int(frequency_callback + frequency_precision))
    new_min_frequency = max(20, int(frequency_callback - frequency_precision))

    # update the small slider
    small_frequency_slider.configure(from_=new_min_frequency, to=new_max_frequency)
    small_frequency_slider.set(frequency)

def on_small_frequency_slider(frequency_callback: int):
    """
    This function is the callback for the small frequency slider. It updates the main slider.
    :param frequency_callback: Callback frequency given by a slider.
    :return: Nothing
    """

    # update the global frequency variable and the label
    update_frequency(frequency_callback)
    # update the main slider
    main_frequency_slider.set(frequency)


def on_main_volume_slider(volume_callback: float) -> None:
    """
    This function is the callback for the main volume slider. It updates the small slider.
    :param volume_callback: Callback volume given by a slider.
    :return: Nothing
    """

    # update the global volume variable and the label
    update_volume(volume_callback)

    # get the new maximum and minimum values for the small slider (not going out of -60 to 0 dB)
    new_max_volume = min(0.0, round(volume_callback + volume_precision, 1))
    new_min_volume = max(-60.0, round(volume_callback - volume_precision, 1))

    # update the small slider
    small_volume_slider.configure(from_=new_min_volume, to=new_max_volume)
    small_volume_slider.set(volume)

def on_small_volume_slider(volume_callback: float):
    """
    This function is the callback for the small volume slider. It updates the main slider.
    :param volume_callback: Callback volume given by a slider.
    :return: Nothing
    """

    # update the global volume variable and the label
    update_volume(volume_callback)
    # update the main slider
    main_volume_slider.set(volume)


# callback functions for the buttons
def play() -> None:
    """
    This function is a callback for the "Play" button. It plays the sound corresponding to the values on both the sliders.
    :return: Nothing
    """

    pass

def save_sound() -> None:
    """
    This function is a callback for the "Save" button. It saves the characteristics of the current sound (sliders' value)
    in a JSON file.
    :return: Nothing
    """

    pass

def load_sound() -> None:
    """"""

    pass


# frequency sliders ----------
frequency_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
frequency_frame.grid(row=0, column=0, padx=(0, 4), sticky="n")

ctk.CTkLabel(frequency_frame, text="Frequency:").pack(pady=(0, 4))
ctk.CTkLabel(frequency_frame, textvariable=frequency_var).pack(pady=(0, 8))

frequency_sliders_frame = ctk.CTkFrame(frequency_frame, fg_color="transparent")

# the main slider
main_frequency_slider = ctk.CTkSlider(frequency_sliders_frame, from_=20, to=10000, number_of_steps=9980,
                                      height=240, width=16, orientation="vertical", command=on_main_frequency_slider)
main_frequency_slider.set(frequency)


# the small slider
small_frequency_slider = ctk.CTkSlider(frequency_sliders_frame, from_=int(frequency-frequency_precision), to=int(frequency+frequency_precision),
                                       orientation="vertical", number_of_steps=int(frequency_precision*2),
                                       height=200, width=14, command=on_small_frequency_slider)
small_frequency_slider.set(frequency)

# pack and place the components
frequency_sliders_frame.pack()
main_frequency_slider.pack(side="left", padx=6)
small_frequency_slider.pack(side="left", padx=6, pady=(30, 0))


# volume sliders ----------
volume_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
volume_frame.grid(row=0, column=1, padx=(16, 0), sticky="n")

ctk.CTkLabel(volume_frame, text="Volume:").pack(pady=(0, 4))
ctk.CTkLabel(volume_frame, textvariable=volume_var).pack(pady=(0, 8))

volume_sliders_frame = ctk.CTkFrame(volume_frame, fg_color="transparent")

# the main slider
main_volume_slider = ctk.CTkSlider(volume_sliders_frame, from_=-60, to=0, number_of_steps=60,
                                      height=240, width=16, orientation="vertical", command=on_main_volume_slider)
main_volume_slider.set(volume)


# the small slider
small_volume_slider = ctk.CTkSlider(volume_sliders_frame, from_=int(volume-volume_precision), to=int(volume+volume_precision),
                                       orientation="vertical", number_of_steps=int(volume_precision*4),
                                       height=200, width=14, command=on_small_volume_slider)
small_volume_slider.set(volume)

# pack and place the components
volume_sliders_frame.pack()
main_volume_slider.pack(side="left", padx=6)
small_volume_slider.pack(side="left", padx=6, pady=(40, 0))


# buttons ----------
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.grid(row=0, column=3, sticky="e")

ctk.CTkButton(btn_frame, text="Play", command=play,
              width=200, height=50, fg_color="#8B1A2A", hover_color="#A52535", text_color="white").pack(pady=15)
ctk.CTkButton(btn_frame, text="Save", command=save_sound,
              width=200, height=50, fg_color="#8B1A2A", hover_color="#A52535", text_color="white").pack(pady=15)
ctk.CTkButton(btn_frame, text="Load", command=load_sound,
              width=200, height=50, fg_color="#8B1A2A", hover_color="#A52535", text_color="white").pack(pady=15)


# start the app
app.mainloop()














