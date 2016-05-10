import Tkinter as tk
import ttk
import tkFileDialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import numpy as np
import csv


"""global variables"""
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
final_predictions={}
data_file_path=''
time_frame=7

style.use("ggplot")
f = Figure()
a = f.add_subplot(111)


"""global funtions"""
def tutorial():
    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text="Overview of the application", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(tut, text="Close", command=tut.destroy)
    B1.pack()

def changeTimeFrame():
    global time_frame
    tfFrame = tk.Tk()
    tfFrame.geometry("640x360")
    tfFrame.wm_title("Number of days?")
    label = ttk.Label(tfFrame, text = "Enter the number of days to forecast")
    label.pack(side="top", fill="x", pady=10)
    ent = ttk.Entry(tfFrame)
    ent.insert(0, 7)
    ent.pack()
    ent.focus_set()

    def callback():
        time_frame = int(ent.get())
        tfFrame.destroy()

    b = ttk.Button(tfFrame, text="submit", width=10, command = callback)
    b.pack()
    tk.mainloop()



def Get_Attributes(filename):
    try:
        with open(filename, 'r') as fi:
            reader = pd.read_csv(fi)
            return list(reader.columns)
    except:
        print "file not imported yet"

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font = NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def animate(i):
    pullData = open("sampledata.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear() #this erases the graph data in a
    a.plot(xList, yList, "#00A3E0", label="random data")
    a.legend(bbox_to_anchor=(0,1.02), loc=3, ncol=2,borderaxespad=0)
    temp_title="Temperary Title"
    a.set_title(temp_title)

def assignFilePath(filename):
    global data_file_path
    data_file_path = filename

def print_data_path():
    global data_file_path
    print data_file_path


"""class definitions"""
class ForecastApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Forecast App")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command= tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(self, menu=menubar)
        self.filename=tk.StringVar()
        self.frames={}
        #update frame page
        for page in (StartPage, GraphPage, FilePage, AttPage):
            frame= page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame= self.frames[cont]
        frame.tkraise() # raise to the top




class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Alpha Data Forecast Application \n use at your own risk."""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        botton1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(FilePage))
        botton1.pack()
        botton2 = ttk.Button(self, text="Disagree", command=quit)
        botton2.pack()



class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        botton1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        botton1.pack()

        """important!! this is how the graph was drawn"""

        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        """"""


class FilePage(tk.Frame):
        def __init__(self, parent, controller):
            self.controller = controller
            tk.Frame.__init__(self, parent)
            top_label = ttk.Label(self, text="Choose Data File", font=LARGE_FONT)
            top_label.pack(pady=10, padx=10)
            self.but = ttk.Button(self, text="Browse", command=self.load_file)
            self.but.pack()

        def load_file(self):
            filepath = tkFileDialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
            if filepath:
                self.controller.filename.set(filepath)

                page = AttPage(self,self.controller)
                page.pack(side="left")

            else:
                popupmsg("Fail to open file! Make sure your file is in the right format.")




class AttPage(tk.Frame):
    def __init__(self, parent, controller):
        # self.controller = controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text=("""Select an attribute to predict:"""), font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)
        f = self.controller.filename.get()
        labels=[]
        if f:
            atts = Get_Attributes(f)
            for i in range(len(atts)):
                self.label[i] = tk.Label(self, text= atts[i], font=LARGE_FONT)
                self.label[i].pack(pady=10, padx=10)






app = ForecastApp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000) #adding data to graph live
app.mainloop()
