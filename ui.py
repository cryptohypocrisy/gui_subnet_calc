# classes to create ui


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from network import Network
import validation as v
import os, sys
import subprocess
import adapterinfo as ai

network = Network()


class InputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10", width=500)
        #self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        #self.grid()

        self.parent = self.winfo_toplevel()

        self.inputFrame = ttk.Frame(self)
        self.inputFrame.columnconfigure(0, weight=1)
        self.inputFrame.grid(column=0, row=1, columnspan=3, sticky=tk.E+tk.W+tk.S+tk.N)

        self.calcFrame = ttk.Frame(self, height=125, relief='sunken', borderwidth=0)
        self.calcFrame.grid(column=0, row=4, columnspan=3, sticky=tk.E + tk.W + tk.S + tk.N)
        self.calcFrame.grid_propagate(0)
        #self.calcFrame.columnconfigure(0, weight=1)
        # self.calcFrame.rowconfigure(0, weight=1)
        self.calcTextBox = tk.Text(self.calcFrame, bg='black', fg='white')
        # self.calcTextBox.grid_propagate(0)
        self.calcTextBox.grid(column=0, row=1, sticky=tk.E+tk.W+tk.S+tk.N)

        self.nicInfoFrame = ttk.Frame(self, width=525, height=150, relief='sunken', borderwidth=1)
        self.nicInfoFrame.grid(column=0, row=6, columnspan=2, sticky=tk.E+tk.W+tk.S+tk.N)
        self.nicInfoFrame.grid_propagate(False)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.ipEntry = tk.StringVar()
        self.netmaskEntry = tk.StringVar()

        self.initLabel()
        self.initInput()
        self.createButtons()
        self.displayAdapterInfo()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def initLabel(self):
        labelFrame = ttk.Frame(self)
        labelFrame.grid(column=0, row=0, columnspan=3, padx=25, pady=5)
        logo2 = self.resource_path('logo2.gif')
        logo = ImageTk.PhotoImage(Image.open(logo2))
        label = tk.Label(labelFrame, image=logo)
        label.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S)
        label.image = logo

    def initInput(self):
        ttk.Label(self.inputFrame, text="IP Address:").grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S)
        ttk.Entry(self.inputFrame, width=30, textvariable=self.ipEntry).grid(column=1,
                                                                  row=0, sticky=tk.E+tk.W+tk.N+tk.S)
        ttk.Label(self.inputFrame, text="Netmask (CIDR or Dotted Decimal:").grid(column=0, row=1,
                                                                                 sticky=tk.E+tk.W+tk.N+tk.S)
        ttk.Entry(self.inputFrame, width=30, textvariable=self.netmaskEntry).grid(column=1, row=1,
                                                                                  sticky=tk.E+tk.W+tk.N+tk.S)


        for child in self.inputFrame.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def createButtons(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=0, row=3, columnspan=3, sticky=tk.E+tk.W+tk.S+tk.N)
        buttonFrame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(buttonFrame, text="Clear", command=self.clear).grid(column=0, row=0,
                                                                       sticky=tk.E+tk.W+tk.S+tk.N)
        ttk.Button(buttonFrame, text="Calculate", command=self.displayResults).grid(column=1, row=0,
                                                                               sticky=tk.E+tk.W+tk.S+tk.N)
        ttk.Button(buttonFrame, text="Exit", command=self.parent.destroy).grid(column=2, row=0,
                                                                               sticky=tk.E+tk.W+tk.S+tk.N)

        for child in buttonFrame.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def displayResults(self):
        fmt0 = "{:<35}{:>}"
        fmt1 = "{:<35}{:>}{}{}"
        fmt2 = "{:<35}{:<,}"

        if self.setAttributes():
            self.calcTextBox.config(state=tk.NORMAL)
            self.calcTextBox.delete('1.0', tk.END)
            self.calcTextBox.insert(tk.END, fmt0.format("IP Address:", ".".join(network.ip)) + "\n" +
                                    fmt0.format("Netmask:", ".".join(network.mask)) + "\n" +
                                    fmt0.format("Wildcard:", ".".join(network.get_wildcard())) + "\n" +
                                    fmt1.format("Network:", ".".join(network.get_network_address()), "/", network.cidr) + "\n" +
                                    fmt0.format("Broadcast:", ".".join(network.get_broadcast_address())) + "\n" +
                                    fmt0.format("Class:", network.get_net_class()) + "\n" +
                                    fmt2.format("Hosts per Network:", network.get_num_networks_hosts()[1]))

        self.calcTextBox.config(state=tk.DISABLED)

    def setAttributes(self):
        self.calcTextBox.config(state=tk.NORMAL)
        self.calcTextBox.delete('1.0', tk.END)

        network.ip = v.check_ip(self.ipEntry.get())
        if not network.ip:
            self.calcTextBox.insert(tk.END, "Invalid IP address...try again.\n")

        network.mask, network.cidr = v.check_mask(self.netmaskEntry.get())
        if not network.mask:
            self.calcTextBox.insert(tk.END, 'Invalid netmask...try again.\n')

        if not network.mask or not network.ip:
            return False
        else:
            return True

    def displayAdapterInfo(self):
        # create text box and place it into frame, set height in lines
        nicInfo = tk.Text(self.nicInfoFrame, height=10, width=63, wrap=tk.NONE, fg='white', bg='black')

        # create scrollbars for text window and place it into frame
        yscrollbar = ttk.Scrollbar(self.nicInfoFrame, orient=tk.VERTICAL)
        xscrollbar = ttk.Scrollbar(self.nicInfoFrame, orient=tk.HORIZONTAL)

        # set scroll action to alter nicInfo's yview attribute
        # and link the scrollbar to nicInfo
        yscrollbar.config(command=nicInfo.yview)
        xscrollbar.config(command=nicInfo.xview)
        nicInfo['yscroll'] = yscrollbar.set
        nicInfo['xscroll'] = xscrollbar.set

        # put text box into the grid and place scrollbar on top
        nicInfo.grid(column=0, row=5)
        yscrollbar.place(in_=nicInfo, x=506, y=-2, height=150)
        xscrollbar.place(in_=nicInfo, width=508, x=-2, y=131)

        # insert host info into into the textbox
        # and disable input
        #nicInfo.insert(tk.END, "Host information...\n\n")
        nicInfo.insert(tk.END, ai.ipconfig())
        nicInfo.config(state=tk.DISABLED)

    def clear(self):
        self.ipEntry.set("")
        self.netmaskEntry.set("")
        self.calcTextBox.config(state=tk.NORMAL)
        self.calcTextBox.delete('1.0', tk.END)


def dimensions(w, h):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw/2) - (w/2)
    y = (sh/2) - (h/2)

    return x, y


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Subnet Calculator")

    w = 555
    h = 475
    x, y = dimensions(w, h)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)

    InputFrame(root).grid(column=0, row=0)
    #InputFrame(root).grid(column=0, row=1)  # just for testing
    root.mainloop()
