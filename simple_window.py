import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import matplotlib.pyplot as plt

import compress


# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------


def plot_times(compress_types, file_to_compress):    
    elapsed_times = compress.compress(file_to_compress, compress_types)
    if elapsed_times != None:
        plt.bar(compress_types,elapsed_times)
        
        plt.ylabel('time in seconds')
        plt.title('Compression times with different algorithms') 
        fig = plt.gcf()
        return fig
    else:
        return None
    
# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------


#  The magic function that makes it possible.... glues together tkinter and pyplot using Canvas Widget
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')



# ------------------------------- Beginning of GUI CODE -------------------------------
sg.theme('Dark Blue 3')


figure_x, figure_y, figure_w, figure_h = (0,0,640,480)

# define the window layout

layout = [[sg.Text('Compression algorithms benchmark', font='Any 18')],
          [sg.Text('File to compress:',  justification='right'),
             sg.InputText('linia.jpg',key='_FILE_IN_'), sg.FilesBrowse()],
          [sg.Checkbox('gzip', default=True, key='gzip'),
           sg.Checkbox('bzip2', key='bzip2'),
           sg.Checkbox('lzma', key='lzma', size=(10,1)), sg.Button('Compress')],
          [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
          ]


# create the form and show it without the plot
window = sg.Window('Compression algorithms benchmark',
    layout, force_toplevel=True, finalize=True)


figure_agg = None
# show it all again and get buttons
while True:  # Event Loop
    event, values = window.read()       # can also be written as event, values = window()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Compress':
        checkboxes = ['gzip','bzip2', 'lzma']
        compress_types = []
        for checkbox in checkboxes:
            if values[checkbox]:
                compress_types.append(checkbox)     

        if figure_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(figure_agg)
        file_to_compress = values['_FILE_IN_']
        if compress_types and file_to_compress != '':
            fig = plot_times(compress_types, file_to_compress)
            if fig != None:
                figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    

window.close()
