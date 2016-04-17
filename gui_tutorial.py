import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import numpy as np
from tkFileDialog import askopenfilename
import csv

"""global variables"""

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

final_predictions={}
data_file_path=''

"""global funtions"""

def OpenFile():
    filename = askopenfilename(filetypes=[('csv file', '.csv')])
    if filename:
        data_file_path = filename

def Get_Attributes(filepath):
    with open(filepath, 'r') as fi:
        reader = pd.read_csv(fi)
        return list(reader.columns)

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
        filemenu.add_command(label="Load Data File", command =lambda: popupmsg("not supported yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        pagemenu = tk.Menu(menubar, tearoff=1)
        pagemenu.add_command(label="Graph", command = lambda: show_frame(GraphPage))
        menubar.add_cascade(label="Pages", menu=pagemenu)

        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label="1 day", command = lambda : changeTimeFrame("1d"))
        dataTF.add_command(label="3 day", command = lambda : changeTimeFrame("3d"))
        dataTF.add_command(label="1 week", command = lambda : changeTimeFrame("7d"))
        menubar.add_cascade(label = "Data Time Frame", menu=dataTF)

        tk.Tk.config(self, menu=menubar)

        self.frames={}
        #update frame page
        for page in (StartPage, GraphPage, FilePage):
            frame= page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame= self.frames[cont]
        frame.tkraise() # raise to the top




class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Alpha Data Forecast Application \n use at your own risk."""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        botton1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(GraphPage))
        botton1.pack()
        botton2 = ttk.Button(self, text="Disagree", command=quit)
        botton2.pack()



class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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
            tk.Frame.__init__(self, parent)
            top_label = ttk.Label(self, text="Attribute Selections", font=LARGE_FONT)
            top_label.pack(pady=10, padx=10)
            labels=[]
            # if data_file_path:
            #     dir_label = ttk.Label(self, text="Your file has these Attributes/Columns: ", font=LARGE_FONT)
            #     dir_label.pack()
            #     data_attributes = Get_Attributes(data_file_path)
            #     for i in data_attributes:
            #         label[i] = ttk.Label(self, text= data_attributes[i])
            #         label[i].pack()
            # if not data_file_path:
            #     dir_label = ttk.Label(self, text="Import a csv file to start")
            #     dir_label.pack()



app = ForecastApp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000) #adding data to graph live
app.mainloop()
