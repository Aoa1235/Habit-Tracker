
from ClassPixel import Pixel

from datetime import datetime
from tkinter import *
from tkinter import messagebox

class PixelUI:

    #----------------------------------------- Tkinter UI ------------------------------------------#

    def __init__(self, pixel: Pixel) -> None:           #Main pixel window for adding to, deleting, or see the statistics of the pixel graph
        
        self.PixelUpdaterWindow = Tk()
        self.PixelUpdaterWindow.title("Pixel Graph Editor")
        self.PixelUpdaterWindow.config(padx=20, pady=20)
        
        #Graph Object

        #self.graph = Canvas()

        #pixel.getCurrentGraph()           #needs fixing

        # self.graphImage = PhotoImage(file=getCurrentGraph())
        # self.graph.create_image(100, 100, image=self.graphImage)
        # self.graph.grid(column=0, row=0)

        #Label Objects
        
        self.date = Label(text="Date:")
        self.amount = Label(text="Amount:")

        self.date.grid(row=1, column=0)
        self.amount.grid(row=2, column=0)

        #Dates - for placeholder in entry: https://stackoverflow.com/questions/27820178/how-to-add-placeholder-to-an-entry-in-tkinter

        self.dateYear = Entry(width=1)
        self.dateYear.insert(END, string="YYYY")
        self.dateYear.grid(row=1, column=5, sticky="NSEW")

        self.dateSlash1 = Label(text="/")
        self.dateSlash1.grid(row=1, column=2)

        self.dateMonth = Entry(width=3)
        self.dateMonth.insert(END, string="MM")
        self.dateMonth.grid(row=1, column=1, sticky="NSEW")

        self.dateSlash2 = Label(text="/")
        self.dateSlash2.grid(row=1, column=4)

        self.dateDay = Entry(width=3)
        self.dateDay.insert(END, string="DD")
        self.dateDay.grid(row=1, column=3, sticky="NSEW")

        #Amount to Increase

        self.defaultSpinboxVal = StringVar(self.PixelUpdaterWindow)
        self.defaultSpinboxVal.set("1")

        self.amountToIncrease = Spinbox(width=3, from_=0, to=10, textvariable=self.defaultSpinboxVal)    
        self.amountToIncrease.grid(row=2, column=1)

        #Button Objects

        # self.addButton = Button(text="Add a Pixel", width=11, command=lambda:pixel.updatePixel(int(self.amountToIncrease.get()), updateDate=self.entryDateUpdate()))              
        # self.updateButton = Button(text="Update a Pixel", width=11, command=lambda:pixel.updatePixel(int(self.amountToIncrease.get()), updateDate=self.entryDateUpdate()))
        self.increaseButton = Button(text="Increase a Pixel", width=11, command=lambda:pixel.updatePixel(int(self.amountToIncrease.get()), updateDate=self.entryDateUpdate()))
        self.deleteButton = Button(text="Delete\na Pixel", width=11, command=lambda:pixel.deleteDate(delDate=self.entryDateUpdate()))
        self.todayButton = Button(text="Today", command=self.inputToday)
        self.statusButton = Button(text="Pixel\nStatus", command=lambda:self.statsTab(pixel=pixel))

        # self.addButton.grid(column=6, row=1)
        # self.updateButton.grid(column=6, row=2)
        self.increaseButton.grid(column=5, columnspan=2, row=2)
        self.deleteButton.grid(column=5, columnspan=2, row=3)
        self.todayButton.grid(column=3, columnspan=2, row=2)
        self.statusButton.grid(column=3, columnspan=2, row=3)

        self.PixelUpdaterWindow.mainloop()

    def statsTab(self, pixel: Pixel):       #outputs a variety of statistics pertaining to the pixel graph (see first line in function for stats displayed)

        #quantities to display: maxQuantity, avgQuantity (overall), Average Quantity (in past week), todaysQuantity, yesterdayQuantity, totalQuantity since minDate

        #window labels add onto previous window rather than new window
        self.statsWindow = Toplevel(master=self.PixelUpdaterWindow)
        self.statsWindow.transient(self.PixelUpdaterWindow)

        self.statsWindow.title("Pixel Graph Stats")
        self.statsWindow.config(padx=20, pady=20)

        
        statDict = pixel.pixelStatus(argDate=self.entryDateUpdate())

       
        # Stat Labels

        #Max Quantity
        self.maxLabel = Label(text="Max Quantity:", master=self.statsWindow)
        self.max = Label(text=statDict["maxQuantity"], master=self.statsWindow)

        self.maxLabel.grid(row=0, column=0)
        self.max.grid(row=0, column=1)
        
        #Average Quantity (overall)
        self.avgOVALabel = Label(text="Overall Pixel Average:", master=self.statsWindow)
        self.avgOVA = Label(text=statDict["avgQuantity"], master=self.statsWindow)

        self.avgOVALabel.grid(row=1, column=0)
        self.avgOVA.grid(row=1, column=1)

        #Average Quantity (in past week)
        self.avgIPWLabel = Label(text="Pixel Average in Past Week:", master=self.statsWindow)           #needs function calculation
        self.avgIPW = Label(text="", master=self.statsWindow)

        self.avgIPWLabel.grid(row=2, column=0)
        self.avgIPW.grid(row=2, column=1)

        #Today's Quantity
        self.todayQuantityLabel = Label(text="Today's Current Quantity:", master=self.statsWindow)
        self.todayQuantity = Label(text=statDict["todaysQuantity"], master=self.statsWindow)

        self.todayQuantityLabel.grid(row=3, column=0)
        self.todayQuantity.grid(row=3, column=1)

        #Yesterday's Quantity
        self.yesterdayQuantityLabel = Label(text="Yesterday's Quantity:", master=self.statsWindow)
        self.yesterdayQuantity = Label(text=statDict["yesterdayQuantity"], master=self.statsWindow)

        self.yesterdayQuantityLabel.grid(row=4, column=0)
        self.yesterdayQuantity.grid(row=4, column=1)

        #Total Quantity since start Date
        startdate = statDict["minDate"]
        self.totQuantitySinceStartLabel = Label(text=f"Total Quantity\nSince {startdate}:", master=self.statsWindow)
        self.totQuantitySinceStart = Label(text=statDict["totalQuantity"], master=self.statsWindow)
        
        self.totQuantitySinceStartLabel.grid(row=5, column=0)
        self.totQuantitySinceStart.grid(row=5, column=1)

        self.statsWindow.mainloop()

    def inputToday(self):       #puts today's date into date boxes
        today = datetime.now()

        #Deletes original date data
        self.dateYear.delete(first=0, last=END)
        self.dateMonth.delete(first=0, last=END)
        self.dateDay.delete(first=0, last=END)

        #Inputs new data
        self.dateYear.insert(index=0, string=today.strftime("%Y"))
        self.dateMonth.insert(index=0, string=today.strftime("%m"))
        self.dateDay.insert(index=0, string=today.strftime("%d"))

    def entryDateUpdate(self):  #takes numbers from date boxes and combines them into a function usable form
        return(self.dateYear.get() + self.dateMonth.get() + self.dateDay.get())
