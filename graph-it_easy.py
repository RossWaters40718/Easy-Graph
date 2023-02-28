from win32api import GetMonitorInfo, MonitorFromPoint
from tkinter.filedialog import asksaveasfile, askopenfile
import tkinter as tk
from tkinter import StringVar, BooleanVar, simpledialog
from tkinter import font, Menu, colorchooser, messagebox
from tkfontchooser import askfont
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as pat
from numpy import random, arange, geomspace, linspace
from sympy import parse_expr
import configparser
import pathlib
import timeit
import os
#
class Test():
    def log(exe_style):# Example
        clear_graph()  # Always Call clear_graph() To Start Fresh.
        #////////////////////////////// These May Be Omitted If Prior Setup.
        if exe_style=='loop':set_title("X Scale = Log, Draw Style = Loop Update Using Lists (100 pts.)")
        elif exe_style=='instant':set_title("X Scale = Log, Draw Style = Instant Update Using Lists (100 pts.)")
        elif exe_style=='live':set_title("X Scale = Log, Draw Style = Live Update (100 pts.)")
        set_xlabel('Frequency In Hertz')
        set_xscale_style('log') # Always Set Scale Style Before Scale To Avoid Zero Error
        set_x_scale('20,20000')
        set_ylabel('Amplitude In dB')
        set_yscale_style('linear')
        set_y_scale('-10,10')
        #//////////////////////////////
        # Customize X and/or Y Asis Tick Labels And Locations Without affecting Limits
        # If X Values Are Changed, Y Must Also Be Sent Even If No Changes ('y',None,None).
        # If Y Values Are Changed, X Must Also Be Sent Even If No Changes ('x',None,None).
        x_locs=[20,50,100,200,500,1000,2000,5000,10000,20000]
        x_lbls=['20','50','100','200','500','1k','2k','5k','10k','20k']
        change_tick_labels('x',x_locs,x_lbls)# Change X Tick Labels And Locations
        change_tick_labels('y',None,None)# No Change Y Tick Labels And Locations
# ****************************** Plot 1 ******************************
        plt_num=1 # Make Sure To Set The Plot Number Even If Only One Plot Will Exist.
        #Set Plot 1 2DLine  Properties
        plt1_color='aqua'# Set The line2d Color
        plt1_style='solid'# Set The line2d Style
        plt1_width=1# Set The line2d Width
        # Present Your Lists Data Here Or Inside Loop
        x=geomspace(20.0,20000.0,num=100,endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
        y=random.uniform(low=-10.0,high=10.0,size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line2d,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
        if exe_style=='loop':
            frames=0
            t_0=timeit.default_timer()
            for i in arange(1,len(x)+1): # Start Should Always Be 1 With Stop At Length + 1
                line2d.set_data(x[:i],y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='instant':# Instantly Update Graph With List Data
            line2d.set_data(x,y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            frames=0
            t_0=timeit.default_timer()
            for i in range(0,len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='live': # Live Update
            x=geomspace(20.0,20000.0,num=100,endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
            y_data=random.uniform(low=-10.0,high=10.0,size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line2d,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
            frames=0
            t_0=timeit.default_timer()
            for i in arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x values (x_data[0]),(x_data[1]) And 2 y values (y_data[0]),(y_data[1]) 
                # Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line2d.set_data(x[:i+1],y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        legend1=pat.Patch(color=plt1_color,label='Plot 1')
        legend2=pat.Patch(color=plt1_color,label='FPS = '+fps)
        plt.legend(bbox_to_anchor=(0.995,1.15),frameon=0,facecolor=Graph_Color.get(),labelcolor='linecolor',
                fontsize=int(Legend_Fontsize.get()),framealpha=1,loc='upper left',handles=[legend1,legend2])
        canvas.draw()        
# ****************************** Plot 2 ******************************
        plt_num=2 # Make Sure To Set The Plot Number
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Place Your Data Here
        #Set Plot 2 2DLine  Properties
        plt2_color='yellow'# Set The line2d Color
        plt2_style='dotted'# Set The line2d Style
        plt2_width=2# Set The line2d Width
        x=geomspace(20.0,20000.0,num=100,endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
        y=random.uniform(low=-10.0,high=10.0,size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line2d,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
        if exe_style=='loop': # Loop Through Lists Data
            frames=0
            t_0=timeit.default_timer()
            for i in arange(1,len(x)+1): # Start Should Always Be 1 With Stop At Length + 1
                line2d.set_data(x[:i],y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='instant': # Instantly Update Graph With List Data
            line2d.set_data(x,y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            frames=0
            t_0=timeit.default_timer()
            for i in range(0,len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='live': # Incomming Data Inside Test Loop
            x_data=geomspace(20.0,20000.0,num=100,endpoint=True)# Cannot Be Zero! Use geospace or logspace For Logs
            y_data=random.uniform(low=-10.0,high=10.0,size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line2d,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
            frames=0
            t_0=timeit.default_timer()
            for i in arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x values (x_data[0]),(x_data[1]) And 2 y values (y_data[0]),(y_data[1]) 
                # Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line2d.set_data(x[:i+1],y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        legend3=pat.Patch(color=plt2_color,label='Plot 2')
        legend4=pat.Patch(color=plt2_color,label='FPS = '+fps)
        plt.legend(bbox_to_anchor=(0.995,1.15),frameon=0,facecolor=Graph_Color.get(),labelcolor='linecolor',
                fontsize=int(Legend_Fontsize.get()),framealpha=1,loc='upper left',handles=[legend1,legend2,legend3,legend4])
        canvas.draw()        
    def linear(exe_style):# Example
        clear_graph() # Always Call clear_graph() To Start Fresh.
        #////////////////////////////// These May Be Omitted If Prior Setup.
        if exe_style=='loop':set_title('X Scale = Linear, Draw Style = Loop Update Using Lists (100 pts.)')
        elif exe_style=='instant':set_title('X Scale = Linear, Draw Style = Instant Update Using Lists (100 pts.)')
        elif exe_style=='live':set_title('X Scale = Linear, Draw Style = Live Update (100 pts.)')
        set_xscale_style('linear') # Always Set Scale Style Before Scale
        set_x_scale('0.0,300.0')
        set_xlabel('Time In Milliseconds')
        set_ylabel('Current In Amperes')
        set_yscale_style('linear')
        set_y_scale('0,500')
        #//////////////////////////////
        # Change X and/or Y Asis Tick Labels Without affecting Limits
        x_locs=[0,30,60,90,120,150,180,210,240,270,300,]
        x_lbls=['0','30m','60m','90m','120m','150m','180m','210m','240m','270m','300m']
        change_tick_labels('x',x_locs,x_lbls)
        y_locs=[0,100,200,300,400,500]
        y_lbls=['0','100m','200m','300m','400m','500m']
        change_tick_labels('y',y_locs,y_lbls)
# ****************************** Plot 1 ******************************
        plt_num=1 # Make Sure To Set The Plot Number Even If Only One Plot Will Exist.
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Data Can Also Be Incomming X And Y Data From Test Equipment Or Sensors.
        # Place Your Lists Data Here
        #Set Plot 1 2DLine  Properties
        plt1_color='aqua'# Set The line2d Color
        plt1_style='solid'# Set The line2d Style
        plt1_width=1# Set The line2d Width
        x_data=linspace(0.0,500.0,num=100)# 100 linear x values 0.0 to 500
        y_data=random.uniform(low=0.0,high=500.0,size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line2d,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
        frames=0
        t_0=timeit.default_timer()
        if exe_style=='loop':
            for i in arange(1,len(x_data)+1): # Start Should Always Be 1 With Stop At Length + 1
                line2d.set_data(x_data[:i],y_data[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x_data[i-1],y_data[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='instant': # Instantly Update Graph With List Data
            line2d.set_data(x_data,y_data)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            # redraw just the points
            ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            frames=0
            t_0=timeit.default_timer()
            for i in range(0,len(x_data)): # Data For Saving To File
                newline=[plt_num,x_data[i],y_data[i],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='live':
            x_data=linspace(0.0,500.0,num=100)# 100 linear x values 0.0 to 500
            y_data=random.uniform(low=0.0,high=500.0,size=(100,))
            x,y=[],[]
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line2d,=ax.plot([],c=plt1_color,ls=plt1_style,lw=plt1_width)
            frames=0
            t_0=timeit.default_timer()
            for i in arange(100):# Range Must Be Predetermined If Using Loop
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x values (x_data[0]),(x_data[1]) And 2 y values (y_data[0]),(y_data[1]) 
                # Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line2d.set_data(x[:i+1],y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt1_color,plt1_style,plt1_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        legend1=pat.Patch(color=plt1_color,label='Plot 1')
        legend2=pat.Patch(color=plt1_color,label='FPS = '+fps)
        plt.legend(bbox_to_anchor=(0.995,1.15),frameon=0,facecolor=Graph_Color.get(),labelcolor='linecolor',
                fontsize=int(Legend_Fontsize.get()),framealpha=1,loc='upper left',handles=[legend1,legend2])
        canvas.draw()        
# ****************************** Plot 2 ******************************
        plt_num=2 # Set The Plot Number
        # Generate Data To Plot Here
        # Data Can Be 2 List. X Data List And Y Data List Or
        # Data Can Also Be Incomming X And Y Data From Test Equipment Or Sensors.
        #Set Plot 2 2DLine  Properties
        plt2_color='yellow'# Set The line2d Color
        plt2_style='dashed'# Set The line2d Style
        plt2_width=1# Set The line2d Width
        x=linspace(0.0,500.0,num=100)# 100 linear x values 0.0 to 500
        y=random.uniform(low=0.0,high=500.0,size=(100,))
        axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
        line2d,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
        frames=0
        t_0=timeit.default_timer()
        if exe_style=='loop':
            for i in arange(1,len(x)+1):
                line2d.set_data(x[:i],y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='instant': # Instantly Update Graph With np.array Data
            line2d.set_data(x,y)# Update The Artist
            fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
            ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
            fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
            frames=0
            t_0=timeit.default_timer()
            for i in range(0,len(x)): # Data For Saving To File
                newline=[plt_num,x[i],y[i],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        elif exe_style=='live':
            x_data=linspace(0.0,500.0,num=100)# 100 linear x values 0.0 to 500
            y_data=random.uniform(low=0.0,high=500.0,size=(100,))
            # Generate Your X,Y Data Here And Create Seperate List For X Data And Y Data As They Arrive.
            # Each Time The Lists Gets Inserted Or Appended, The List Data Will Be Executed Inside The Loop.
            # This Should Be Used For Live Update Type Plots.
            x,y=[],[]    
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line2d,=ax.plot([],c=plt2_color,ls=plt2_style,lw=plt2_width)
            frames=0
            t_0=timeit.default_timer()
            for i in arange(100):
                #////////////////////////////////////////////////////////    
                # Incomming Live Data From Sensors / Test Equip. etc...  
                # Retrieve New x,y Values Here And Place In x,y Lists
                # 2 x values (x_data[0]),(x_data[1]) And 2 y values (y_data[0]),(y_data[1]) 
                # Need To Be Present In Lists Before Loop Execution.
                x.insert(i,x_data[i])
                y.insert(i,y_data[i])
                #////////////////////////////////////////////////////////    
                line2d.set_data(x[:i+1],y[:i+1])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                newline=[plt_num,x[i-1],y[i-1],plt2_color,plt2_style,plt2_width]
                Plot_Data.append(str(newline))
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
                frames+=1
            t_1=timeit.default_timer()-t_0    
            fps=str(int(frames/t_1))
        legend3=pat.Patch(color=plt2_color,label='Plot 2')
        legend4=pat.Patch(color=plt2_color,label='FPS = '+fps)
        plt.legend(bbox_to_anchor=(0.995,1.15),frameon=0,facecolor=Graph_Color.get(),labelcolor='linecolor',
                fontsize=int(Legend_Fontsize.get()),framealpha=1,loc='upper left',handles=[legend1,legend2,legend3,legend4])
        canvas.draw()        
    def test_1():
        clear_graph()
        # Configure Graph Prior To Execution Using Menus
        load_plot_file("Plot_1.plt") # Or Configure Graph Here With Existing File
        #load_plot_file() # If File Name Doesn't Exist, askopenfile Dialog Will Appear.
        # Or Configure Graph Here With Code
        #////******* Place Data Aquisition Code Here *******\\\\#
        canvas.draw()        
    def test_2():
        clear_graph()
        #////******* Place Data Aquisition Code Here *******\\\\#
        canvas.draw()        
    def test_3():
        clear_graph()
        #////******* Place Data Aquisition Code Here *******\\\\#
        canvas.draw()        
    def test_4():
        clear_graph()
        #////******* Place Data Aquisition Code Here *******\\\\#
        canvas.draw()        
    def test_5():
        clear_graph()
        #////******* Place Data Aquisition Code Here *******\\\\#
        canvas.draw()        
    def test_menu():
        #////******* Here You Can Modify The Menu To Suit Your Needs *******\\\\#
        tst=Menu(menubar,background='aqua',foreground='black',tearoff=0)
        menubar.add_cascade(label ='Tests',menu=tst)
        tst.add_command(label ='Log Scale "Loop" Example',command=lambda:Test.log('loop'))
        tst.add_separator()
        tst.add_command(label ='Linear Scale "Live" Example',command=lambda:Test.linear('live'))
        tst.add_separator()
        tst.add_command(label ='Linear Scale "Instant" Example',command=lambda:Test.linear('instant'))
        tst.add_separator()
        tst.add_command(label ='Test 1 (Empty)',command=lambda:Test.test_1())
        tst.add_separator()
        tst.add_command(label ='Test 2 (Empty)',command=lambda:Test.test_2())
        tst.add_separator()
        tst.add_command(label ='Test 3 (Empty)',command=lambda:Test.test_3())
        tst.add_separator()
        tst.add_command(label ='Test 4 (Empty)',command=lambda:Test.test_4())
        tst.add_separator()
        tst.add_command(label ='Test 5 (Empty)',command=lambda:Test.test_5())
        tst.add_separator()
        root.config(menu=menubar)
class Init_Graph:
    def __init__(self,funct,exist=None,file_name=None):
        self.funct=funct
        self.exist=exist
        self.file_name=file_name
        if self.funct=='read' or self.funct=='write':
            dir=pathlib.Path(__file__).parent.absolute()
            filename='graph_it.ini' # Program ini file
            self.ini_path=os.path.join(dir,filename)
            if self.exist==None:
                if not os.path.exists(self.ini_path):
                    set_defaults()
                    return
        config=configparser.ConfigParser()
        def read_ini_data():
            if self.funct=='read':
                dir=pathlib.Path(__file__).parent.absolute()
                filename='graph_it.ini' # Program ini file
                self.ini_path=os.path.join(dir,filename)
                if self.exist==None:
                    if not os.path.exists(self.ini_path):set_defaults()
            elif self.funct=='load':
                if self.file_name==None:
                    types=[('Plot Files', '*.plt'),('Text Document', '*.txt'),('All Files', '*.*')] 
                    directory=askopenfile(mode='r',initialdir=GraphIt_Folder.get(),defaultextension=".plt",
                        filetypes=types)
                    if directory is None:return
                    else:self.ini_path=directory.name
                else:self.ini_path=os.path.join(path, self.file_name )
            config.read(self.ini_path)
            keys=["graph_color","viewport_color","title_color","major_color",
                "minor_color","x_color","xtick_color","y_color","ytick_color"]
            for key in keys:
                try:
                    value=config.get("COLORS",key)
                    if key=="graph_color":Graph_Color.set(value)
                    elif key=="viewport_color":Viewport_Color.set(value)
                    elif key=="title_color":Title_Color.set(value)
                    elif key=="major_color":Major_Color.set(value)
                    elif key=="minor_color":Minor_Color.set(value)
                    elif key=="x_color":X_Color.set(value)
                    elif key=="xtick_color":XTick_Color.set(value)
                    elif key=="y_color":Y_Color.set(value)
                    elif key=="ytick_color":YTick_Color.set(value)
                except configparser.NoOptionError:
                    pass
            config.read(self.ini_path)
            keys=["title","x_label","y_label"]
            for key in keys:
                try:
                    value=config.get("TEXT",key)
                    if key=="title":
                        ax.set_title(value)
                        Title.set(value)
                    elif key=="x_label":    
                        ax.set_xlabel(value)
                        X_Text.set(value)
                    elif key=="y_label":    
                        ax.set_ylabel(value)
                        Y_Text.set(value)
                except configparser.NoOptionError:
                    pass
            config.read(self.ini_path)
            keys=["major","minor","show_minor"]
            for key in keys:
                try:
                    value=config.get("GRID_STYLE",key)
                    if key=="major":Major_Style.set(value)
                    elif key=="minor":Minor_Style.set(value)    
                    elif key=="show_minor":
                        value=parse_expr(value,evaluate=False)
                        Show_Minor.set(value)    
                except configparser.NoOptionError:
                    pass
            config.read(self.ini_path)
            keys=["font family","title_fontsize","legend_fontsize","x_fontsize","xtick_fontsize",
                "y_fontsize","ytick_fontsize"]
            for key in keys:
                try:
                    value=config.get("FONT_SIZES",key)
                    if key=="font family":
                        family=parse_expr(value,evaluate=False)
                        ax.set_title(Title.get(),**family)
                        ax.set_xlabel(X_Text.get(),**family)
                        ax.set_ylabel(Y_Text.get(),**family)
                        Font_Family.set(value)
                    elif key=="title_fontsize":Title_Fontsize.set(value)
                    elif key=="legend_fontsize":Legend_Fontsize.set(value)
                    elif key=="x_fontsize":X_Fontsize.set(value)
                    elif key=="xtick_fontsize":XTick_Fontsize.set(value)
                    elif key=="y_fontsize":Y_Fontsize.set(value)
                    elif key=="ytick_fontsize":YTick_Fontsize.set(value)
                except configparser.NoOptionError:
                    pass
            config.read(self.ini_path)
            keys=["x_style","x_scale","y_style","y_scale"]
            for key in keys:
                try:
                    value=config.get("SCALE_STYLES",key)
                    if key=="x_style":X_Style.set(value)
                    elif key=="x_scale":X_Scale.set(value)
                    elif key=="y_style":Y_Style.set(value)
                    elif key=="y_scale":Y_Scale.set(value)
                except configparser.NoOptionError:
                    pass
            config.read(self.ini_path)
            keys=["x","y","state","width","height"]
            for key in keys:
                try:
                    value=config.get("WINDOW",key)
                    if key=="x":x=float(value)
                    elif key=="y":y=float(value)
                    elif key=="state":root.state(value)
                    elif key=="width":width=float(value)    
                    elif key=="height":height=float(value)    
                except configparser.NoOptionError:
                    pass
            if funct=='load':# Place Data In List
                try:
                    Plot_Data.clear()
                    config.read(self.ini_path)
                    for key,value in config.items('LINE_DATA'):# Check For x,y Data
                        index=parse_expr(value)
                        Plot_Data.append(index)
                except Exception:
                    pass
            root.geometry('%dx%d+%d+%d' % (width,height,x,y))
            root.update()
            X_Tick_Lbls.set('')# Only Use Default Tick Labels/Locations For Load 
            X_Tick_Locs.set('')
            Y_Tick_Lbls.set('')
            Y_Tick_Locs.set('')
            set_axes()
        def write_ini_data():
            if self.funct=='write':
                dir=pathlib.Path(__file__).parent.absolute()
                filename='graph_it.ini' # Program ini file
                self.ini_path=os.path.join(dir,filename)
                if self.exist==None:
                    if not os.path.exists(self.ini_path):set_defaults()
            elif self.funct=='save':
                types=[('Plot Files', '*.plt'),('Text Document', '*.txt'),('All Files', '*.*')] 
                directory=asksaveasfile(initialdir=GraphIt_Folder.get(),
                    defaultextension=".plt",filetypes=types)     
                if directory is None:return
                else: self.ini_path=directory.name
            config=configparser.ConfigParser()
            config.read(self.ini_path)
            try:
                config.add_section("COLORS")
            except configparser.DuplicateSectionError:
                pass
            config.set("COLORS", "graph_color", Graph_Color.get())
            config.set("COLORS", "viewport_color", Viewport_Color.get())
            config.set("COLORS", "title_color", Title_Color.get())
            config.set("COLORS", "major_color", Major_Color.get())
            config.set("COLORS", "minor_color", Minor_Color.get())
            config.set("COLORS", "x_color", X_Color.get())
            config.set("COLORS", "xtick_color", XTick_Color.get())
            config.set("COLORS", "y_color", Y_Color.get())
            config.set("COLORS", "ytick_color", YTick_Color.get())
            try:
                config.add_section("TEXT")
            except configparser.DuplicateSectionError:
                pass
            if exist!='keep':# Keep Default .ini Values 
                config.set("TEXT", "title", Title.get())
                config.set("TEXT", "x_label", X_Text.get())
                config.set("TEXT", "y_label", Y_Text.get())
                try:
                    config.add_section("GRID_STYLE")
                except configparser.DuplicateSectionError:
                    pass
            config.set("GRID_STYLE", "major", Major_Style.get())
            config.set("GRID_STYLE", "minor", Minor_Style.get())
            status=str(Show_Minor.get())
            config.set("GRID_STYLE", "show_minor", status)
            try:
                config.add_section("FONT_SIZES")
            except configparser.DuplicateSectionError:
                pass
            config.set("FONT_SIZES", "font family", Font_Family.get())
            config.set("FONT_SIZES", "title_fontsize", Title_Fontsize.get())
            config.set("FONT_SIZES", "legend_fontsize", Legend_Fontsize.get())
            config.set("FONT_SIZES", "x_fontsize", X_Fontsize.get())
            config.set("FONT_SIZES", "xtick_fontsize", XTick_Fontsize.get())
            config.set("FONT_SIZES", "y_fontsize", Y_Fontsize.get())
            config.set("FONT_SIZES", "ytick_fontsize", YTick_Fontsize.get())
            try:
                config.add_section("SCALE_STYLES")
            except configparser.DuplicateSectionError:
                pass
            if exist!='keep':# Keep Default .ini Values 
                config.set("SCALE_STYLES", "x_style",X_Style.get())
                config.set("SCALE_STYLES", "x_scale", X_Scale.get())
                config.set("SCALE_STYLES", "y_style", Y_Style.get())
                config.set("SCALE_STYLES", "y_scale", Y_Scale.get())
                try:
                    config.add_section("WINDOW")
                except configparser.DuplicateSectionError:
                    pass
            if root.state()=='normal':
                config.set("WINDOW", "x", str(root.winfo_x()))
                config.set("WINDOW", "y", str(root.winfo_y()))
                config.set("WINDOW", "state", str(root.state()))
                config.set("WINDOW", "width", str(root.winfo_width()))
                config.set("WINDOW", "height", str(root.winfo_height()))
            if Plot_Data and self.funct=='save':
                try:
                    config.add_section("LINE_DATA")
                except configparser.DuplicateSectionError:
                    pass
                for i, item in enumerate(Plot_Data):
                    config.set("LINE_DATA", str(i), item)
            with open(self.ini_path, 'w') as configfile:
                config.write(configfile)
        if funct=='read' or funct=='load':read_ini_data()        
        elif funct=='write' or funct=='save':write_ini_data()
def open_plot_file():
    path=askopenfile(mode='r',initialdir=GraphIt_Folder.get(),defaultextension=".plt",
        filetypes=[("PLT","*.plt"),("TXT","*.txt")])
    if path is None:return
    os.popen("notepad "+path.name).read()
def load_plot_file(file_name=None):
    if file_name==None:Init_Graph('load')# Write Properties To File
    else:Init_Graph('load',None,file_name)# Write Properties To File
    if not Plot_Data:return
    t_num,p_num=0,0
    num_plts,start_index,end_index=[],[],[]
    for i in arange(0,len(Plot_Data)):# Get Number Of Plots And Set Start Points
        t_num=Plot_Data[i][0]
        if t_num>p_num:# Next Plot Number
            p_num=t_num
            num_plts.append(p_num)
            start_index.append(i)
    if len(num_plts)==1:end_index.append(len(Plot_Data))# Index 0
    else:
        if len(num_plts)>=2:# Set The End Points Of Each Plot
            for i in arange(0,len(num_plts)-1):        
                end_index.append(start_index[i+1])        
                if i==len(num_plts):end_index.append(len(Plot_Data))
            end_index.append(len(Plot_Data))# Final End Point     
    if len(num_plts)>=1:
        for p in arange(1,len(num_plts)+1):
            if p==1:index=0
            x,y=[],[]
            color=Plot_Data[index][3]# Set The line2d Color
            style=Plot_Data[index][4]# Set The line2d Style
            width=Plot_Data[index][5]# Set The line2d Width
            for i in arange(start_index[p-1],end_index[p-1]):
                x.append(Plot_Data[index][1])
                y.append(Plot_Data[index][2])
                index+=1
            axbackground=fig.canvas.copy_from_bbox(ax.bbox) # Get Copy Of Everything Inside fig.bbox
            line2d,=ax.plot([],c=color,ls=style,lw=width)
            i=0
            if p==1:a=1
            else:a=0
            for i in arange(start_index[p-1],end_index[p-1]+a):
                line2d.set_data(x[:i],y[:i])# Update The Artist
                fig.canvas.restore_region(axbackground)# Reset Background To Copy Of fig.bbox
                ax.draw_artist(line2d)# Draw The Animated Artist (points) From The cached Renderer
                fig.canvas.blit(ax.bbox)# Renderer To The GUI Framework For Visualization
                fig.canvas.flush_events()# Flush Pending Events And Re-paint Canvas
            canvas.draw()
def destroy():# X Icon Was Clicked Or File/Exit
    Plot_Data.clear()
    Init_Graph('write','keep')
    for widget in root.winfo_children():
        if isinstance(widget,tk.Canvas):widget.destroy()
        else: widget.destroy()
        os._exit(0)
    return
def help():
    dir=pathlib.Path(__file__).parent.absolute()
    filename='graph-it_help.txt' # Program help file
    help_path=os.path.join(dir,filename)
    exist=os.path.exists(help_path)
    if exist:os.popen("notepad "+help_path).read()
    else:
        msg='Help File Not Found!'
        msg2='\nPlease Include graph-it_help.txt In Your Application Path.'
        messagebox.showerror("<graph-it_help>",msg+msg2)
def about():
    messagebox.showinfo('About Graph-It Easy', 'Creator: Ross Waters\nEmail: RossWatersjr@gmail.com'\
        '\nLanguage: Python version 3.11.2 64-bit'\
        '\nProgram: graph-it_easy.py Created Using\ntkinter version 8.6,\nmatplotlib version 3.6.2'\
        '\nRevision \ Date: 1.2.2 \ 02/28/2023'\
        '\nCreated For Windows 10/11')
def config_g(which): # Configure Graph Menu
    if which=='graph color':        
        color_code=colorchooser.askcolor(title ="Choose Graph Color",initialcolor=Graph_Color.get())
        if color_code[1]==None:return
        Graph_Color.set(color_code[1])
        fig.patch.set_facecolor(Graph_Color.get())# Set the Figure Facecolor
    elif which=='font family':
        name=parse_expr(Font_Family.get(),evaluate=False)
        plt.rcParams.update({'font.family': name['fontname'][-1]})
        sample='Only Select Font Family!'
        new_font=askfont(root,text=sample,title="Choose Graph Font Family" ,family=name['fontname'][-1],
            size=14,weight='normal',slant='roman')
        if new_font=='' or new_font==None:return
        new_font['family']=new_font['family'].replace('\\', '')
        plt.rcParams.update({'font.family': new_font['family']})
        family={'fontname':plt.rcParams["font.family"]}
        Font_Family.set(str(family))
        ax.set_title(Title.get(),**family,ha='center',color=Title_Color.get(),
            fontsize=int(Title_Fontsize.get()),weight='normal',style='italic')
        ax.set_xlabel(X_Text.get(),**family,ha='center',color=X_Color.get(),
            fontsize=int(X_Fontsize.get()),weight='normal',style='italic')
        ax.set_ylabel(Y_Text.get(),**family,ha='center',color=Y_Color.get(),
            fontsize=int(Y_Fontsize.get()),weight='normal',style='italic')
    elif which=='viewport color':        
        color_code=colorchooser.askcolor(title ="Choose Viewport Color",initialcolor=Viewport_Color.get())
        if color_code[1]==None:return
        Viewport_Color.set(color_code[1])
        ax.set_facecolor(Viewport_Color.get())# Set the Graph Facecolor
    elif which=='text':        
        txt=simpledialog.askstring("<Graph Title Text>","Enter Text To Display For Graph Title.",
            parent=root,initialvalue=Title.get())
        if txt==''or txt==None:return
        set_title(txt)
    elif which=='legends':
        size=simpledialog.askinteger("<Graph Legend Font Size>","Enter Font Size To Display For Graph Legends.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=Legend_Fontsize.get())
        if size is None:return
        Legend_Fontsize.set(size)
    elif which=='color':
        color_code=colorchooser.askcolor(title ="Choose Title Color",initialcolor=Title_Color.get())
        if color_code[1]==None:return
        ax.set_title(Title.get(),ha='center',color=color_code[1],
            fontsize=int(Title_Fontsize.get()),weight='normal',style='italic')
        Title_Color.set(color_code[1])
    elif which=='fontsize':
        size=simpledialog.askinteger("<Graph Title Fontsize>","Enter Font Size To Display For Graph Title.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=int(Title_Fontsize.get()))
        if size is None:return
        ax.set_title(Title.get(),ha='center',color=Title_Color.get(),
        fontsize=size,weight='normal',style='italic')
        Title_Fontsize.set(str(size))
    elif which=='show minor':
        if Show_Minor.get():
            msg='Turn "Off" Graph Minor Grid Lines?'
        else:msg='Turn "On" Graph Minor Grid Lines?'
        answer=messagebox.askyesno("Show Minor Ticks",msg)
        if answer==True and Show_Minor.get():
            Show_Minor.set(False)
            plt.minorticks_off()
        elif answer==True and not Show_Minor.get():
            Show_Minor.set(True)
            plt.minorticks_on()
        elif answer==False:return    
    elif which=='major color':        
        color_code=colorchooser.askcolor(title ="Choose Major Grid Line Color",initialcolor=Major_Color.get())
        if color_code[1]==None:return
        Major_Color.set(color_code[1])
        ax.grid(which='major',color=Major_Color.get(),linestyle='solid')
        ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get()) 
    elif which=='minor color':        
        color_code=colorchooser.askcolor(title ="Choose Minor Grid Line Color",initialcolor=Major_Color.get())
        if color_code[1]==None:return
        Minor_Color.set(color_code[1])
        ax.grid(which='minor',color=Minor_Color.get(),linestyle='solid') 
        ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get()) 
    # Major Grid Lines
    elif which=='major style solid':
        Major_Style.set('solid')
        ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get()) 
    elif which=='major style dotted':
        Major_Style.set('dotted')
        ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get()) 
    elif which=='major style dashed':
        Major_Style.set('dashed')
        ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get()) 
    elif which=='major style dashdot':
        Major_Style.set('dashdot')
        ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get())
    # Minor Grid Lines
    elif which=='minor style solid':
        Minor_Style.set('solid')
        ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get()) 
    elif which=='minor style dotted':
        Minor_Style.set('dotted')
        ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get()) 
    elif which=='minor style dashed':
        Minor_Style.set('dashed')
        ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get()) 
    elif which=='minor style dashdot':
        Minor_Style.set('dashdot')
        ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get())
    elif which=='clear':
        clear_graph()
    fig.canvas.draw()
def config_x(which): # Configure X Axis Menu
    if which=='text':
        txt=simpledialog.askstring("<X Label Text>","Enter Text To Display For X Label.",
            parent=root,initialvalue='X Label')
        if txt==''or txt==None:return
        X_Text.set(txt)
    elif which=='fontsize':        
        size=simpledialog.askinteger("<X Label Fontsize>","Enter Font Size To Display For X Label.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=int(X_Fontsize.get()))
        if size is None:return
        X_Fontsize.set(str(size))
    elif which=='color':        
        color_code=colorchooser.askcolor(title ="Choose X Label Text Color",initialcolor=X_Color.get())
        if color_code[1]==None:return
        X_Color.set(color_code[1])
    elif which=='tick fontsize':        
        size=simpledialog.askinteger("<X Tick Labels Fontsize>","Enter Font Size To Display For X Tick Labels.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=int(XTick_Fontsize.get()))
        if size is None:return
        XTick_Fontsize.set(str(size))
        ax.tick_params(axis='x',which='major',labelsize=int(XTick_Fontsize.get()))
    elif which=='tick color':        
        color_code=colorchooser.askcolor(title ="Choose X Tick Label Color",initialcolor=XTick_Color.get())
        if color_code[1]==None:return
        XTick_Color.set(color_code[1])
        ax.tick_params(axis='x',colors=XTick_Color.get()) # Grid And Label The Axis Ticks
    elif which=='linear' or which=='log' or which=='symlog':
        set_xscale_style(which)
    elif which=='x limits':
        x=simpledialog.askstring("<X Axis Scale>","Set X Axis Scale 'Left, Right'. Example: 0.0, 10.0",
            parent=root,initialvalue=X_Scale.get())
        set_x_scale(x)    
        return    
    ax.set_xlabel(X_Text.get(),ha='center',color=X_Color.get(),
        fontsize=int(X_Fontsize.get()),weight='normal',style='italic')
    fig.canvas.draw()
def config_y(which): # Configure Y Axis Menu
    if which=='text':
        txt=simpledialog.askstring("<Y Label Text>","Enter Text To Display For Y Label.",
            parent=root,initialvalue='Y Label')
        if txt==''or txt==None:return
        Y_Text.set(txt)
    elif which=='fontsize':        
        size=simpledialog.askinteger("<Y Label Fontsize>","Enter Font Size To Display For Y Label.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=int(Y_Fontsize.get()))
        if size is None:return
        Y_Fontsize.set(str(size))
    elif which=='color':        
        color_code=colorchooser.askcolor(title ="Choose Y Label Text Color",initialcolor=Y_Color.get())
        if color_code[1]==None:return
        Y_Color.set(color_code[1])
    elif which=='tick fontsize':        
        size=simpledialog.askinteger("<Y Tick Labels Fontsize>","Enter Font Size To Display For Y Tick Labels.",
            parent=root,minvalue=6,maxvalue=32,initialvalue=int(YTick_Fontsize.get()))
        if size is None:return
        YTick_Fontsize.set(str(size))
        ax.tick_params(axis='y',which='major',labelsize=int(YTick_Fontsize.get()))
    elif which=='tick color':        
        color_code=colorchooser.askcolor(title ="Choose Y Tick Label Color",initialcolor=YTick_Color.get())
        if color_code[1]==None:return
        YTick_Color.set(color_code[1])
        ax.tick_params(axis='y',colors=YTick_Color.get()) # Grid And Label The Axis Ticks
    elif which=='linear' or which=='log' or which=='symlog':
        set_yscale_style(which)
    elif which=='y limits':
        y=simpledialog.askstring("<Y Axis Scale>","Set Y Axis Scale 'Bottom, Top'. Example: 0.0, 10.0",
            parent=root,initialvalue=Y_Scale.get())
        set_y_scale(y)
    ax.set_ylabel(Y_Text.get(),ha='center',color=Y_Color.get(),
        fontsize=int(Y_Fontsize.get()),weight='normal',style='italic')
    fig.canvas.draw()
def clear_graph(): # Gets Things Ready For New Plot Sequence
    Plot_Data.clear()
    ax.cla()
    set_axes()
def set_title(txt):
    family=Font_Family.get()
    family=parse_expr(Font_Family.get(),evaluate=False)
    ax.set_title(txt,**family,ha='center',color=Title_Color.get(),
        fontsize=int(Title_Fontsize.get()),weight='normal',style='italic')
    Title.set(txt)    
def set_xlabel(txt):
    family=Font_Family.get()
    family=parse_expr(Font_Family.get(),evaluate=False)
    ax.set_xlabel(txt,**family,ha='center',color=X_Color.get(),
        fontsize=int(X_Fontsize.get()),weight='normal',style='italic')
    X_Text.set(txt)
def set_ylabel(txt):
    family=Font_Family.get()
    family=parse_expr(Font_Family.get(),evaluate=False)
    ax.set_ylabel(txt,**family,ha='center',color=Y_Color.get(),
        fontsize=int(Y_Fontsize.get()),weight='normal',style='italic')
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
def delay(sec):
    t1=0
    t0=timeit.default_timer()
    while t1<=sec:t1=timeit.default_timer()-t0
def change_tick_labels(axis,locs=None,lbls=None):# Changes X-Y Axis Tick Labels Without affecting Limits
    if axis=='x':
        if locs is None:    
            X_Tick_Locs.set('')
            X_Tick_Lbls.set('')
        else:    
            ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())        
            plt.xticks(locs, lbls)
            X_Tick_Locs.set(str(locs))
            X_Tick_Lbls.set(str(lbls))
            global X_Labels
            global X_Locations
            X_Labels=[item.get_text() for item in ax.get_xticklabels()]
            X_Locations=ax.get_xticks()
            ax.set_xticklabels(X_Labels)
            ax.set_xticks(X_Locations)
            fig.canvas.draw()
            fig.canvas.flush_events()
            delay(0.2)# Give Time To Update New locs,labels
    elif axis=='y':
        if locs is None:    
            Y_Tick_Locs.set('')
            Y_Tick_Lbls.set('')
        else:    
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())        
            plt.yticks(locs, lbls)
            Y_Tick_Locs.set(str(locs))
            Y_Tick_Lbls.set(str(lbls))
            global Y_Labels
            global Y_Locations
            Y_Labels=[item.get_text() for item in ax.get_yticklabels()]
            Y_Locations=ax.get_yticks()
            ax.set_yticklabels(Y_Labels)
            ax.set_yticks(Y_Locations)
            fig.canvas.draw()
            fig.canvas.flush_events()
            delay(0.2)# Give Time To Update New locs,labels
def set_x_scale(x):# Argument is String value Of X1, X2. Example: "10.0, 100.0"         
    if x==None or x=='':return
    temp=str(x).replace('-','').replace(',','').replace(' ','').replace('.','') # Verify That All Are Numeric Values
    if temp.isdecimal():
        X_Scale.set(x)
        x=parse_expr(x,evaluate=False)
        if X_Style.get()!='linear':
            if x[0]<=0 or x[1]<=0: 
                msg='X Axis Scale "Log" Values Cannot Be Zero Or Less! Please Try Again.'
                messagebox.showerror("<X Axis Scale>",msg)
                return
        ax.set_xlim([float(x[0]),float(x[1])])
        fig.canvas.draw()
    else:
        msg='Something Is Incorrect With The X Axis Values Entered! Please Try Again.'
        messagebox.showerror("<X Axis Scale>",msg)
        return
def set_y_scale(y): # Argument is String value Of Y1, Y2. Example: "10.0, 100.0"            
    if y==None or y=='':return
    temp=str(y).replace('-','').replace(',','').replace(' ','').replace('.','') # Verify That All Are Numeric Values
    if temp.isdecimal():
        Y_Scale.set(y)
        y=parse_expr(y,evaluate=False)
        if Y_Style.get()!='linear':
            if y[0]<=0 or y[1]<=0: 
                msg='Y Axis Scale "Log" Values Cannot Be Zero Or Less! Please Try Again.'
                messagebox.showerror("<Y Axis Scale>",msg)
                return
        ax.set_ylim([float(y[0]),float(y[1])])
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
    x=parse_expr(X_Scale.get(),evaluate=False)
    ax.set_xlim([float(x[0]),float(x[1])])
    fig.patch.set_facecolor(Graph_Color.get())# Set the Graph Facecolor
    ax.set_facecolor(Viewport_Color.get())# Set the Graph Facecolor
    y=parse_expr(Y_Scale.get(),evaluate=False)
    ax.set_ylim([float(y[0]),float(y[1])])
    fig.add_axes(ax)        
    ax.tick_params(axis='x',colors=XTick_Color.get()) # Grid And Label The Axis Ticks
    ax.tick_params(axis='y',colors=YTick_Color.get())
    ax.tick_params(axis='x',which='major',labelsize=int(XTick_Fontsize.get()))
    ax.tick_params(axis='y',which='major',labelsize=int(YTick_Fontsize.get()))
    ax.grid(which='major',color=Major_Color.get(),linestyle=Major_Style.get()) # Turn Both Major and Minor Ticks On
    ax.grid(which='minor',color=Minor_Color.get(),linestyle=Minor_Style.get())
    name=parse_expr(Font_Family.get(),evaluate=False)
    plt.rcParams.update({'font.family':name['fontname'][-1]})
    family=parse_expr(Font_Family.get(),evaluate=False)
    ax.set_title(Title.get(),**family,ha='center',color=Title_Color.get(),
        fontsize=int(Title_Fontsize.get()),weight='normal',style='italic')
    ax.set_xlabel(X_Text.get(),**family,ha='center',color=X_Color.get(),
        fontsize=int(X_Fontsize.get()),weight='normal',style='italic')
    ax.set_ylabel(Y_Text.get(),**family,ha='center',color=Y_Color.get(),
        fontsize=int(Y_Fontsize.get()),weight='normal',style='italic')
    ax.autoscale_view(False,False,False)
    if X_Tick_Locs.get()!="" and X_Tick_Lbls.get()!="":change_tick_labels('x',X_Locations,X_Labels)
    if Y_Tick_Locs.get()!="" and Y_Tick_Lbls.get()!="":change_tick_labels('y',Y_Locations,Y_Labels)
    ax.format_coord = lambda x, y: 'x={:g}, y={:g}'.format(x, y)# Restore Mouse Coords.
    fig.canvas.draw()
    fig.canvas.flush_events()
    return
def set_defaults():# If No INI FILE Exist, Setup With tk Variables And Create File
    Graph_Color.set('#420021')
    Font_Family.set("{'fontname': ['Arial']}")
    Viewport_Color.set('#000024')
    Title_Color.set('#00ffff')
    Title_Fontsize.set('14')
    Title.set('Title Text')
    Major_Color.set('#808080')
    Minor_Color.set('#808080')
    Major_Style.set('solid')
    Minor_Style.set('dotted')
    Show_Minor.set('True')
    Legend_Fontsize.set('7')
    X_Color.set('#00ffff')
    XTick_Color.set('#ffffff')
    X_Tick_Lbls.set('')
    X_Tick_Locs.set('')
    X_Fontsize.set('12')
    XTick_Fontsize.set('8')
    X_Text.set('X Axis Text')
    X_Style.set('linear')
    X_Scale.set('0.0, 100.0')
    Y_Tick_Lbls.set('')
    Y_Tick_Locs.set('')
    Y_Color.set('#00ffff')
    YTick_Color.set('#ffffff')
    Y_Fontsize.set('12')
    YTick_Fontsize.set('8')
    Y_Text.set('Y Axis Text')
    Y_Style.set('linear')
    Y_Scale.set('-10.0, 10.0')
    x=(screen_width/2)-(root_wid/2)
    y=(screen_height/2)-(root_hgt/2)
    root.geometry('%dx%d+%d+%d' % (root_wid,root_hgt,x,y,))
    root.update()
    Init_Graph('write','pass')
    Init_Graph('read')
if __name__ == "__main__":
    root=tk.Tk()
    dir=pathlib.Path(__file__).parent.absolute()
    filename='graph-it.ico' # Program icon
    ico_path=os.path.join(dir, filename)
    root.iconbitmap(default=ico_path) # root and children
    root.font=font.Font(family='Lucida Sans',size=9,weight='normal',slant='italic')# Menu Font
    root.title('Graph-It Easy')
    monitor_info=GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area=monitor_info.get("Work")
    monitor_area=monitor_info.get("Monitor")
    screen_width=work_area[2]
    screen_height=work_area[3]
    taskbar_hgt=(monitor_area[3]-work_area[3])
    root.configure(bg='gray')
    root.option_add("*Font",root.font)
    root.protocol("WM_DELETE_WINDOW",destroy)
    fig=plt.figure(figsize=(10,10),facecolor='black',frameon=True,)
    ax=plt.axes()
    fig.add_axes(ax)
    canvas=FigureCanvasTkAgg(fig,master=root) # Create The Canvas
    toolbar=NavigationToolbar2Tk(canvas,root) # create Matplotlib toolbar
    tb_hgt=toolbar.winfo_reqheight()
    root_hgt=((screen_height-taskbar_hgt)/2.0)+tb_hgt 
    root_wid=root_hgt*2.0
    canvas.get_tk_widget().pack(fill='both',pady=(0,0)) # place Canvas and Toolbar on Tkinter window
    Plot_Data=[]
    Graph_Color=StringVar()
    GraphIt_Folder=StringVar()
    Font_Family=StringVar()
    Viewport_Color=StringVar()
    Title_Color=StringVar()
    Major_Color=StringVar()
    Minor_Color=StringVar()
    X_Color=StringVar()
    X_Labels=[]
    Empty_X_Lbls=[]
    X_Tick_Lbls=StringVar()
    X_Tick_Locs=StringVar()
    XTick_Color=StringVar()
    Y_Color=StringVar()
    Y_Labels=[]
    Empty_Y_Lbls=[]
    Y_Tick_Lbls=StringVar()
    Y_Tick_Locs=StringVar()
    YTick_Color=StringVar()
    Title_Fontsize=StringVar()
    X_Fontsize=StringVar()
    XTick_Fontsize=StringVar()
    Y_Fontsize=StringVar()
    YTick_Fontsize=StringVar()
    Title=StringVar()
    Major_Style=StringVar()
    Minor_Style=StringVar()
    Show_Minor=BooleanVar()
    X_Text=StringVar()
    X_Style=StringVar()
    X_Scale=StringVar()
    Y_Text=StringVar()
    Y_Style=StringVar()
    Y_Scale=StringVar()
    Legend_Fontsize=StringVar()
    menubar=Menu(root)# Create Menubar
    file=Menu(menubar,background='aqua',foreground='black',tearoff=0)# File Menu and commands
    menubar.add_cascade(label='File',menu=file)
    file.add_command(label='Open Plot File To View',command=lambda:open_plot_file())
    file.add_separator()
    file.add_command(label='Save Plot File As',command=lambda:Init_Graph('save'))
    file.add_separator()
    file.add_command(label='Load Plot File To Graph',command=lambda:load_plot_file())
    file.add_separator()
    file.add_command(label='Exit',command=lambda:destroy())
    file.add_separator()
    configure_g=Menu(menubar,background='aqua',foreground='black',tearoff=0)# Configure Graph Menu and commands
    menubar.add_cascade(label ='Configure Graph',menu=configure_g)
    configure_g.add_command(label='Graph Face Color',command=lambda:config_g('graph color'))
    configure_g.add_separator()
    configure_g.add_command(label='Graph Font Family',command=lambda:config_g('font family'))
    configure_g.add_separator()
    configure_g.add_command(label='Graph Legend Font Size',command=lambda:config_g('legends'))
    configure_g.add_separator()
    title=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    title.add_command(label='Text',command=lambda:config_g('text'))
    title.add_command(label='Color',command=lambda:config_g('color'))
    title.add_command(label='Font Size',command=lambda:config_g('fontsize'))
    configure_g.add_cascade(label='Graph Title',menu=title)
    configure_g.add_separator()
    configure_vp=Menu(menubar,background='aqua',foreground='black',tearoff=0)# Configure Viewport Menu and commands
    menubar.add_cascade(label='Configure Viewport',menu=configure_vp)
    configure_vp.add_command(label='Viewport Face Color',command=lambda:config_g('viewport color'))
    configure_vp.add_separator()
    configure_vp.add_command(label='Viewport Major Grid Line Color',command=lambda:config_g('major color'))
    configure_vp.add_separator()
    major=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    major.add_command(label='Solid',command=lambda:config_g('major style solid'))
    major.add_command(label='Dotted',command=lambda:config_g('major style dotted'))
    major.add_command(label='Dashed',command=lambda:config_g('major style dashed'))
    major.add_command(label='DashDot',command=lambda:config_g('major style dashdot'))
    configure_vp.add_cascade(label='Viewport Major Grid Line Style',menu=major)
    configure_vp.add_separator()
    configure_vp.add_command(label ='Viewport Minor Grid Line Color',command=lambda:config_g('minor color'))
    configure_vp.add_separator()
    minor=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    minor.add_command(label='Solid',command=lambda:config_g('minor style solid'))
    minor.add_command(label='Dotted',command=lambda:config_g('minor style dotted'))
    minor.add_command(label='Dashed',command=lambda:config_g('minor style dashed'))
    minor.add_command(label='DashDot',command=lambda:config_g('minor style dashdot'))
    configure_vp.add_cascade(label='Viewport Minor Grid Line Style',menu=minor)
    configure_vp.add_separator()
    configure_vp.add_command(label='Show Minor Grid Lines',command=lambda:config_g('show minor'))
    configure_vp.add_separator()
    configure_vp.add_command(label='Clear Viewport Data',command=lambda:config_g('clear'))
    configure_vp.add_separator()
    configure_x=Menu(menubar,background='aqua',foreground='black',tearoff=0)# Configure X Menu and commands
    menubar.add_cascade(label ='Configure X Axis',menu=configure_x)
    x_label=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    x_label.add_command(label='Text',command=lambda:config_x('text'))
    x_label.add_command(label='Color',command=lambda:config_x('color'))
    x_label.add_command(label='Font Size',command=lambda:config_x('fontsize'))
    configure_x.add_cascade(label='X Axis Label',menu=x_label)
    configure_x.add_separator()
    style_x=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    style_x.add_command(label='Linear',command=lambda:config_x('linear'))
    style_x.add_command(label='Log',command=lambda:config_x('log'))
    style_x.add_command(label='SymLog',command=lambda:config_x('symlog'))
    configure_x.add_command(label='X Axis Scale',command=lambda:config_x('x limits'))
    configure_x.add_separator()
    configure_x.add_cascade(label='X Axis Scale Style',menu=style_x)
    configure_x.add_separator()
    configure_x.add_command(label='X Tick Label Color',command=lambda:config_x('tick color'))
    configure_x.add_separator()
    configure_x.add_command(label='X Tick Label Font Size',command=lambda:config_x('tick fontsize'))
    configure_x.add_separator()
    configure_y=Menu(menubar,background='aqua',foreground='black',tearoff=0)# Configure Y Menu and commands
    menubar.add_cascade(label ='Configure Y Axis',menu=configure_y)
    y_label=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    y_label.add_command(label='Text',command=lambda:config_y('text'))
    y_label.add_command(label='Color',command=lambda:config_y('color'))
    y_label.add_command(label='Font Size',command=lambda:config_y('fontsize'))
    configure_y.add_cascade(label='Y Axis Label',menu=y_label)
    configure_y.add_separator()
    style_y=Menu(menubar,background='aqua',foreground='black',tearoff=0) # SubMenu
    style_y.add_command(label='Linear',command=lambda:config_y('linear'))
    style_y.add_command(label='Log',command=lambda:config_y('log'))
    style_y.add_command(label='SymLog',command=lambda:config_y('symlog'))
    configure_y.add_command(label ='Y Axis Scale',command=lambda:config_y('y limits'))
    configure_y.add_separator()
    configure_y.add_cascade(label='Y Axis Scale Style',menu=style_y)
    configure_y.add_separator()
    configure_y.add_command(label='Y Tick Label Color',command=lambda:config_y('tick color'))
    configure_y.add_separator()
    configure_y.add_command(label='Y Tick Label Font Size',command=lambda:config_y('tick fontsize'))
    configure_y.add_separator()
    Test.test_menu()# Create Test Menu
    configure_help=Menu(menubar,background='aqua',foreground='black',tearoff=0)# File Menu and commands
    menubar.add_cascade(label='Help',menu=configure_help)
    configure_help.add_command(label='Help',command=lambda:help())
    configure_help.add_separator()
    configure_help.add_command(label='About',command=lambda:about())
    configure_help.add_separator()
    root.config(menu=menubar)
    dir=os.path.expanduser( '~' )# Create Save Folder For .plt Files
    path=os.path.join(dir,'Graph-it Files', '' )
    GraphIt_Folder.set(path)
    if not os.path.isdir(GraphIt_Folder.get()):os.mkdir(path,mode = 0o666) #Read/Write
    Init_Graph('read') # Read And Initialize Properties           
root.mainloop()    


