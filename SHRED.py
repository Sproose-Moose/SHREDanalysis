#Project SHRED 2024
#Author: (c) Seth Gerow, Embry-Riddle Aeronautical University
#email: gerows@my.erau.edu
import pandas as pd

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
        
def importnewdata(filename):  #this function reads a given file and formats it properly to be added to the databse
    nanvalue = float("NAN")
    df = pd.read_excel(filename)
    df.replace(0,nanvalue,inplace=True)
    df.Yaw.replace(nanvalue, 0, inplace=True)
    df.dropna(axis=1, inplace=True)
    (date, cal_date) = getdate(df)
    df.Time = df.Time.str.removeprefix(date)
    df.Time = df.Time.str.removeprefix(" ")
    normalizetime(df)
    return df


        

        