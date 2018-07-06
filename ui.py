# classes to create ui


import tkinter as tk
from tkinter import ttk
from network import Network
import validation as v

network = Network()


class InputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.grid()
        #self.columnconfigure(0, weight=1)

        self.parent = parent

        self.ipEntry = tk.StringVar()
        self.netmaskEntry = tk.StringVar()
        self.ipLabel = tk.StringVar()
        self.netmaskLabel = tk.StringVar()
        self.wildcardLabel = tk.StringVar()
        self.netAddressLabel = tk.StringVar()
        self.cidrLabel = tk.StringVar()
        self.broadcastLabel = tk.StringVar()
        self.netClassLabel = tk.StringVar()
        self.numHostsLabel = tk.StringVar()

        self.initInput()
        self.createButtons()

    def initInput(self):
        # logo = tk.PhotoImage(file='logo.gif')
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
        # buttonFrame.columnconfigure(1, weight=1)
        # buttonFrame.columnconfigure(2, weight=1)
        ttk.Button(buttonFrame, text="Clear", command=self.clear,).grid(column=0, row=0,
                                                                       sticky=tk.E+tk.W+tk.S+tk.N)
        ttk.Button(buttonFrame, text="Calculate", command=self.displayResults).grid(column=1, row=0,
                                                                               sticky=tk.E+tk.W+tk.S+tk.N)
        ttk.Button(buttonFrame, text="Exit", command=self.parent.destroy).grid(column=2, row=0,
                                                                               sticky=tk.E+tk.W+tk.S+tk.N)

        for child in buttonFrame.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def displayResults(self):
        self.setAttributes()
        fmt = "{:<35}{:<}"
        self.ipLabel.set(fmt.format("IP Address:", ".".join(network.ip)))
        self.netmaskLabel.set(fmt.format("Netmask:", ".".join(network.mask)))
        self.wildcardLabel.set(fmt.format("Wildcard:", ".".join(network.get_wildcard())))
        self.netAddressLabel.set("{:<35}{:<}{}{}".format("Network:", ".".join(network.get_network_address()), "/", network.cidr))
        self.broadcastLabel.set(fmt.format("Broadcast:", ".".join(network.get_broadcast_address())))
        self.netClassLabel.set(fmt.format("Class:", ".".join(network.get_net_class())))
        self.numHostsLabel.set("{:<35}{:<,}".format("Hosts per Network:", network.get_num_networks_hosts()[1]))

        textFrame = ttk.Frame(self, relief='sunken', borderwidth=5)
        textFrame.grid(column=0, row=3, columnspan=2, rowspan=2, sticky=tk.E+tk.W+tk.S+tk.N)
        textFrame.columnconfigure(0, weight=1)
        textFrame.rowconfigure(0, weight=1)

        tk.Label(textFrame, textvariable=self.ipLabel).grid(column=0, row=0, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.netmaskLabel).grid(column=0, row=1, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.wildcardLabel).grid(column=0, row=2, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.netAddressLabel).grid(column=0, row=3, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.broadcastLabel).grid(column=0, row=4, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.netClassLabel).grid(column=0, row=5, sticky=tk.W)
        tk.Label(textFrame, textvariable=self.numHostsLabel).grid(column=0, row=6, sticky=tk.W)

    def setAttributes(self):
        network.ip = v.check_ip(self.ipEntry.get())
        if not network.ip:
            tk.Label(self, text="!", fg='red', font=("", 14)).grid(column=2, row=0)
            return
        else:
            tk.Label(self, text="").grid(column=2, row=0)

        network.mask, network.cidr = v.check_mask(self.netmaskEntry.get())
        if not network.mask or not network.cidr:
            tk.Label(self, text="!", fg='red', font=("", 14)).grid(column=2, row=1)
        else:
            tk.Label(self, text="").grid(column=2, row=1)

    def clear(self):
        self.ipEntry.set("")
        self.netmaskEntry.set("")
        self.ipLabel.set("")
        self.netmaskLabel.set("")
        self.wildcardLabel.set("")
        self.netAddressLabel.set("")
        self.cidrLabel.set("")
        self.broadcastLabel.set("")
        self.netClassLabel.set("")
        self.numHostsLabel.set("")


def dimensions(w, h):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw/2) - (w/2)
    y = (sh/2) - (h/2)

    return x, y


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Subnet Calculator")

    w = 380
    h = 300
    x, y = dimensions(w, h)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)

    root.grid()
    InputFrame(root).grid(column=0, row=0, columnspan=2, rowspan=3)
    # InputFrame(root).grid(column=0, row=1)  # just for testing
    root.mainloop()
