import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import openpyxl
import numexpr as nx
from pandastable import Table

#telling pandas to display 1000 characters in the command window allows me to view more of the chart when I print to command
pd.set_option('display.width', 1000)

#master is the tkinter app and master attributes describe the total app setup
master = Tk()
master.title("Shred Data Analysis")
master.resizable(width='False', height='False') #stops the app or user from resizing this is temporary as I build the GUI
master.geometry('1000x700') #width x height 720 is the max height, if you increase beyond that on my laptop it will reset to smallest size


mainframe = Frame(master, bg='#F2B33D')
mainframe.columnconfigure([0,1,2,3,4], minsize='200')
mainframe.pack()
ttk.Label(mainframe, text="Project SHRED Phase 3 Data Analysis Tool").grid(row=0, column=1, columnspan=3, sticky='n')
ttk.Label(mainframe, text="Column 1").grid(row=1,column=0)
ttk.Label(mainframe, text="Column 2").grid(row=1,column=1)
ttk.Label(mainframe, text="Column 3").grid(row=1,column=2)
ttk.Label(mainframe, text="Column 4").grid(row=1,column=3)
ttk.Label(mainframe, text="Column 5").grid(row=1,column=4)
          
tableframe = ttk.Frame(mainframe, padding="3 3 3 3", borderwidth=2, relief='sunken')
tableframe.grid(column=0, row=2, columnspan=2, sticky='ew')
ttk.Label(tableframe, text="tableframe", anchor='n').pack()

graphframe = ttk.Frame(mainframe, padding="3 3 3 3", borderwidth=2, relief='sunken')
graphframe.grid(column=2, row=2, columnspan=2, sticky='ew')
ttk.Label(graphframe, text="graphframe", anchor='n').pack()

#buttonframe = ttk.Frame(mainframe, height=300, width=300, padding="3 3 3 3", borderwidth=2, relief='sunken')
#buttonframe.grid(column=0, row=1)
#ttk.Label(buttonframe, text="button")

#these are some of the elements of the app
#data = Text(mainframe, state="disabled", width="50", height="20", wrap="none")
#ys = ttk.Scrollbar(mainframe, orient = 'vertical', command = data.yview)
#xs = ttk.Scrollbar(mainframe, orient = 'horizontal', command = data.xview)
#data['yscrollcommand'] = ys.set
#data['xscrollcommand'] = xs.set
#data.grid(column = 0, row = 0, sticky = 'nwes')
#xs.grid(column = 0, row = 1, sticky = 'we')
#ys.grid(column = 1, row = 0, sticky = 'ns')

#these are the functions used
def getdate(df): #this function pulls the calendar day in format: month day, year from a Shred data excel file
    time = df.Time.str.split(pat=None,n=7,expand=False,regex=None)
    date = df.Time.get(1)
    date = date.split(" ")[0]
    year = int(date[0:2])+2000
    calendar = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month = calendar[int(date[3:4])-1]
    day = date[4:6]
    cal_date = (month + " " + str(day) + ", " + str(year))
    return date, cal_date
def normalizetime(df): #this function changes the timestamps from the imported data to a range starting at zero to be used for plots
    starttime = df.Time[1]
    starttime = (int(starttime[0:2])*3600) + (int(starttime[3:5])*60) + (int(starttime[6:8])) + (int(starttime[9:])/1000)
    for i in range(1,len(df)):
        time = df.Time[i]
        df.Time[i] = (int(time[0:2])*3600) + (int(time[3:5])*60) + (int(time[6:8])) + (int(time[9:])/1000)
        df.Time[i] = df.Time[i]-starttime
def importnewdata(filename): #this function reads a given file and formats it properly to be added to the databse
    nanvalue = float("NAN")
    df = pd.read_excel(filename)
    df.replace(0,nanvalue,inplace=True)
    df.dropna(axis=1, inplace=True)
    (date, cal_date) = getdate(df)
    df.Time = df.Time.str.removeprefix(date)
    df.Time = df.Time.str.removeprefix(" ")
    normalizetime(df)
    return df
def load_file(): #this function is for the choose file button which allows a user to select a file to read and it reads it
    f_in = filedialog.askopenfilename( filetypes = [ ( 'Excel', '.xlsx' ) ])  # Change to appropriate extension.
    if len( f_in ) > 0:
        filedata = importnewdata(f_in)
#        currentdisplay = data.get('1.0', 'end')
#        if len(currentdisplay) > 0:
#            data['state'] = 'normal'
#            data.delete('1.0', 'end')
#            data.insert('1.0', filedata)
#            data['state'] = 'disabled'
#        elif len(currentdisplay) == 0:
#            data['state'] = 'normal'
#            data.insert('1.0', filedata)
#            data['state'] = 'disabled'
        ptb = Table(mainframe, dataframe = filedata)
        ptb.grid(column=0, row = 2, columnspan=2, sticky='ew')
        ptb.show()
        #print( filedata )   # printed to the terminal for simplicity.
        return filedata
        
ttk.Button(mainframe, text="Choose File", command = load_file).grid(column=4, row=2)
#ttk.Label(mainframe, text="this is a program which will open an excel file and get the data from it").grid(column=4, row=3)

#the main loop loops these things over and over so that a permanent tab appears
master.mainloop()