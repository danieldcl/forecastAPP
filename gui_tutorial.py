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


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(10,6), dpi=100)
a = f.add_subplot(111)

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
    a.plot(xList, yList)


class ForecastApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Forecast App")
        tk.Tk.geometry(self, "600x400")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames={}

        #update frame page
        for page in (StartPage, GraphPage):
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
        botton2 = ttk.Button(self, text="Disagree", command= self.quit)
        botton2.pack()

# class PageOne(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page one", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#         botton1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
#         botton1.pack()
#         botton2 = ttk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame(PageTwo))
#         botton2.pack()
#
#
# class PageTwo(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page Two", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#         botton1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
#         botton1.pack()
#         botton2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
#         botton2.pack()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        botton1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        botton1.pack()

        """important"""

        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = ForecastApp()
ani = animation.FuncAnimation(f, animate, interval=1000) #adding data to graph live
app.mainloop()
