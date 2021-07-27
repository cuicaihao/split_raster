import PySimpleGUI as sg                        # Part 1 - The import

# Define the window's contents

default_input_image_path = "../data/raw/RGB.png"
default_output_folder_path = "../data/processed/RGB"


def TextLabel(text): return sg.Text(
    text+':', justification='r', size=(32, 1))


layout = [

    # Part 2 - The Layout
    [TextLabel('Path to input image'), sg.Input(
        default_input_image_path, size=(32, 10), key='input'), sg.FileBrowse()],

    [TextLabel('Path to output folder'), sg.Input(
        default_output_folder_path, size=(32, 10), key='output'), sg.FolderBrowse()],

    [TextLabel('Crop Size'), sg.Combo(
        [100, 200, 400], size=(32, 10), default_value=100, key='crop_size')],

    [TextLabel('repetition_rate'), sg.Slider(range=(0, 100), orientation='h', size=(
        32, 1), default_value=0.0, key='repetition_rate')],

    [sg.Output(size=(70, 20), key='-OUTPUT-')],
    [sg.Button('Run'), sg.Button('Clear'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Split Raster', layout)      # Part 3 - Window Defintion

# Display and interact with the Window
# Part 4 - Event loop or Window.read call
# Do something with the information gathered
counter = 0
while True:             # Event Loop
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Run':
        print(counter, event, values)
        counter += 1
    if event == 'Clear':
        values["input"] = ""
        values["output"] = ""
        window['-OUTPUT-'].update('')
        counter = 0


# Finish up by removing from the screen
window.close()
