# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:25:17 2020

@author: Clay

Create tabs for axes, with basic axes setting not dependent on the graph
    -size axis labels
    -legend labels??
    -shared x/y axis?    
    -standard, log, scales
    -Rotation was being tricky, save it for later
    -all of the stats
break-out window for options, with rescalable window for graph
save button
red bounding box for current plot selection? not a plot option, but a canvas-level draw so it doesn't save with the figure?

Tips:
-For titles, special formatting can be used as described here -- https://matplotlib.org/1.3.1/users/mathtext.html
    - example, "This is the title $e = x^{random} + y_x$"
    -mathematical expression go in between $--$
    -it will occassionally break the program. Don't close the $ until you're done
-To change the style, axes *must* be created after global style changes, therefore before passed into gui.
    with plt.style.context('dark_background'):
        #...
        #create fig and axes plots
        #...
        gui(fig)
-shared axis labels for each row be accomplished by \
    choosing far left-most plot and leaving right plots blank \
    similarly, shared x labels for multiple columns by choosing bottom
-figsize / dpi

Update notes:
-converting the growing list of if/elif statements to a switch/case-style class improved program idle speed 5-fold (.18s to .0000004s)
    and active speed from .18s to .13s (updating the graph is probably the bottleneck now)
-created a second window for the graph. Hope to make it dynamically expand in the future.

"""
#import time


from tkinter import *
from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.backends import _backend_tk
import tkinter as Tk
import random
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('dark_background')



def gui(*args):
    if len(args)<1:
        fig = Figure(figsize = (10,6))
        ax = fig.add_subplot(121)
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")  
        pts = 1000
        
        mean1, mean2, var1, var2 = 4,7,1,1
        x = [random.gauss(4,1) for _ in range(pts)]
        y = [random.gauss(7,1) for _ in range(pts)]
        bins = np.linspace(0, 10, 100)
        ax.hist(x, bins, alpha=0.5, label='x', color='pink')
        ax.hist(y, bins, alpha=0.5, label='y', color='deepskyblue')
#        ax.plot([1,2,3,4,5,6],[2,2,5,5,3,4])
        ax.legend(loc='upper right')
        ax.grid(True)
        ax.tick_params(labelcolor='white', top='on', bottom='on', left='on', right='on') 
    
        ax2 = fig.add_subplot(122)
        x = [i for i in range(1000)]
        y = [random.gauss(7,1) for _ in range(pts)]
        ax2.plot(x,y)
        ax2.grid(False)
        
    #Otherwise grab the figure passed into the function    
    if len(args)==1:
        fig = args[0]
    #These are for global xlabels and other options later. A hidden axes
    globalax = fig.add_subplot(111, frame_on=False) #ends up being "final" axes of fig.axes[-1] for global settings
    globalax.grid(False)
    globalax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False) 

    #getting info for dynamic GUI rendering listbox
    CURRENT_SUBPLOT = "global"
    subplot_strs = [f"subplot_{i}" for i in range(len(fig.axes))]
    subplot_strs = ["global"] + subplot_strs[:-1]
    
    column_legend = [[sg.Radio('TL', 'legendary', enable_events=True, key='-TL-'), sg.Radio('T', 'legendary', enable_events=True,key='-T-'), 
                      sg.Radio('TR', 'legendary', enable_events=True,key='-TR-')],
                      [sg.Radio('ML', 'legendary', enable_events=True,key='-ML-'), sg.Radio('M', 'legendary', enable_events=True,key='-M-'),
                       sg.Radio('MR', 'legendary', enable_events=True,key='-MR-'),sg.Radio('No Legend', 'legendary', enable_events=True,key='-NOLEGEND-')],
                       [sg.Radio('BL', 'legendary', enable_events=True,key='-BL-'),sg.Radio('B', 'legendary', enable_events=True,key='-B-'),
                        sg.Radio('BR', 'legendary', enable_events=True,key='-BR-')]]
                        
    
    
    #the main settings column for the program
    column1_frame = [[sg.Text('X Label'), 
                      sg.Input(key='-XLABEL-', enable_events=True, size=(30,14))],
                      [sg.Text('Y Label'), 
                       sg.Input(key='-YLABEL-', enable_events=True, size=(30,14))],
                       [sg.Text('XLimits', key='XLIM'), 
                        sg.Input(key='-XMIN-', enable_events=True, size=(4,14)),
                        sg.Input(key='-XMAX-', enable_events=True, size=(4,14)),
                        sg.Text('YLimits'), 
                        sg.Input(key='-YMIN-', enable_events=True, size=(4,14)),
                        sg.Input(key='-YMAX-', enable_events=True, size=(4,14))],
                        [sg.Text('Ticks', key='-TICKTEXT-'), sg.Checkbox("left", enable_events=True, key='-LEFTTICK-', default=True),
                         sg.Checkbox("bottom", enable_events=True, key='-BOTTOMTICK-', default=True),
                         sg.Checkbox("right", enable_events=True, key='-RIGHTTICK-', default=True),
                         sg.Checkbox("top", enable_events=True, key='-TOPTICK-', default=True)], 
                         [sg.Checkbox("Grid", enable_events=True, key='-GRID-', pad=((50,0),0)), 
                          sg.Checkbox("Frame", enable_events=True, key='-FRAME-', default=True),
                          sg.Checkbox("Frame-Part", enable_events=True, key='-FRAMEPART-', default=False)],
                          [sg.Text("Legend"), sg.Column(column_legend)]]  
    column1 = [[sg.Text('Choose subplot:', justification='center', font='Helvetica 14', key='-text2-')],
            [sg.Listbox(values=subplot_strs, key='-SUBPLOT-', size=(20,3), enable_events=True)],
            [sg.Text('Title', justification='center', font='Helvetica 14', key='-OUT-'), sg.Input(key='-TITLE-', enable_events=True, size=(32,14))],
            [sg.Text('Font size', pad=(0,(14,0)), justification='center', font='Helvetica 12', key='-OUT2-'),sg.Slider(range=(1, 32), key='-TITLESIZE-', enable_events = True, 
                      pad=(0,0), default_value=12, size=(24, 15), 
                      orientation='h', font=("Helvetica", 10))],
            [sg.Frame('General Axes Options, global', [[sg.Column(column1_frame)]], key='-AXESBOX-', pad=(0,(14,0)))]]

    
    #And here is where we create the layout
    sg.theme('DarkBlue')
    layout = [[sg.Text('Matplotlib Editor', size=(20, 1), justification='center', font='Helvetica 20')],
               [sg.Column(column1)]]

    layout2 = [[sg.Canvas(size=(fig.get_figwidth()*100, fig.get_figheight()*100), background_color='black', key='canvas')]]
    
   # layout_save()
    
    
    #[sg.Listbox(values=pyplot.style.available, size=(20, 6), key='-STYLE-', enable_events=True)]
    window = sg.Window('Simple GUI to envision ROC curves', layout)    
    window.Finalize()  # needed to access the canvas element prior to reading the window
    
    window_g = sg.Window("Graphing", layout2, resizable=True)
    window_g.Finalize()
    canvas_elem = window_g['canvas']
    graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
    canvas = canvas_elem.TKCanvas

    def update_graph():
        graph.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        canvas.image = photo
        canvas.pack(fill="both", expand=True)
        canvas.create_image(fig.get_figwidth()*100 / 2, fig.get_figheight()*100 / 2, image=photo)
        #canvas.update(size=(size(window_g)[0],size(window_g)[1]))
        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()
        _backend_tk.blit(photo, figure_canvas_agg.get_renderer()._renderer, (0, 1, 2, 3))

    update_graph()
    
    def frame_set(ax, value):
        ax.spines["top"].set_visible(value)
        ax.spines["right"].set_visible(value)
        ax.spines["bottom"].set_visible(value)
        ax.spines["left"].set_visible(value)         


### THIS IS THE MAIN BULK OF THE PROGRAM -- MANAGING EVENTS FOR THE GUI ####    
    class event_manager_class:
        
        def switch(self, event):
            if event != 'Exit' or None:
                event = event[1:-1]
            #print(event)
            getattr(self, event)()
    
        def TITLE(self):
            if CURRENT_SUBPLOT == 'global':
                fig.suptitle(values['-TITLE-'])
            else:
                fig.axes[CURRENT_SUBPLOT].set_title(values['-TITLE-'])

        def TITLESIZE(self):
            fontsize = int(values['-TITLESIZE-'])
            if CURRENT_SUBPLOT == 'global':
                if type(fig._suptitle) is matplotlib.text.Text:
                    fig.suptitle(values['-TITLE-'], fontsize=fontsize)
            else:
                fig.axes[CURRENT_SUBPLOT].set_title(fig.axes[CURRENT_SUBPLOT].get_title(), fontsize=fontsize)
        def XLABEL(self):
            if CURRENT_SUBPLOT == 'global':
                globalax.set_xlabel(values['-XLABEL-'])
            else:
                fig.axes[CURRENT_SUBPLOT].set_xlabel(values['-XLABEL-'])            
        def YLABEL(self):
            if CURRENT_SUBPLOT == 'global':
                globalax.set_ylabel(values['-YLABEL-'])
            else:
                fig.axes[CURRENT_SUBPLOT].set_ylabel(values['-YLABEL-'])           
        def XMIN(self):
            try: limit_update = float(values['-XMIN-'])
            except ValueError: return
            if CURRENT_SUBPLOT == 'global':
                [sub.set_xlim(xmin=limit_update) for sub in fig.axes]
            else:
                fig.axes[CURRENT_SUBPLOT].set_xlim(xmin=limit_update)            
        def XMAX(self):
            try: limit_update = float(values['-XMAX-'])
            except ValueError: return
            if CURRENT_SUBPLOT == 'global':
                [sub.set_xlim(xmax=limit_update) for sub in fig.axes]
            else:
                fig.axes[CURRENT_SUBPLOT].set_xlim(xmax=limit_update)            
        def YMIN(self):
            try: limit_update = float(values['-YMIN-'])
            except ValueError: return
            if CURRENT_SUBPLOT == 'global':
                [sub.set_ylim(ymin=limit_update) for sub in fig.axes]
            else:
                fig.axes[CURRENT_SUBPLOT].set_ylim(ymin=limit_update)            
        def YMAX(self):
            try: limit_update = float(values['-YMAX-'])
            except ValueError: return
            if CURRENT_SUBPLOT == 'global':
                [sub.set_ylim(ymax=limit_update) for sub in fig.axes]
            else:
                fig.axes[CURRENT_SUBPLOT].set_ylim(ymax=limit_update)            
        def LEFTTICK(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.tick_params(left=values['-LEFTTICK-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].tick_params(left=values['-LEFTTICK-'])            
        def TOPTICK(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.tick_params(top=values['-TOPTICK-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].tick_params(top=values['-TOPTICK-'])
        def RIGHTTICK(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.tick_params(right=values['-RIGHTTICK-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].tick_params(right=values['-RIGHTTICK-'])            
        def BOTTOMTICK(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.tick_params(bottom=values['-BOTTOMTICK-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].tick_params(bottom=values['-BOTTOMTICK-'])    
        def GRID(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.grid(values['-GRID-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].grid(values['-GRID-'])
        def FRAME(self):
            if CURRENT_SUBPLOT == 'global':
                [frame_set(sub, values['-FRAME-']) for sub in fig.axes[0:-1]]
            else:
                frame_set(fig.axes[CURRENT_SUBPLOT], values['-FRAME-'])
        def FRAMEPART(self):
            if CURRENT_SUBPLOT == 'global':
                [sub.spines["top"].set_visible(values['-FRAMEPART-']) for sub in fig.axes[0:-1]]
                [sub.spines["right"].set_visible(values['-FRAMEPART-']) for sub in fig.axes[0:-1]]
            else:
                fig.axes[CURRENT_SUBPLOT].spines["top"].set_visible(values['-FRAMEPART-'])   
                fig.axes[CURRENT_SUBPLOT].spines["right"].set_visible(values['-FRAMEPART-'])
        #Radio Buttons for legend
        def TL(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=2) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=2)
        def T(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=9) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=9)               
        def TR(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=1) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=1)              
        def ML(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=6) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=6) 
        def M(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=10) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=10)
        def MR(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=7) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=7)     
        def BL(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=3) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=3)            
        def B(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=8) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=8)              
        def BR(self):
            if CURRENT_SUBPLOT == 'global': [sub.legend(loc=4) for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend(loc=4)
        def NOLEGEND(self):  
            if CURRENT_SUBPLOT == 'global': [sub.legend().remove() for sub in fig.axes[0:-1]]
            else: fig.axes[CURRENT_SUBPLOT].legend().remove()             

################################################################################################
            
    event_manager = event_manager_class()
    
    while True:
        event, values = window.read(timeout=10)
        #print(event)
        #tic = time.perf_counter()
    
        if event == 'Exit' or event is None:
            break
        elif event == '__TIMEOUT__':
            pass
        #This gets a special elif bc I need to change the global variable CURRENT_SUBPLOT
        elif event == '-SUBPLOT-':
            idx = values['-SUBPLOT-'][0][-1]
            if idx.isdigit():    
                CURRENT_SUBPLOT = int(idx)
            else:
                CURRENT_SUBPLOT = 'global'
            window['-AXESBOX-'].Update("General Axes Options, " + values['-SUBPLOT-'][0])            
        else:
            event_manager.switch(event)
            update_graph()
        #toc = time.perf_counter()
        #print(toc-tic)

    #window['-OUT-'].update(CURRENT_SUBPLOT)
    
    
    window.close()
    window_g.close()

