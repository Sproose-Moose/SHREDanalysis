import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from SHRED import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import openpyxl
import numexpr as nx
from pandastable import Table
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
#Project SHRED 2024
#Author: (c) Seth Gerow, Embry-Riddle Aeronautical University
#email: gerows@my.erau.edu
#This is the second generation of the SHRED data analysis app. It is a tkinter GUI which imports a Micaplex wind tunnel excel file and display the data in a table. It then provides options for creating plots and exporting data and analysis to a text or excel file.

#Building the GUI application
root = tk.Tk()
root.title('SHRED Analysis MK2')
root.geometry('1080x720')
root.resizable(width='False', height='False') #stops the app or user from resizing this is temporary as I build the GUI

#building frames for the GUI
tree_frame = ttk.Frame(root)
tree_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

#Frame on the right for buttons and selections
button_frame = ttk.Frame(tree_frame, relief='sunken')
button_frame.place(relx=0.68, rely=0.02, relwidth=0.3, relheight=0.6)

# define columns and headings
colnames = ['Type', 'Units', 'Time', 'Z Encoder', 'Yaw', 'WAFBC Drag', 'WAFBC Side',
       'WAFBC Lift', 'WAFBC Roll', 'WAFBC Pitch', 'WAFBC Yaw', 'WAFMC Drag',
       'WAFMC Side', 'WAFMC Lift', 'WAFMC Roll', 'WAFMC Pitch', 'WAFMC Yaw',
       'BAFMC Axial', 'BAFMC Side', 'BAFMC Normal', 'BAFMC Roll',
       'BAFMC Pitch', 'BAFMC Yaw', 'DPT250', 'DPT251', 'PT250', 'TE250',
       'Velocity', 'Dynamic Pressure', 'Mach', 'Reynolds Number per ft',
       'Velocity Setpoint', 'Temperature Setpoint', 'cRIO AI0', 'cRIO AI1',
       'cRIO AI2', 'cRIO AI3', 'Drag (raw)']
columns = []
for i in range(0, len(colnames)):
    columns.append(i)
    
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

for i in range(1,len(colnames)):
    tree.heading(i-1, text=colnames[i])

tree.column('0', stretch=False)

#adding the treeview
tree.place(relx=0.02, rely=0.65, relwidth=0.95, relheight=0.30)

#Button Panel Items
#Button Actions
def load_file(): #this function is for the choose file button which allows a user to select a file to read and it reads and returns the 
    f_in = filedialog.askopenfilename( filetypes = [ ( 'Excel', '.xlsx' ) ])  # Change to appropriate extension.
    if len( f_in ) > 0:
        global filedata
        filedata = importnewdata(f_in)
        data=[]
        for i in tree.get_children():
            tree.delete(i)
        for i in range(0, len(filedata)-1):
            data.append(filedata.iloc[[i],1:].values.tolist())
            tree.insert('',tk.END, values=data[i][0])
def clear_table():
    for i in tree.get_children():
        tree.delete(i)

buttonlbl = ttk.Label(button_frame, text = 'Data Manipulation Tools')
buttonlbl.place(relx=0.5, rely=0.04, anchor = 'center')
selectbtn = ttk.Button(button_frame, text = 'Select Data', command = load_file)
selectbtn.place(relx=0.5, rely=0.1, anchor = 'center')
clrbutton = ttk.Button(button_frame, text = 'Clear Table', command = clear_table)
clrbutton.place(relx=0.25, rely=0.94, anchor = 'center')

expbutton = ttk.Button(button_frame, text = 'Export')
expbutton.place(relx=0.15, rely=0.14)
savechkbutton = ttk.Checkbutton(button_frame, text = 'Save as New Sheet')
savechkbutton.place(relx=0.45, rely=0.15)

# add a scrollbar
scrollbary = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbary.place(relx=0.97, rely=0.65, width=25, relheight=0.30)
tree.configure(yscrollcommand=scrollbary.set)

scrollbarx = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
scrollbarx.place(relx=0.02, rely=0.95, relwidth=0.95, height=25)
tree.configure(xscrollcommand=scrollbarx.set)

#add in plots
plot_frame = ttk.Frame(tree_frame, relief='sunken')
plot_frame.place(relx=0.02, rely=0.02, relwidth=0.64, relheight=0.6)


#Axes Options
xselectlabel = ttk.Label(button_frame, text='X-Axis')
xselectlabel.place(relx=0.25, rely=0.3, anchor='center')
yselectlabel = ttk.Label(button_frame, text='Y-Axis')
yselectlabel.place(relx=0.75, rely=0.3, anchor='center')
yaxisselect = tk.Listbox(button_frame, selectmode=tk.MULTIPLE, exportselection=0)
yaxisselect.place(relx=0.6, rely=0.35, relwidth=0.30, relheight=0.25)
xaxisselect = tk.Listbox(button_frame, selectmode=tk.MULTIPLE, exportselection=0)
xaxisselect.place(relx=0.1, rely=0.35, relwidth=0.30, relheight=0.25)
vslabel = tk.Label(button_frame, text='vs.')
vslabel.place(relx=0.5, rely=0.47, anchor='center')

#creates selections for x and y axes
for i in range(1,len(colnames)-1):
    xaxisselect.insert(i+1, colnames[i+1])
    yaxisselect.insert(i+1, colnames[i+1])

#plotting function
def create():
    global frame
    global filedata
    frame = ttk.Frame(plot_frame, relief='sunken')
    frame.place(relx=0,rely=0,relwidth=1,relheight=1)
    mainfig = Figure(figsize = (5, 5), dpi = 100)
    #print(xaxisselect.curselection()[0])
    x = filedata.iloc[1:,xaxisselect.curselection()[0]+2]
    y = filedata.iloc[1:,yaxisselect.curselection()[0]+2]
    plot = mainfig.add_subplot(111)
    plot.scatter(x,y)
    canvas = FigureCanvasTkAgg(mainfig, frame)
    canvas.draw
    canvas.get_tk_widget().pack()
def clear():
    global frame
    frame.destroy()
    frame.pack_forget()

#plot button
pltbutton = ttk.Button(button_frame, text = 'Plot', command=create)
pltbutton.place(relx=0.5, rely=0.65, anchor='center')
pltclrbutton = ttk.Button(button_frame, text = 'Clear Plot',command=clear)
pltclrbutton.place(relx=0.75, rely=0.94, anchor = 'center')

#run the application
root.mainloop()