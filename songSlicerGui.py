# GUI for songslicer
# Run the program with 'python songSlicerGui.py'

import tkinter as tk
from tkinter.filedialog import askopenfilename
from songSlicerClasses import *

def run(*args):
    if check_input():
        status.set("Opening {}".format(filename.get()))
        inputSongFile = songFile(filename.get())
        inputBeat = beatParameters(beat.get(),beat_units.get())
        slicer = songSlicer(inputSongFile)
        if start_trim.get() > 0:
            slicer.trim("start", start_trim.get())
        if end_trim.get() > 0:
            slicer.trim("end", end_trim.get())
        slicer.slice(inputBeat)
        slicer.export("even")
        slicer.export("odd")
        status.set("Done")

def check_input():
    # Check file exists
    if not os.path.isfile(filename.get()):
        status.set("Error: file \"{}\" not found".format(filename.get()))
        return False
    
    # Check beat length, front/end trim are non-negative integer
    if not isinstance(beat.get(), int) or beat.get() <= 0:
        status.set("Error: Beat Length {} must be a positive non-zero integer".format(beat.get()))
        return False
    if not isinstance(start_trim.get(), int) or start_trim.get() < 0:
        status.set("Error: Start Trim {} must be a positive integer".format(start_trim.get()))
        return False
    if not isinstance(end_trim.get(), int) or end_trim.get() < 0:
        status.set("Error: End Trim {} must be a positive integer".format(end_trim.get()))
        return False
    
    return True

def file_select():
    file_search_return = askopenfilename(
        filetypes=[
            ("mp3 files", ".mp3")
        ]
    )
    filename.set(file_search_return)

# Add ffmpeg to PATH
initialize_ffmpeg_path()

root=tk.Tk()
root.title("SongSlicer")

mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0)
background_colour = "#33C5FF"
element_colour = "#7DB6EC"
mainframe.configure(bg=background_colour)
root.configure(bg=background_colour)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# File select
ROW=1
filename = tk.StringVar()
filename.set("Select a file...")
file_entry_span = 4
file_entry = tk.Entry(mainframe, width=70, textvariable=filename)
file_entry.grid(column=1, row=ROW, columnspan=file_entry_span)
file_select_button = tk.Button(mainframe, text="Open", command=file_select)
file_select_button.grid(column=file_entry_span+1, row=ROW)
file_select_button["bg"]=element_colour

# Start/End trim
ROW+=1
trim_label = tk.Label(mainframe, text="Optional: Trim from start/end.")
trim_label.grid(column=1, row=ROW)
trim_label["bg"]=background_colour
start_trim_label = tk.Label(mainframe, text="Start Trim (ms):")
start_trim_label.grid(column=2, row=ROW)
start_trim_label["bg"]=background_colour
start_trim = tk.IntVar()
start_trim.set(0)
start_trim_entry = tk.Entry(mainframe, width=7, textvariable=start_trim)
start_trim_entry.grid(column=3, row=ROW)
end_trim_label = tk.Label(mainframe, text="End Trim (ms):")
end_trim_label.grid(column=4, row=ROW)
end_trim_label["bg"]=background_colour
end_trim = tk.IntVar()
end_trim.set(0)
end_trim_entry = tk.Entry(mainframe, width=7, textvariable=end_trim)
end_trim_entry.grid(column=5, row=ROW)

# Beat entry
ROW+=1
beat = tk.IntVar()
beat_length_label = tk.Label(mainframe, text="Enter beat length...")
beat_length_label.grid(column=1, row=ROW)
beat_length_label["bg"]=background_colour
beat_entry = tk.Entry(mainframe, width=7, textvariable=beat)
beat_entry.grid(column=2, row=ROW)
beat_units = tk.StringVar()
OPTIONS = ["bpm", "milliseconds"]
beat_units.set(OPTIONS[0])
beat_unit_options = tk.OptionMenu(mainframe, beat_units, *OPTIONS)
beat_unit_options.grid(column=3, row=ROW)
beat_unit_options["bg"]=element_colour
beat_unit_options["activebackground"]=element_colour
beat_unit_options["menu"]["bg"]=element_colour
beat_unit_options["highlightthickness"]=0

# Run button
ROW+=1
run_button = tk.Button(mainframe, text="Slice", command=run, width=20)
run_button.grid(column=1, row=ROW, columnspan=2)
run_button["bg"]=element_colour

# Status text
ROW+=1
status_header = tk.Label(mainframe, text="Status")
status_header.grid(column=1, row=ROW)
status_header["bg"]=background_colour
status = tk.StringVar()
status.set("Ready...")
status_label = tk.Label(mainframe, textvariable=status)
status_label.grid(column=2, row=ROW)
status_label["bg"]=background_colour

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind("<Return>", run)
file_entry.focus()

root.mainloop()


