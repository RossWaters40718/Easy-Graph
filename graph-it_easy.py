from win32api import GetMonitorInfo, MonitorFromPoint
from tkinter.filedialog import asksaveasfile, askopenfile
import tkinter as tk
from tkinter import StringVar, IntVar, BooleanVar, simpledialog
from tkinter import font, Menu, colorchooser, messagebox
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as pch
import time
from datetime import datetime
import numpy as np
import os
#
# Notes For End Users:
# Matplotlib Graph For Windows Using TK Backend.
# There Are Several Methods That May Be Used To Configure The Graph.
# The Provided Menus Offer Almost All Properties For Configuration before
# Executing Your Code From The Test Menu. Another Way Is To Setup All The
# tk Variables Found In (set_defaults()) Before Runtime Or Setup These Variables
# In Your Code And Then Executing (set_axes()) Prior To Drawing. You Will Find Some
# Existing Functions That I Created Just To Make Things Easier To Change With
# Code During Runtime. View The Examples Provided For These Functions. Of Course
# You May Add More Functions Or Just Use Standard matplotlib Procedures For Change.
# The Class (Test) Provides Place Holders For Test Menu Items And Test Code.  
# There Are 3 Ways To Plot A Graph:
# If X And Y Data Are In Lists Or Numpy Arrays, There Are 2 Plotting Types. Loop Or Instant.
# X And Y Values Must Be In Their Own Seperate List Or Numpy Array. If Not Then Modification Is Required.
# To Use The Loop Type, Set Argument Test.log('loop') exe_style ='loop'.
# To Use Instant, Set Argument Test.log('instant') exe_style ='instant'.
# The 3rd Way To Plot Is Using Live Incomming Data. Set Argument Test.log('live') exe_style ='live'.
# The Argument int (plt_num) Is Used To Reset For A New Plot.
# For Each Time A New Plot Sequence On The Same Graph, Increment plt_num by 1
# The str(color,style,width) Arguments Are Basically Matplotlib Std For plt.plot().
# All Plotted Values Are Stored In List(Plot_Data) Until Cleared By clear_graph().
# These Values (Plot_Data) Can Be Saved To Text Files Before Clearing In File Menu
# Or Being Cleared By Starting A New Test (clear_graph()) Function.
#
class Test():
    def log(exe_style):# Example
        clear_graph() # Always Call clear_graph() To Start Fresh.
        # These May Be Omitted If Setup In Menus
        #//////////////////////////////
        if exe_style=='loop':set_title('X Scale = Log, Draw Style = Loop Update Using Lists (100 pts.)')
        elif exe_style=='instant':set_title('X Scale = Log, Draw Style = Instant Update Using Lists (100 pts.)')
        elif exe_style=='live':set_title('X Scale = Log, Draw Style = Live Update (100 pts.)')
        set_xlabel('Frequency In hz')
        set_xscale_style('log') # Always Set Scale Style Before Scale
        set_x_scale('20,20000')
        set_ylabel('Amplitude In dB')
        set_yscale_style('linear')
        set_y_scale('-10,10')
        #//////////////////////////////
        # Customize Line Properties, X and/or Y Asis Tick Labels And Legends
        #Set Plot 1 2DLine  Properties
        plt1_color='aqua'# Set The Line Color
        plt1_style='solid'# Set The Line Style
        plt1_width=1# Set The Line Width
        #Set Plot 2 2DLine  Properties
        plt2_color='yellow'# Set The Line Color
        plt2_style='dotted'# Set The Line Style
        plt2_width=2# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt3_color='lightgray'# Set The Line Color
        plt3_style=''# Set The Line Style
        plt3_width=0# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt4_color='lightgray'# Set The Line Color
        plt4_style=''# Set The Line Style
        plt4_width=0# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt5_color='lightgray'# Set The Line Color
        plt5_style=''# Set The Line Style
        plt5_width=0# Set The Line Width
        # Plot Legends
        legend1=pch.Patch(color=plt1_color, label='Plot 1')
        legend2=pch.Patch(color=plt2_color, label='Plot 2')
        legend3=pch.Patch(color=plt3_color, label='Plot 3')
        legend4=pch.Patch(color=plt4_color, label='Plot 4')
        legend5=pch.Patch(color=plt5_color, label='Plot 5')
        plt.legend(bbox_to_anchor=(0.995, 1.15),frameon = 0,facecolor=Window_Color.get(),labelcolor='linecolor',
                fontsize=8,framealpha=1,loc='upper left',handles=[legend1,legend2,legend3,legend4,legend5])
        date_time= datetime.now().strftime("%m/%d/%Y %H:%M:%S")# Time Stamp For Save Data File
        file_header=['Plot Number--X Value--Y Value--Line Color--Line Style--Line Width--Date/Time:',date_time]
        Plot_Data.append(file_header) # Header For Save Data File
        # Customize X and/or Y Asis Tick Labels Here Without affecting Limits
        ax.set_xticks([20,50,100,200,500,1000,2000,5000,10000,20000])
        new_xticks=['20','50','100','200','500','1k','2k','5k','10k','20k']
        change_tick_labels('x',new_xticks)
        # ******************** Plot 1 ********************
        plt_num=1 # Set The Plot Number For The Save File Option
        # Present Your Lists Data Here Or Inside Loop
        x=np.geomspace(20.0, 20000.0, num=100, endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
        y=np.random.uniform(low=-10.0, high=10.0, size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
        if exe_style=='loop': # @ 300 fps
            for i in np.arange(1,len(x)+1): # Start Should Always Be 1 With Stop At Length + 1
                line.set_data(x[:i], y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
        elif exe_style=='instant':# Instantly Update Graph With List Data
            line.set_data(x, y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            for i in range(0, len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
        elif exe_style=='live': # Live Update
            x=np.geomspace(20.0, 20000.0, num=100, endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
            y_data=np.random.uniform(low=-10.0, high=10.0, size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
            for i in np.arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x And 2 y Values Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line.set_data(x[:i+1], y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
            x.clear()
            y.clear()
        # ******************** Plot 2 ********************
        plt_num=2 # Set The Plot Number For Save File Option
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Place Your Data Here
        x=np.geomspace(20.0, 20000.0, num=100, endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
        y=np.random.uniform(low=-10.0, high=10.0, size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
        if exe_style=='loop': # Loop Through Lists Data
            for i in np.arange(1,len(x)+1): # Start Should Always Be 1 With Stop At Length + 1
                line.set_data(x[:i], y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
        elif exe_style=='instant': # Instantly Update Graph With List Data
            line.set_data(x, y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            # redraw just the points
            ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            for i in range(0, len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(newline)
        elif exe_style=='live': # Incomming Data Inside Test Loop
            x_data=np.geomspace(20.0, 20000.0, num=100, endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
            y_data=np.random.uniform(low=-10.0, high=10.0, size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
            for i in np.arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x And 2 y Values Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line.set_data(x[:i+1], y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
            x.clear()
            y.clear()
    def linear(exe_style):# Example
        clear_graph() # Always Call clear_graph() To Start Fresh.
        # These May Be Omitted If Setup In Menus
        #//////////////////////////////
        if exe_style=='loop':set_title('X Scale = Linear, Draw Style = Loop Update Using Lists (100 pts.)')
        elif exe_style=='instant':set_title('X Scale = Linear, Draw Style = Instant Update Using Lists (100 pts.)')
        elif exe_style=='live':set_title('X Scale = Linear, Draw Style = Live Update (100 pts.)')
        set_xscale_style('linear') # Always Set Scale Style Before Scale
        set_x_scale('0.0,500.0')
        set_xlabel('Time In Seconds')
        set_ylabel('Current In Amperes')
        set_yscale_style('linear')
        set_y_scale('0,500')
        #//////////////////////////////
        # Customize Line Properties, X and/or Y Asis Tick Labels And Legends
        #Set Plot 1 2DLine  Properties
        plt1_color='aqua'# Set The Line Color
        plt1_style='solid'# Set The Line Style
        plt1_width=1# Set The Line Width
        #Set Plot 2 2DLine  Properties
        plt2_color='lime'# Set The Line Color
        plt2_style='dotted'# Set The Line Style
        plt2_width=2# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt3_color='lightgray'# Set The Line Color
        plt3_style=''# Set The Line Style
        plt3_width=0# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt4_color='lightgray'# Set The Line Color
        plt4_style=''# Set The Line Style
        plt4_width=0# Set The Line Width
        #Set Plot 3 2DLine  Properties
        plt5_color='lightgray'# Set The Line Color
        plt5_style=''# Set The Line Style
        plt5_width=0# Set The Line Width
        # Plot Legends
        legend1=pch.Patch(color=plt1_color, label='Plot 1')
        legend2=pch.Patch(color=plt2_color, label='Plot 2')
        legend3=pch.Patch(color=plt3_color, label='Plot 3')
        legend4=pch.Patch(color=plt4_color, label='Plot 4')
        legend5=pch.Patch(color=plt5_color, label='Plot 5')
        plt.legend(bbox_to_anchor=(0.995, 1.15),frameon = 0,facecolor=Window_Color.get(),labelcolor='linecolor',
                fontsize=8,framealpha=1,loc='upper left',handles=[legend1,legend2,legend3,legend4,legend5])
        date_time= datetime.now().strftime("%m/%d/%Y %H:%M:%S")# Time Stamp For Save Data File
        file_header=['Plot Number--X Value--Y Value--Line Color--Line Style--Line Width--Date/Time:',date_time]
        Plot_Data.append(file_header) # Header For Save Data File
        # Change X and/or Y Asis Tick Labels Here Without affecting Limits
        ax.set_xticks([0,100,200,300,400,500])
        new_xticks=['0','100m','200m','300m','400m','500m']
        change_tick_labels('x',new_xticks)
        ax.set_yticks([0,100,200,300,400,500])
        new_yticks=['0','100m','200m','300m','400m','500m']
        change_tick_labels('y',new_yticks)
        # ******************** Plot 1 ********************
        plt_num=1# Set The Plot Number
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Data Can Also Be Incomming X And Y Data From Test Equipment Or Sensors.
        # Place Your Lists Data Here
        x_data=np.linspace(0.0,500.0, num=100)# 100 linear x values 0.0 to 500
        y_data=np.random.uniform(low=0.0, high=500.0, size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
        if exe_style=='loop':
            for i in np.arange(1,len(x_data)+1): # Start Should Always Be 1 With Stop At Length + 1
                line.set_data(x_data[:i], y_data[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x_data[i-1],y_data[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
        elif exe_style=='instant': # Instantly Update Graph With List Data
            line.set_data(x_data, y_data)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            # redraw just the points
            ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            for i in range(0, len(x_data)): # Data For Saving To File
                newline=[plt_num,x_data[i],y_data[i],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
        elif exe_style=='live':
            x_data=np.linspace(0.0,500.0, num=100)# 100 linear x values 0.0 to 500
            y_data=np.random.uniform(low=0.0, high=500.0, size=(100,))
            x,y=[],[]
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
            for i in np.arange(100):# Range Must Be Predetermined If Using Loop
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x And 2 y Values Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line.set_data(x[:i+1], y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
            x.clear()
            y.clear()
        # ******************** Plot 2 ********************
        plt_num=2 # Set The Plot Number By 1
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Data Can Also Be Incomming X And Y Data From Test Equipment Or Sensors.
        x=np.linspace(0.0,500.0, num=100)# 100 linear x values 0.0 to 500
        y=np.random.uniform(low=0.0, high=500.0, size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
        if exe_style=='loop':
            for i in np.arange(1,len(x)+1):
                line.set_data(x[:i], y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
        elif exe_style=='instant': # Instantly Update Graph With np.array Data
            line.set_data(x, y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            # redraw just the points
            ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            for i in range(0, len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(newline)
        elif exe_style=='live':
            x_data=np.linspace(0.0,500.0, num=100)# 100 linear x values 0.0 to 500
            y_data=np.random.uniform(low=0.0, high=500.0, size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
            for i in np.arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x And 2 y Values Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line.set_data(x[:i+1], y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(newline)
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                #time.sleep(0.01)
            x.clear()
            y.clear()
    def test_1():
        clear_graph()
        #////******* Place Test Code Here *******\\\\#
    def test_2():
        clear_graph()
        #////******* Place Test Code Here *******\\\\#
    def test_3():
        clear_graph()
        #////******* Place Test Code Here *******\\\\#
    def test_4():
        clear_graph()
        #////******* Place Test Code Here *******\\\\#
    def test_5():
        clear_graph()
        #////******* Place Test Code Here *******\\\\#
    def test_menu():
        #////******* Here You Can Modify The Menu To Suit Your Needs *******\\\\#
        tst = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Tests', menu=tst)
        tst.add_command(label ='Log Scale "Loop" Example', command=lambda:Test.log('loop'))
        tst.add_separator()
        tst.add_command(label ='Linear Scale "Instant: Example', command=lambda:Test.linear('instant'))
        tst.add_separator()
        tst.add_command(label ='Linear Scale "Live" Example', command=lambda:Test.linear('live'))
        tst.add_separator()
        tst.add_command(label ='Test 1 (Empty)', command=lambda:Test.test_2())
        tst.add_separator()
        tst.add_command(label ='Test 2 (Empty)', command=lambda:Test.test_2())
        tst.add_separator()
        tst.add_command(label ='Test 3 (Empty)', command=lambda:Test.test_3())
        tst.add_separator()
        tst.add_command(label ='Test 4 (Empty)', command=lambda:Test.test_4())
        tst.add_separator()
        tst.add_command(label ='Test 5 (Empty)', command=lambda:Test.test_5())
        tst.add_separator()
        root.config(menu = menubar)
def open_file():
    file=askopenfile(mode='r', filetypes=[("Plot Documents","*.plt"),("Text Documents","*.txt")])
    if file is not None:
        os.system(file.name)
def save_data_as():
    user_directory=os.path.expanduser( '~' )
    path=os.path.join(user_directory, 'Documents', '' )
    file=asksaveasfile(initialdir=path,
        defaultextension=".plt",filetypes=[("Plot Documents","*.plt"),("Text Documents","*.txt")])     
    if file is not None:
        with open(file.name, mode='wt', encoding='utf-8') as myfile:
            for lines in range(0,len(Plot_Data)):
                myfile.write(str(lines+1)+' '+str(Plot_Data[lines]))
                myfile.write('\n')
def destroy():# X Icon Was Clicked Or File/Exit
    Plot_Data.clear()
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):widget.destroy()
        else: widget.destroy()
        os._exit(0)
    return
def about():
    messagebox.showinfo('About Graph-It Easy', 'Creator: Ross Waters\nEmail: RossWatersjr@gmail.com'\
        '\nLanguage: Python version 3.11.0 64-bit'\
        '\nProgram: graph-it_easy.py Created Using\ntkinter version 8.6,\nmatplotlib version 3.6.2'\
        '\nRevision \ Date: 1.1.4 \ 02/05/2023'\
        '\nCreated For Windows 10/11')
def config_g(which): # Configure Graph Menu
    if which=='window color':        
        color_code = colorchooser.askcolor(title ="Choose Window Color", initialcolor=Window_Color.get())
        if color_code[1]==None:return
        Window_Color.set(color_code[1])
        fig.patch.set_facecolor(Window_Color.get())# Set the Figure Facecolor
    elif which=='graph color':        
        color_code = colorchooser.askcolor(title ="Choose Graph Color", initialcolor=Graph_Color.get())
        if color_code[1]==None:return
        Graph_Color.set(color_code[1])
        ax.set_facecolor(Graph_Color.get())# Set the Graph Facecolor
    elif which=='text':        
        txt=simpledialog.askstring("<Window Title Text>","Enter Text To Display For Window Title.",
            parent=root, initialvalue=Title.get())
        if txt==''or txt==None:return
        set_title(txt)
    elif which=='color':
        color_code = colorchooser.askcolor(title ="Choose Title Color", initialcolor=Title_Color.get())
        if color_code[1]==None:return
        ax.set_title(Title.get(), ha='center', color=color_code[1],
            fontsize=Title_Fontsize.get(), weight='normal', style='italic')
        Title_Color.set(color_code[1])
    elif which=='fontsize':
        size=simpledialog.askinteger("<Window Title Fontsize>","Enter Font Size To Display For Window Title.",
            parent=root, minvalue=6, maxvalue=32, initialvalue=Title_Fontsize.get())
        if size is None:return
        ax.set_title(Title.get(), ha='center', color=Title_Color.get(),
        fontsize=size, weight='normal', style='italic')
        Title_Fontsize.set(size)
    elif which=='show minor':
        if Show_Minor.get():
            msg='Turn "Off" Graph Minor Grid Lines?'
        else:msg='Turn "On" Graph Minor Grid Lines?'
        answer = messagebox.askyesno("Show Minor Ticks",msg)
        if answer==True and Show_Minor.get():
            Show_Minor.set(False)
            plt.minorticks_off()
        elif answer==True and not Show_Minor.get():
            Show_Minor.set(True)
            plt.minorticks_on()
        elif answer==False:return    
    elif which=='major color':        
        color_code = colorchooser.askcolor(title ="Choose Major Grid Line Color", initialcolor=Major_Color.get())
        if color_code[1]==None:return
        Major_Color.set(color_code[1])
        ax.grid(which='major', color= Major_Color.get(), linestyle='solid')
    elif which=='minor color':        
        color_code = colorchooser.askcolor(title ="Choose Minor Grid Line Color", initialcolor=Major_Color.get())
        if color_code[1]==None:return
        Minor_Color.set(color_code[1])
        ax.grid(which='minor', color= Minor_Color.get(), linestyle='solid') 
    # Major Grid Lines
    elif which=='major style solid':
        Major_Style.set('solid')
        ax.grid(which='major', color= Major_Color.get(), linestyle=Major_Style.get()) 
    elif which=='major style dotted':
        Major_Style.set('dotted')
        ax.grid(which='major', color= Major_Color.get(), linestyle=Major_Style.get()) 
    elif which=='major style dashed':
        Major_Style.set('dashed')
        ax.grid(which='major', color= Major_Color.get(), linestyle=Major_Style.get()) 
    elif which=='major style dashdot':
        Major_Style.set('dashdot')
        ax.grid(which='major', color= Major_Color.get(), linestyle=Major_Style.get())
    # Minor Grid Lines
    elif which=='minor style solid':
        Minor_Style.set('solid')
        ax.grid(which='minor', color= Minor_Color.get(), linestyle=Minor_Style.get()) 
    elif which=='minor style dotted':
        Minor_Style.set('dotted')
        ax.grid(which='minor', color= Minor_Color.get(), linestyle=Minor_Style.get()) 
    elif which=='minor style dashed':
        Minor_Style.set('dashed')
        ax.grid(which='minor', color= Minor_Color.get(), linestyle=Minor_Style.get()) 
    elif which=='minor style dashdot':
        Minor_Style.set('dashdot')
        ax.grid(which='minor', color= Minor_Color.get(), linestyle=Minor_Style.get())
    elif which=='clear':
        clear_graph()
    fig.canvas.draw()
def config_x(which): # Configure X Axis Menu
    if which=='text':
        txt=simpledialog.askstring("<X Label Text>","Enter Text To Display For X Label.",
            parent=root, initialvalue='X Label')
        if txt==''or txt==None:return
        X_Text.set(txt)
    elif which=='fontsize':        
        size=simpledialog.askinteger("<X Label Fontsize>","Enter Font Size To Display For X Label.",
            parent=root, minvalue=6, maxvalue=32, initialvalue=X_Fontsize.get())
        if size is None:return
        X_Fontsize.set(size)
    elif which=='color':        
        color_code = colorchooser.askcolor(title ="Choose X Label Text Color", initialcolor=X_Color.get())
        if color_code[1]==None:return
        X_Color.set(color_code[1])
    elif which=='tick fontsize':        
        size=simpledialog.askinteger("<X Tick Labels Fontsize>","Enter Font Size To Display For X Tick Labels.",
            parent=root, minvalue=6, maxvalue=32, initialvalue=XTick_Fontsize.get())
        if size is None:return
        XTick_Fontsize.set(size)
        ax.tick_params(axis='x', which='major', labelsize=XTick_Fontsize.get())
    elif which=='tick color':        
        color_code = colorchooser.askcolor(title ="Choose X Tick Label Color", initialcolor=XTick_Color.get())
        if color_code[1]==None:return
        XTick_Color.set(color_code[1])
        ax.tick_params(axis='x', colors=XTick_Color.get()) # Grid And Label The Axis Ticks
    elif which=='linear' or which=='log' or which=='symlog':
        set_xscale_style(which)
    elif which=='x limits':
        x=simpledialog.askstring("<X Axis Scale>","Set X Axis Scale 'Left, Right'. Example: 0.0, 10.0",
            parent=root, initialvalue=X_Scale.get())
        set_x_scale(x)    
        return    
    ax.set_xlabel(X_Text.get(), ha='center', color=X_Color.get(),
        fontsize=X_Fontsize.get(), weight='normal', style='italic')
    fig.canvas.draw()
def config_y(which): # Configure Y Axis Menu
    if which=='text':
        txt=simpledialog.askstring("<Y Label Text>","Enter Text To Display For Y Label.",
            parent=root, initialvalue='Y Label')
        if txt==''or txt==None:return
        Y_Text.set(txt)
    elif which=='fontsize':        
        size=simpledialog.askinteger("<Y Label Fontsize>","Enter Font Size To Display For Y Label.",
            parent=root, minvalue=6, maxvalue=32, initialvalue=Y_Fontsize.get())
        if size is None:return
        Y_Fontsize.set(size)
    elif which=='color':        
        color_code = colorchooser.askcolor(title ="Choose Y Label Text Color", initialcolor=Y_Color.get())
        if color_code[1]==None:return
        Y_Color.set(color_code[1])
    elif which=='tick fontsize':        
        size=simpledialog.askinteger("<Y Tick Labels Fontsize>","Enter Font Size To Display For Y Tick Labels.",
            parent=root, minvalue=6, maxvalue=32, initialvalue=YTick_Fontsize.get())
        if size is None:return
        YTick_Fontsize.set(size)
        ax.tick_params(axis='y', which='major', labelsize=YTick_Fontsize.get())
    elif which=='tick color':        
        color_code = colorchooser.askcolor(title ="Choose Y Tick Label Color", initialcolor=YTick_Color.get())
        if color_code[1]==None:return
        YTick_Color.set(color_code[1])
        ax.tick_params(axis='y', colors=YTick_Color.get()) # Grid And Label The Axis Ticks
    elif which=='linear' or which=='log' or which=='symlog':
        set_yscale_style(which)
    elif which=='y limits':
        y=simpledialog.askstring("<Y Axis Scale>","Set Y Axis Scale 'Bottom, Top'. Example: 0.0, 10.0",
            parent=root, initialvalue=Y_Scale.get())
        set_y_scale(y)    
    ax.set_ylabel(Y_Text.get(), ha='center', color=Y_Color.get(),
        fontsize=Y_Fontsize.get(), weight='normal', style='italic')
    fig.canvas.draw()
def clear_graph(): # Gets Things Ready For New Plot Sequence
    Plot_Data.clear()
    ax.cla()
    set_axes()
def set_title(txt):
    ax.set_title(txt, ha='center', color=Title_Color.get(),
        fontsize=Title_Fontsize.get(), weight='normal', style='italic')
    Title.set(txt)
def set_xlabel(txt):
    ax.set_xlabel(txt, ha='center', color=X_Color.get(),
        fontsize=X_Fontsize.get(), weight='normal', style='italic')
    X_Text.set(txt)
def set_ylabel(txt):
    ax.set_ylabel(txt, ha='center', color=Y_Color.get(),
        fontsize=Y_Fontsize.get(), weight='normal', style='italic')
    Y_Text.set(txt)
def set_xscale_style(style):
    plt.xscale(style)
    if Show_Minor.get():plt.minorticks_on()
    else:plt.minorticks_off()
    X_Style.set(style)
def set_yscale_style(style):
    plt.yscale(style)
    if Show_Minor.get():plt.minorticks_on()
    else:plt.minorticks_off()
    Y_Style.set(style)
def change_tick_labels(axis,list):# Changes X-Y Asis Tick Labels Without affecting Limits
    if axis=='x':
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())        
        locs, labels=plt.xticks()
        labels=list
        plt.xticks(locs, labels)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.5)# Give Time To Update New locs,labels
    elif axis=='y':    
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())        
        locs, labels=plt.yticks()
        labels=list
        plt.yticks(locs, labels)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.5)# Give Time To Update New locs,labels
def set_x_scale(x):# Argument is String value Of X1, X2. Example: "10.0, 100.0"         
    if x==None or x=='':return
    temp=str(x).replace('-','').replace(',','').replace(' ','').replace('.','') # Verify That All Are Numeric Values
    if temp.isdecimal():
        x_scale=x.split(",")
        X_Scale.set(x)
        x1=float(x_scale[0])
        x2=float(x_scale[1])
        if X_Style.get()!='linear':
            if x1<=0 or x2<=0: 
                msg='X Axis Scale "Log" Values Cannot Be Zero Or Less! Please Try Again.'
                messagebox.showerror("<X Axis Scale>",msg)
                return
        ax.set_xlim([x1,x2])
        fig.canvas.draw()
    else:
        msg='Something Is Incorrect With The X Axis Values Entered! Please Try Again.'
        messagebox.showerror("<X Axis Scale>",msg)
        return
def set_y_scale(y): # Argument is String value Of Y1, Y2. Example: "10.0, 100.0"            
    if y==None or y=='':return
    temp=str(y).replace('-','').replace(',','').replace(' ','').replace('.','') # Verify That All Are Numeric Values
    if temp.isdecimal():
        y_scale=y.split(",")
        Y_Scale.set(y)    
        y1=float(y_scale[0])
        y2=float(y_scale[1])
        if Y_Style.get()!='linear':
            if y1<=0 or y2<=0: 
                msg='Y Axis Scale "Log" Values Cannot Be Zero Or Less! Please Try Again.'
                messagebox.showerror("<Y Axis Scale>",msg)
                return
        ax.set_ylim([y1,y2])
        fig.canvas.draw()
    else:
        msg='Something Is Incorrect With The Y Axis Values Entered! Please Try Again.'
        messagebox.showerror("<Y Axis Scale>",msg)
        return    
def set_axes():
    plt.cla()
    plt.grid(True)
    plt.xscale(X_Style.get())
    plt.yscale(Y_Style.get())
    if Show_Minor.get():plt.minorticks_on()
    else:plt.minorticks_off()
    x=X_Scale.get().split(",")
    x1=float(x[0])
    x2=float(x[1])
    ax.set_xlim([x1,x2])
    fig.patch.set_facecolor(Window_Color.get())# Set the Window Facecolor
    ax.set_facecolor(Graph_Color.get())# Set the Graph Facecolor
    y=Y_Scale.get().split(",")
    y1=float(y[0])
    y2=float(y[1])
    ax.set_ylim([y1,y2])
    fig.add_axes(ax)        
    ax.tick_params(axis='x', colors=XTick_Color.get()) # Grid And Label The Axis Ticks
    ax.tick_params(axis='y', colors=YTick_Color.get())
    ax.tick_params(axis='x', which='major', labelsize=XTick_Fontsize.get())
    ax.tick_params(axis='y', which='major', labelsize=XTick_Fontsize.get())
    ax.grid(which='major', color= Major_Color.get(), linestyle=Major_Style.get()) # Turn Both Major and Minor Ticks On
    ax.grid(which='minor', color= Minor_Color.get(), linestyle=Minor_Style.get())
    ax.set_title(Title.get(), ha='center', color=Title_Color.get(),
        fontsize=Title_Fontsize.get(), weight='normal', style='italic')
    ax.set_xlabel(X_Text.get(), ha='center', color=X_Color.get(),
        fontsize=X_Fontsize.get(), weight='normal', style='italic')
    ax.set_ylabel(Y_Text.get(), ha='center', color=Y_Color.get(),
        fontsize=Y_Fontsize.get(), weight='normal', style='italic')
    ax.autoscale(enable=False, axis="x", tight=True)    
    ax.autoscale(enable=False, axis="y", tight=True)    
    fig.canvas.draw()
    return
def set_defaults():
    Plot_Data.clear()
    First_Points.set(False)
    Window_Color.set('#000000')
    Graph_Color.set('#09031e')
    Title.set('Title')
    Title_Color.set('#70ffff')
    Title_Fontsize.set(16)
    Major_Color.set('#7e7e7e')
    Minor_Color.set('#7e7e7e')
    Major_Style.set('solid')
    Minor_Style.set('dotted')
    Show_Minor.set(True)
    X_Text.set('X Label')
    X_Color.set('#70ffff')
    X_Fontsize.set(12)
    XTick_Fontsize.set(10)
    XTick_Color.set('#ffffff')
    X_Style.set('linear')
    X_Scale.set('0.0, 5.0')
    Y_Text.set('Y Label')
    Y_Color.set('#70ffff')
    Y_Fontsize.set(12)
    YTick_Fontsize.set(10)
    YTick_Color.set('#ffffff')
    Y_Style.set('linear')
    Y_Scale.set('0.0, 5.0')
    set_axes()
if __name__ == "__main__":
    root=tk.Tk()
    root.font=font.Font(family='lucidas', size=12, weight='normal', slant='italic')
    root.title('Graph-It Easy')
    monitor_info=GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area=monitor_info.get("Work")
    monitor_area=monitor_info.get("Monitor")
    screen_width=work_area[2]
    screen_height=work_area[3]
    taskbar_hgt=(monitor_area[3]-work_area[3])
    root.configure(bg='gray')
    root.option_add('*TCombobox*Listbox.font', root.font)
    root.protocol("WM_DELETE_WINDOW", destroy)
    fig=plt.figure(figsize=(10, 10),facecolor='black',frameon=True,)
    ax=plt.axes()
    fig.add_axes(ax)        
    canvas=FigureCanvasTkAgg(fig, master=root) # Create The Canvas
    toolbar=NavigationToolbar2Tk(canvas, root) # create Matplotlib toolbar
    tb_hgt=toolbar.winfo_reqheight()
    root_hgt=((screen_height-taskbar_hgt)/2.0)+tb_hgt 
    root_wid=root_hgt*2.0
    x=(screen_width/2)-(root_wid/2)
    y=(screen_height/2)-(root_hgt/2)
    root.geometry('%dx%d+%d+%d' % (root_wid, root_hgt, x, y, )) # Position Center Of Screen
    canvas.get_tk_widget().pack(fill='both',pady=(0,0)) # place Canvas and Toolbar on Tkinter window
    Plot_Data=[]
    First_Points=BooleanVar()
    Window_Color=StringVar()
    Graph_Color=StringVar()
    Title=StringVar()
    Title_Color=StringVar()
    Title_Fontsize=IntVar()
    Major_Color=StringVar()
    Minor_Color=StringVar()
    Major_Style=StringVar()
    Minor_Style=StringVar()
    Show_Minor=BooleanVar()
    X_Text=StringVar()
    X_Color=StringVar()
    X_Fontsize=IntVar()
    XTick_Color=StringVar()
    XTick_Fontsize=IntVar()
    X_Style=StringVar()
    X_Scale=StringVar()
    Y_Text=StringVar()
    Y_Color=StringVar()
    Y_Fontsize=IntVar()
    YTick_Fontsize=IntVar()
    YTick_Color=StringVar()
    Y_Style=StringVar()
    Y_Scale=StringVar()
    menubar = Menu(root)# Creating Menubar
    file = Menu(menubar, tearoff = 0)# File Menu and commands
    menubar.add_cascade(label ='File', menu = file)
    file.add_command(label ='Open File', command=lambda:open_file())
    file.add_separator()
    file.add_command(label ='Save Data As', command=lambda:save_data_as())
    file.add_separator()
    file.add_command(label ='About', command=lambda:about())
    file.add_separator()
    file.add_command(label ='Exit', command=lambda:destroy())
    file.add_separator()
    configure_g = Menu(menubar, tearoff = 0)# Configure Graph Menu and commands
    menubar.add_cascade(label ='Graph Config', menu = configure_g)
    configure_g.add_command(label ='Window Face Color', command=lambda:config_g('window color'))
    configure_g.add_separator()
    configure_g.add_command(label ='Graph Face Color', command=lambda:config_g('graph color'))
    configure_g.add_separator()
    title = Menu(menubar, tearoff=0) # SubMenu
    title.add_command(label='Text', command=lambda:config_g('text'))
    title.add_command(label='Color', command=lambda:config_g('color'))
    title.add_command(label='Font Size', command=lambda:config_g('fontsize'))
    configure_g.add_cascade(label='Window Title', menu=title)
    configure_g.add_separator()
    configure_g.add_command(label ='Major Grid Line Color', command=lambda:config_g('major color'))
    configure_g.add_separator()
    style1 = Menu(menubar, tearoff=0) # SubMenu
    style1.add_command(label='Solid', command=lambda:config_g('major style solid'))
    style1.add_command(label='Dotted', command=lambda:config_g('major style dotted'))
    style1.add_command(label='Dashed', command=lambda:config_g('major style dashed'))
    style1.add_command(label='DashDot', command=lambda:config_g('major style dashdot'))
    configure_g.add_cascade(label='Major Grid Line Style', menu=style1)
    configure_g.add_separator()
    configure_g.add_command(label ='Minor Grid Line Color', command=lambda:config_g('minor color'))
    configure_g.add_separator()
    style_2 = Menu(menubar, tearoff=0) # SubMenu
    style_2.add_command(label='Solid', command=lambda:config_g('minor style solid'))
    style_2.add_command(label='Dotted', command=lambda:config_g('minor style dotted'))
    style_2.add_command(label='Dashed', command=lambda:config_g('minor style dashed'))
    style_2.add_command(label='DashDot', command=lambda:config_g('minor style dashdot'))
    configure_g.add_cascade(label='Minor Grid Line Style', menu=style_2)
    configure_g.add_separator()
    configure_g.add_command(label ='Show Minor Grid Lines', command=lambda:config_g('show minor'))
    configure_g.add_separator()
    configure_g.add_command(label ='Clear Graph Data', command=lambda:config_g('clear'))
    configure_g.add_separator()
    configure_x = Menu(menubar, tearoff = 0)# Configure X Menu and commands
    menubar.add_cascade(label ='X Axis Config.', menu = configure_x)
    x_label = Menu(menubar, tearoff=0) # SubMenu
    x_label.add_command(label='Text', command=lambda:config_x('text'))
    x_label.add_command(label='Color', command=lambda:config_x('color'))
    x_label.add_command(label='Font Size', command=lambda:config_x('fontsize'))
    configure_x.add_cascade(label='X Axis Label', menu=x_label)
    configure_x.add_separator()
    configure_x.add_command(label ='X Tick Label Color',  command=lambda:config_x('tick color'))
    configure_x.add_separator()
    configure_x.add_command(label ='X Tick Label Font Size',  command=lambda:config_x('tick fontsize'))
    configure_x.add_separator()
    style3 = Menu(menubar, tearoff=0) # SubMenu
    style3.add_command(label='Linear', command=lambda:config_x('linear'))
    style3.add_command(label='Log', command=lambda:config_x('log'))
    style3.add_command(label='SymLog', command=lambda:config_x('symlog'))
    configure_x.add_command(label ='X Axis Scale', command=lambda:config_x('x limits'))
    configure_x.add_separator()
    configure_x.add_cascade(label='X Axis Scale Style', menu=style3)
    configure_x.add_separator()
    configure_y = Menu(menubar, tearoff = 0)# Configure Y Menu and commands
    menubar.add_cascade(label ='Y Axis Config.', menu = configure_y)
    y_label = Menu(menubar, tearoff=0) # SubMenu
    y_label.add_command(label='Text', command=lambda:config_y('text'))
    y_label.add_command(label='Color', command=lambda:config_y('color'))
    y_label.add_command(label='Font Size', command=lambda:config_y('fontsize'))
    configure_y.add_cascade(label='Y Axis Label', menu=y_label)
    configure_y.add_separator()
    configure_y.add_command(label ='Y Tick Label Color',  command=lambda:config_y('tick color'))
    configure_y.add_separator()
    configure_y.add_command(label ='Y Tick Label Font Size',  command=lambda:config_y('tick fontsize'))
    configure_y.add_separator()
    style4 = Menu(menubar, tearoff=0) # SubMenu
    style4.add_command(label='Linear', command=lambda:config_y('linear'))
    style4.add_command(label='Log', command=lambda:config_y('log'))
    style4.add_command(label='SymLog', command=lambda:config_y('symlog'))
    configure_y.add_command(label ='Y Axis Scale', command=lambda:config_y('y limits'))
    configure_y.add_separator()
    configure_y.add_cascade(label='Y Axis Scale Style', menu=style4)
    configure_y.add_separator()
    root.config(menu = menubar)
    Test.test_menu()# Test Menu
    set_defaults()
root.mainloop()    


