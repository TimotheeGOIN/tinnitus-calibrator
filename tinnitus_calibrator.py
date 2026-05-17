
import json

import customtkinter as ctk
import numpy as np
import sounddevice as sd

from tkinter import filedialog


# appearance settings for the window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Tinnitus Calibrator")
app.geometry("640x400")

# the main frame containing all the elements in the window
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(expand=True, fill="both", padx=30, pady=30)
main_frame.columnconfigure(2, weight=1)


# the magic word (to recognize the JSON file)
magicword = "the song bird"

# initialize variables
is_playing: bool = False
is_calibrated: bool = False
calibration_volume: float = 0.0

samplerate: int = 44100
phase: int = 0
frequency: int = 440
volume: float = -20

frequency_precision: int = 100
volume_precision: float = 5

# initialize the variables from the JSON file
fromjson_frequency: int = None
fromjson_volume: float = None
fromjson_relative_volume: float = None

# initialize the labels for the sliders
frequency_var = ctk.StringVar(value=f"{frequency} Hz")
volume_var = ctk.StringVar(value=f"{volume} dB")


# UI function (reload button, updating sliders...)
def is_same_as_from_json() -> None:
    """
    This function is purely for aesthetic purposes. It checks if the current sound characteristics are the same as the
    ones from the last loaded JSON file. If yes, it updates the "Reload from JSON" button to be marked as the user knows
    the current sound characteristics are the same as the ones from the last loaded JSON file.
    :return: Nothing
    """
    global frequency, volume, fromjson_frequency, fromjson_relative_volume

    # if current sound characs are the same as the ones from the last loaded sound
    if frequency == fromjson_frequency and (volume - calibration_volume) == fromjson_relative_volume:
        reload_btn.configure(state="disabled", fg_color="#8B1A2A")

    # if different, BUT the values from the JSON aren't both None (default): a sound has already been loaded, but current characs doesn't match it
    elif (fromjson_volume is not None) or (fromjson_relative_volume is not None):
        reload_btn.configure(state="normal", fg_color="#3e6182")

    else: # if the values from the JSON are both None (default): no sound has been loaded yet
        reload_btn.configure(state="disabled", fg_color="#3e6182")


def updating_frequency_sliders() -> None:
    """
    This function only updates the frequency sliders position according to the current global frequency variable.
    :return: Nothing
    """

    # update the main slider
    main_frequency_slider.set(frequency)

    # get the new maximum and minimum values for the small slider (not going out of 20 to 10000 Hz)
    new_max_frequency = min(10_000, int(frequency + frequency_precision))
    new_min_frequency = max(20, int(frequency - frequency_precision))

    # update the small slider
    small_frequency_slider.configure(from_=new_min_frequency, to=new_max_frequency)
    small_frequency_slider.set(frequency)

def updating_volume_sliders() -> None:
    """
    This function only updates the volume sliders position according to the current global volume variable.
    :return: Nothing
    """

    # update the main slider
    main_volume_slider.set(volume)

    # get the new maximum and minimum values for the small slider (not going out of -60 to 20 dB)
    new_max_volume = min(0.0, round(volume + volume_precision, 1))
    new_min_volume = max(-60.0, round(volume - volume_precision, 1))

    # update the small slider
    small_volume_slider.configure(from_=new_min_volume, to=new_max_volume)
    small_volume_slider.set(volume)

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

    # update the reload button
    is_same_as_from_json()

def update_volume(volume_callback: float) -> None:
    """
    This function is the callback for the volume's sliders. It updates the current volume and the volume label.
    :param volume_callback: Callback volume given by a slider.
    :return: Nothing
    """
    global volume
    # update the global volume variable and the label
    volume = min(0.0, float(round(volume_callback, 1)))
    volume_var.set(f"{volume:.1f} dB")

    # update the reload button
    is_same_as_from_json()


# callback function for each slider (keep updating the sliders)
def on_main_frequency_slider(frequency_callback: int) -> None:
    """
    This function is the callback for the main frequency slider. It updates the small slider.
    :param frequency_callback: Callback frequency given by a slider.
    :return: Nothing
    """

    # update the global frequency variable and the label
    update_frequency(frequency_callback)

    # update the sliders
    updating_frequency_sliders()

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

    # update the sliders
    updating_volume_sliders()

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


# audio manipulation function
def callback(outdata, frames, time, status) -> None:
    global phase

    # create the current block
    block = (phase + np.arange(frames)) / samplerate
    # create the sine wave with the current frequency and volume
    wave = (10**(volume/20)) * np.sin(2 * np.pi * frequency * block)

    outdata[:, 0] = wave # left channel
    outdata[:, 1] = wave # right channel

    # update the phase
    phase = (phase + frames) % samplerate


# callback functions for the buttons
def play_sound() -> None:
    """
    This function is a callback for the "Play" button. It enables or disables the audio stream depending on the current state.
    :return: Nothing
    """
    global is_playing

    if is_playing:
        # stop the audio stream
        is_playing = False
        stream.stop()
        # update the play button and enable the other buttons
        play_btn.configure(text="Play", fg_color="#4b9e3c", hover_color="#3a822e")
        calibrate_btn.configure(state="normal")
        save_btn.configure(state="normal")
        load_btn.configure(state="normal")
        reload_btn.configure(state="normal")

    else:
        # start the audio stream
        is_playing = True
        stream.start()
        # update the play button and disable the other buttons
        play_btn.configure(text="Pause", fg_color="#8B1A2A", hover_color="#A52535", text_color="white")
        calibrate_btn.configure(state="disabled")
        save_btn.configure(state="disabled")
        load_btn.configure(state="disabled")
        reload_btn.configure(state="disabled")


def calibrate_volume() -> None:
    """
    This function is a callback for the "Calibrate" button. It calibrates the volume to be adapted to the hearing of the user.
    This function has to be called at least once before using the saving and loading function.
    :return: Nothing
    """
    global is_calibrated, calibration_volume

    is_calibrated = True
    calibration_volume = volume

    # change the calibration button color to indicate the sound has been calibrated at least once
    calibrate_btn.configure(state="enabled", fg_color="#3e6182", hover_color="#304d69", text=f"Calibrated {calibration_volume:.1f} dB")

    # enable the saving and loading buttons
    save_btn.configure(state="normal")
    load_btn.configure(state="normal")


def save_sound() -> None:
    """
    This function is a callback for the "Save" button. It saves the characteristics of the current sound (sliders' value)
    in a JSON file.
    :return: Nothing
    """

    # get the current values of the sound characteristics
    sound_data = {
        "magicword": magicword,
        "frequency": frequency,
        "volume": volume,
        "calibration_volume": calibration_volume,
    }

    # ask the user the path where to save the JSON
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    # save the sound characteristics in a JSON file
    with open(file_path, "w") as file:
        file.write(json.dumps(sound_data, indent=4))


def load_sound_from_json() -> None:
    """
    This function is a callback for the "Load from JSON" button. It loads the characteristics of a sound from a JSON file.
    :return: Nothing
    """
    global fromjson_frequency, fromjson_volume, fromjson_relative_volume

    # ask the user the path where to find the JSON file
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    # extract the sound characteristics from the JSON file
    with open(file_path, "r") as file:
        sound_data = json.load(file)

    # ensure the JSON is compatible by checking the magicword
    try:
        if sound_data["magicword"] != magicword:
            raise ValueError("The JSON file is not compatible with this program.")
    except KeyError:
        raise ValueError("The JSON file is not compatible with this program.")

    fromjson_frequency = sound_data["frequency"]
    fromjson_volume = sound_data["volume"]
    fromjson_relative_volume = sound_data["volume"] - sound_data["calibration_volume"]

    # update the sound characteristics variables
    update_frequency(fromjson_frequency)
    update_volume(calibration_volume + fromjson_relative_volume)

    # update all the sliders
    updating_frequency_sliders()
    updating_volume_sliders()


def reload_sound_from_json() -> None:
    """
    This function is a callback for the "Reload from JSON" button. It reloads the characteristics of a sound
    from the last loaded JSON file.
    :return: Nothing
    """
    global frequency, volume

    # replace the current global variables with the ones from the last loaded JSON file
    update_frequency(fromjson_frequency)
    update_volume(calibration_volume + fromjson_relative_volume)

    # update the sliders
    updating_frequency_sliders()
    updating_volume_sliders()


# frequency sliders ---------------
frequency_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
frequency_frame.grid(row=0, column=0, padx=(0, 4), sticky="n")

ctk.CTkLabel(frequency_frame, text="Frequency", font=ctk.CTkFont(size=20)).pack(pady=(0, 4), padx=(20, 0))
ctk.CTkLabel(frequency_frame, textvariable=frequency_var).pack(pady=(0, 8), padx=(20, 0))

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
frequency_sliders_frame.pack(padx=(20, 0))
main_frequency_slider.pack(side="left", padx=10)
small_frequency_slider.pack(side="left", padx=10, pady=(40, 0))


# volume sliders ---------------
volume_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
volume_frame.grid(row=0, column=1, padx=(16, 0), sticky="n")

ctk.CTkLabel(volume_frame, text="Volume", font=ctk.CTkFont(size=20)).pack(pady=(0, 4), padx=(40, 0))
ctk.CTkLabel(volume_frame, textvariable=volume_var).pack(pady=(0, 8), padx=(40, 0))

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
volume_sliders_frame.pack(padx=(40, 0))
main_volume_slider.pack(side="left", padx=10)
small_volume_slider.pack(side="left", padx=10, pady=(40, 0))


# buttons ---------------
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.grid(row=0, column=3, sticky="e")


calibrate_btn = ctk.CTkButton(btn_frame, text="Calibrate", command=calibrate_volume,
                              width=240, height=70, fg_color="#8B1A2A", hover_color="#A52535", text_color="white")
play_btn      = ctk.CTkButton(btn_frame, text="Play", command=play_sound,
                              width=240, height=70, fg_color="#4b9e3c", hover_color="#3a822e", text_color="white")
save_btn      = ctk.CTkButton(btn_frame, text="Save", command=save_sound, state="disabled",
                              width=240, height=30, fg_color="#3e6182", hover_color="#304d69", text_color="white")
load_btn      = ctk.CTkButton(btn_frame, text="Load from JSON", command=load_sound_from_json, state="disabled",
                              width=110, height=30, fg_color="#3e6182", hover_color="#304d69", text_color="white")
reload_btn    = ctk.CTkButton(btn_frame, text="Reload from JSON", command=reload_sound_from_json, state="disabled",
                              width=110, height=30, fg_color="#3e6182", hover_color="#304d69", text_color="white")


calibrate_btn.pack(padx=(0, 20), pady=15)
play_btn.pack(padx=(0, 20), pady=15)
save_btn.pack(padx=(0, 20), pady=15)
load_btn.pack(pady=15, side="left")
reload_btn.pack(padx=(13, 0), pady=15, side="left")

# initialize the audio stream
stream = sd.OutputStream(samplerate=samplerate, channels=2, callback=callback)

# start the app
app.mainloop()






