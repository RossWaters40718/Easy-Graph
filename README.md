# Easy-Graph
Easy Matplotlib Graph For Windows.
Notes For End Users:
Matplotlib Graph For Windows Using tkagg Backend.
There Are Several Methods That May Be Used To Configure The Graph.
The Provided Menus Offer Almost All Properties For Configuration before
Executing Your Code From The Test Menu. Another Way Is To Setup All The
tk Variables Found In (set_defaults()) Before Runtime Or Setup These Variables
In Your Code And Then Calling (set_axes()) Prior To Drawing. You Will Find Some
Existing Functions That I Created Just To Make Things Easier To Change With
Code During Runtime. View The Examples Provided For These Functions. Of Course
You May Add More Functions Or Just Use Standard matplotlib Procedures For Change.
The Class (Test) Provides Place Holders For Test Menu Items And Test Code.
The X,Y Data For Plotting May Be In List Or Numpy Array Forms For Plotting.
I Haved Clocked The Loop Speed At Over 300 FPS Using List Data. There Exist Provided
Methods In The Test Class For Both Types Of Data Input. Hope Some Enjoys.
Have Any Questions View The Examples Inside The Test Class.
Required Imports:
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
