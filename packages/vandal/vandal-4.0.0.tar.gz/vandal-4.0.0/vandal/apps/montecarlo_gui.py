import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import vandal

# set font
FONT_BIG = ("Helvetica heavy", 15)
FONT_SMALL = ("Helvetica", 10)

class MonteCarloGUI:
    def __init__(self, master):
        self.master = master
        master.title("Monte Carlo application (c) David Kundih")

        # set style options
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('.', font=FONT_BIG)

        # create frames
        self.title_frame = tk.Frame(master)
        self.title_frame.pack(pady=(20, 0))

        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack(pady=(20, 0))

        self.plot_frame = tk.Frame(master, bd=2, relief=tk.GROOVE)
        self.plot_frame.pack(padx=10, pady=(20, 10), fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=(0, 20))

        #self.status = tk.Frame(master)
        #self.status.pack(pady=(1, 0))

        self.credit_frame1 = tk.Frame(master)
        self.credit_frame1.pack(pady=(1, 0))

        self.credit_frame2 = tk.Frame(master)
        self.credit_frame2.pack(pady=(1, 0))

        # create labels and entries
        self.heading = tk.Label(self.title_frame, text="MONTE CARLO APPLICATION", font = FONT_BIG)
        self.heading.grid(row=0, column=0, padx=(2, 2), pady=10, sticky='e')

        self.label1 = tk.Label(self.entry_frame, text="Enter a time period: ")
        self.label1.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='e')

        self.entry1 = tk.Entry(self.entry_frame, width=10)
        self.entry1.grid(row=1, column=1, padx=(0, 10), pady=10)

        self.label2 = tk.Label(self.entry_frame, text="Enter a number of simulations: ")
        self.label2.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='e')

        self.entry2 = tk.Entry(self.entry_frame, width=10)
        self.entry2.grid(row=2, column=1, padx=(0, 10), pady=10)

        #self.response = tk.Label(self.status, text="STATUS: Awaiting actions...")
        #self.response.grid(row=0, column=0, padx=(1, 1), pady=10, sticky='e')

        self.credit1 = tk.Label(self.credit_frame1, text="PACKAGE: vandal (c) David Kundih, 2021-")
        self.credit1.grid(row=0, column=0, padx=(1, 1), pady=10, sticky='e')

        self.credit2 = tk.Label(self.credit_frame2, text="GUI: (c) David Kundih, 2023. Based on Tkinkter Framework.")
        self.credit2.grid(row=0, column=0, padx=(1, 1), pady=10, sticky='e')

        # create buttons
        self.file_button = tk.Button(self.button_frame, text="Open .csv file", command=self.load_file, width=15)
        self.file_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        self.execute_button = tk.Button(self.button_frame, text="Initialize simulation", command=self.execute, width=15)
        self.execute_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

        # create plot
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            df = pd.read_csv(file_path)
            self.df = df
        else:
            tk.messagebox.showwarning(title="Warning", message="Please select a valid file.")


            """def change_status(self, arg):
                    self.response.destroy()
                    if arg == 'init':
                        self.response = tk.Label(self.status, text="STATUS: Attempting to create a simulation...")
                        self.response.grid(row=0, column=0, padx=(1, 1), pady=10, sticky='e')
                    elif arg == 'start':
                        self.response = tk.Label(self.status, text="STATUS: Awaiting actions...")
                        self.response.grid(row=0, column=0, padx=(1, 1), pady=10, sticky='e')
            """

    def execute(self):  
        try:
            self.df
        except AttributeError:
            tk.messagebox.showwarning(title="Warning", message="Please select a .csv file first.")
            return 
        
        if not self.entry1.get().isdigit():
            tk.messagebox.showwarning(title="Warning", message="Please enter a valid time period.")
            return 
        elif not self.entry2.get().isdigit():
            tk.messagebox.showwarning(title="Warning", message="Please enter a valid number of simulations.")
            return 
        self.fig.clear()
        MC = vandal.MonteCarlo(self.df, int(self.entry1.get()), int(self.entry2.get()))
        try:
            MC = MC.execute()
        except:
            tk.messagebox.showwarning(title="Warning", message="The input data must be in the first column of a document, each field containing one value. Column index can be of the type string, but it is advised that all values are of the type integer or float. Only .csv files are supported in the current version.")
            return
        plt.title('vandal (c) David Kundih, 2021-', fontsize=12, weight='regular', loc='right')
        plt.plot(MC)
        self.plot_canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = MonteCarloGUI(root)
    root.mainloop()