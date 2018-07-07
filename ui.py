# classes to create ui


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from network import Network
import validation as v
import os, sys

network = Network()


class InputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.grid(columnspan=3, sticky=tk.E+tk.W+tk.E+tk.S)
        #self.columnconfigure(0, weight=1)

        self.parent = self.winfo_toplevel()

        logo = ImageTk.PhotoImage(Image.open('logo.gif'))

        self.calcFrame = ttk.Frame(self, width=310, height=115, relief='sunken', borderwidth=0)
        self.calcFrame.grid(column=0, row=3, columnspan=2, sticky=tk.E + tk.W + tk.S + tk.N)
        self.calcFrame.grid_propagate(False)
        #self.calcFrame.columnconfigure(0, weight=1)
        #self.calcFrame.rowconfigure(0, weight=1)
        self.calcTextBox = tk.Text(self.calcFrame, bg='black', fg='white')
        self.calcTextBox.grid(column=0, row=0, sticky=tk.E+tk.W+tk.S+tk.N)

        self.nicInfoFrame = ttk.Frame(self, width=310, height=250, relief='sunken', borderwidth=1)
        self.nicInfoFrame.grid(column=0, row=4, columnspan=2, sticky=tk.E+tk.W+tk.S+tk.N)
        self.nicInfoFrame.grid_propagate(False)
        #label = tk.Label(self.nicInfoFrame, image=logo)
        #label.image = logo
        #label.grid()


        self.ipEntry = tk.StringVar()
        self.netmaskEntry = tk.StringVar()

        self.initInput()
        self.createButtons()
        # self.displayAdapterInfo()

    def initInput(self):

        # ttk.Label(self.parent, image=logo).grid(column=0, row=0)
        ttk.Label(self, text="IP Address:  ").grid(column=0, row=0)
        ttk.Entry(self, width=19, textvariable=self.ipEntry).grid(column=1,
                                                                  row=0)
        ttk.Label(self, text="Netmask (in CIDR or Dotted Decimal):  ").grid(column=0, row=1)
        ttk.Entry(self, width=19, textvariable=self.netmaskEntry).grid(column=1, row=1)


        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def createButtons(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=0, row=2, columnspan=2, sticky=tk.E+tk.W+tk.S+tk.N)
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
        self.setAttributes()
        fmt0 = "{:<35}{:>}"
        fmt1 = "{:<35}{:>}{}{}"
        fmt2 = "{:<35}{:<,}"

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
        network.ip = v.check_ip(self.ipEntry.get())
        if not network.ip:
            tk.Label(self, text="!", fg='red', font=("", 12)).grid(column=2, row=0)
        else:
            tk.Label(self, text="").grid(column=2, row=0)

        network.mask, network.cidr = v.check_mask(self.netmaskEntry.get())
        if not network.mask or not network.cidr:
            tk.Label(self, text="!", fg='red', font=("", 12)).grid(column=2, row=1)
        else:
            tk.Label(self, text="").grid(column=2, row=1)

    def displayAdapterInfo(self):
        if sys.platform == 'win32':
            command = 'ipconfig/all'
        else:
            command = 'ifconfig'

        #nicInfo = tk.Text(self.nicInfoFrame, fg='white', bg='black')
        #nicInfo.grid(column=0, row=4)
        #nicInfo.insert(tk.END, os.popen(command).read())
        #os.popen(command).read()

    def clear(self):
        logo = tk.PhotoImage(file='logo.gif')
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

    w = 435
    h = 500
    x, y = dimensions(w, h)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)

    root.grid()
    InputFrame(root).grid(column=0, row=0, columnspan=2, rowspan=3)
    # InputFrame(root).grid(column=0, row=1)  # just for testing
    root.mainloop()
