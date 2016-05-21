"""
Author: Ding Chao Liao
last update: 5/20/2016
"""

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import ttk
import tkFileDialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import csv
from functions import *
import time
import threading
import ast


"""global variables"""
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
f = Figure()
a = f.add_subplot(111)


"""global funtions"""

def animate(i):
    # this function reads predictions from the predictions file and generates the graph in graph frame
    with open("predictions.txt", "a+") as fi:
        yList = []
        yList2 = []
        for eachLine in fi:
            fields = eachLine.split(',')
            yList.append(float(fields[0]))
            yList2.append(float(fields[1]))

    xList = [i+1 for i in range(len(yList))]
    a.clear() #this erases the graph data in a
    a.plot(xList, yList, "#00A3E0", label="predicions")
    a.plot(xList, yList2, "#000000", label="real values")
    a.legend(bbox_to_anchor=(0,1.02), loc=3, ncol=2,borderaxespad=0)
    temp_title="Predictions"
    a.set_title(temp_title)


tutorialmessage = """Overview of the application:\n
Our program works best for numerical data analysis.\n
Each predicting model works differently.\n
XGBoost: accurate, moderate to long.\n
DecisionTree: moderate.\n
RandomForest: 10 trees, slow, requires RAM.\n
LinearRegression: fast, best for linear data.\n
1: select dependent attribute and independent attributes.\n
2: pick a predicting model and specify the number of predictions.\n
3: run prediction and see the results \n"""

def tutorial():
    # creates a message box that shows the overview of the program
    tut = tk.Tk()
    tut.wm_title("About/How")
    label = ttk.Label(tut, text=tutorialmessage, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(tut, text="Close", command=tut.destroy)
    B1.pack()


def getSizeOfFile(filepath):
    # this gets the size of the datafile,
    import os
    return int(os.path.getsize(filepath))




def Get_Attributes(filename):
    #this function returns the attribute names of the datafile
    try:
        with open(filename, 'r') as fi:
            return fi.next().strip('\n').split(',')
    except:
        popupmsg("No such file.")

def popupmsg(msg):
    #this function pops up a message box for warning usage.
    popup = tk.Tk()
    popup.wm_title("!")
    popup.geometry("200x100")
    label = ttk.Label(popup, text=msg, font = NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    ttk.Button(popup, text="Close", command=popup.destroy).pack()


"""class definitions"""
class ForecastApp(tk.Tk):
    # main class of the app

    # initialize the labels and buttons
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Forecast App")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # menubar declaration
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About/How", command= tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)
        tk.Tk.config(self, menu=menubar)

        # variables to store important info
        self.filename=tk.StringVar()
        self.yVar = tk.StringVar()
        self.xVar = tk.StringVar()
        self.modelVar = tk.StringVar()
        self.predictions= tk.StringVar()
        self.num = tk.StringVar()


        self.frames={}
        #update frame page
        for page in (StartPage, GraphPage, FilePage, AttPage, CleaningPage, ModelPage, ResultPage):
            frame= page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        # raise frame to the top
        frame= self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):
    # shows the alpha warning frame. if the user click disagree program will close. else go to file page

    # initialize the labels and buttons
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
    # this class generates the graph frame

    # initialize the labels and buttons
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, textvariable=self.controller.yVar, text=self.controller.yVar.get() , font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #create buttons to go to different frames
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame(ResultPage)).pack(anchor='nw')
        ttk.Button(self, text="Select Model", command=lambda: controller.show_frame(ModelPage)).pack(anchor='nw')
        ttk.Button(self, text="File Page", command=lambda: controller.show_frame(FilePage)).pack(anchor='nw')


        """this embeds the matplotlib graph to display on the frame"""
        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        """"""




class FilePage(tk.Frame):
    # page frame to import file and display attributes for selection

    # initialize the labels and buttons
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        top_label = ttk.Label(self, text="Choose Data File: ", font=LARGE_FONT)
        top_label.grid(row=0,column=0, rowspan=1, columnspan=1, pady=10, padx=10)
        self.but = ttk.Button(self, text="Browse", command=self.load_file)
        self.but.grid(row=0, column=1, rowspan=1, columnspan=1)


    def load_file(self):
        # ask user to input file
        filepath = tkFileDialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if filepath:
            # store file path in variable and display attribute selection frame
            self.controller.filename.set(filepath)
            page = AttPage(self,self.controller)
            page.grid(row=2, column=0, columnspan=10)

        else:
            # show popup message
            popupmsg("Fail to open file! Make sure your file is in the right format.")




class AttPage(tk.Frame):
    # This frame generates the list boxes to allow the user to select attributes

    # initialize the labels and buttons
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        fi = self.controller.filename.get()

        # check file size and get the data attributes
        if fi!='':
            fsize = getSizeOfFile(fi)
            if fsize >128000000:
                label = tk.Label(self, text="File Larger than 128mb, we recommend using xgboost modeling", bg='red', font=LARGE_FONT)
                label.pack()
            self.atts = Get_Attributes(fi)
            tk.Label(self, text=("""Select an attribute to predict, then attributes to train:"""), \
                    font=LARGE_FONT).pack(side='top',pady=10, padx=10, anchor='w')

            """ define listboxes  """
            # define and put attributes into list boxes
            self.scrollbar = tk.Scrollbar(self)
            self.scrollbar2 = tk.Scrollbar(self)
            self.scrollbar.pack(side='left', fill='y',pady=10, padx=10)
            self.scrollbar2.pack(side='left', fill='y',pady=10, padx=10)
            self.yList = tk.Listbox(self, width=30, height=20, exportselection=0, yscrollcommand=self.scrollbar.set)
            self.xList = tk.Listbox(self, width=30, height=20, exportselection=0 ,selectmode= tk.MULTIPLE, yscrollcommand=self.scrollbar2.set)

            for i in self.atts:
                self.yList.insert(tk.END, str(i))
                self.xList.insert(tk.END, str(i))

            self.yList.pack(side='left', fill='y',pady=10, padx=10)
            self.xList.pack(side='left', fill='y',pady=10, padx=10)
            self.scrollbar.config(command= self.yList.yview)
            self.scrollbar2.config(command= self.xList.yview)

            """ end of listboxes"""

            # buttons
            self.selectBut = tk.Button(self, text='Next', command=lambda: self.onSelect())
            self.selectBut.pack(side='left',pady=10, padx=10)
            self.resetBut = tk.Button(self, text='reset', command= lambda: self.grid_forget())
            self.resetBut.pack(anchor='nw')


    def onSelect(self):
        # get selected inputs from user. save selections to variables
        ydx = self.yList.curselection()
        xdx = self.xList.curselection()
        if xdx and ydx:
            attributes = []
            for i in xdx:
                attributes.append(self.atts[i])
            self.controller.xVar.set(attributes)
            self.controller.yVar.set(self.atts[ydx[0]])
            self.controller.show_frame(ModelPage)
        else:
            popupmsg("""Pick an attribute to continue.""" )


class CleaningPage(tk.Frame):
    # this frame shows the cleaning in process while the program is cleaning the data and generating predictions

    # initialize the labels and buttons
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(FilePage)).pack(anchor='nw')
        ttk.Label(self, text='This will take some time base on the size of the data and the model! ', font=LARGE_FONT).place(relx=.5, rely=.4, anchor='c')
        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='indeterminate')
        self.progressbar.place(relx=.5, rely=.5, anchor='c')
        ttk.Button(self, text='Confirm and Run', command=self.apply).place(relx=.5, rely=.45, anchor='c')

    def apply(self):
        # create a thread for cleaning process
        self.secondary_thread = threading.Thread(target=self.cleanProgress)
        self.secondary_thread.start()
        self.progressbar.start()
        self.after(10, self.checkbar)

    def checkbar(self):
        # checks cleaning process status
        if self.secondary_thread.is_alive() ==False:
            self.progressbar.stop()
            self.controller.show_frame(ResultPage)

        else:
            self.after(10, self.checkbar)

    def cleanProgress(self):
        # after cleaning and making predictions, store predictions into a text file for generating graph
        try:
            predicted_results = Generate_Prediction(self.controller.modelVar.get(), \
                self.controller.filename.get(), self.controller.xVar.get(), self.controller.yVar.get(), int(self.controller.num.get()))
            forecast = predicted_results[0]
            ytest = predicted_results[1]

            with open('predictions.txt', 'w+') as fil:
                for i in range(len(forecast)):
                    fil.write(str(forecast[i]) +','+ str(ytest[i]) + '\n')

            self.controller.predictions.set(forecast)
        except IndexError:
            popupmsg("An error occurred during data cleaning.")


class ModelPage(tk.Frame):
    # create the frame to allow user to pick predicting models

    # initialize the labels and radiobuttons
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(FilePage)).pack(anchor='nw')
        ttk.Label(self, text="Choose Predicting Model: ", font=LARGE_FONT).pack()

        models = ['xgboost', 'DecisionTree','RandomForest', 'LinearRegression']
        for i in models:
            tk.Radiobutton(self, text=i, variable=self.controller.modelVar, value=i, command=self.controller.modelVar.set(i)).pack()
        ttk.Label(self, text="How Many Days/Predictions? ").pack()

        self.controller.num.trace('w', self.validate_num)
        ttk.Entry(self, textvariable=self.controller.num, width=5).pack()

        self.ToCleanPage = ttk.Button(self, text='Next', state=tk.DISABLED, command=lambda: self.controller.show_frame(CleaningPage))
        self.ToCleanPage.pack(side='top')

    def validate_num(self, name, index, mode):
        # function that validates the user input to be an integer
        try:
            n = self.controller.num.get()
            n = int(n)
            self.ToCleanPage.config(state=tk.NORMAL)
            return True
        except TypeError:
            return False



class ResultPage(tk.Frame):
    # frame to display the predictions

    # initialize the labels, buttons, and redirects
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        ttk.Button(self, text="See Graph", command=lambda: controller.show_frame(GraphPage)).pack(side='left', anchor='nw')
        ttk.Button(self, text="File Page", command=lambda: controller.show_frame(FilePage)).pack(side='left', anchor='nw')
        ttk.Button(self, text="See Predictions", command=self.show_predictions).pack()

    def show_predictions(self):
        # create a text box to display the predictions
        with open('predictions.txt', 'r') as pf:
            r = pf.read()
            # self.scrollbar3 = tk.Scrollbar(self)
            # self.scrollbar3.pack(side='right', fill='y')
            self.text = tk.Text(self, width=50, height=35)
            self.text.insert('end', r)
            self.text.place(relx=.5, rely=.5, anchor='c')
            # self.scrollbar3.config(command= self.text.yview)




# running the app
app = ForecastApp()
app.geometry("960x720")
ani = animation.FuncAnimation(f, animate, interval=5000) # grades the predictions, refreshes every 5 seconds
app.mainloop()
