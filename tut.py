import Tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.entry.pack(side="top", fill="x")
        self.submit.pack(side="top")

    def on_submit(self):
        symbol = self.entry.get()
        stock = Stock(self, symbol)
        stock.pack(side="top", fill="x")


class Stock(tk.Frame):
    def __init__(self, parent, symbol):
        tk.Frame.__init__(self, parent)
        self.symbol = tk.Label(self, text=symbol + ":")
        self.value = tk.Label(self, text="123.45")
        self.symbol.pack(side="left", fill="both")
        self.value.pack(side="left", fill="both")

root = tk.Tk()
Example(root).pack(side="top", fill="both", expand=True)
root.mainloop()
