# class used to instantiate a network object from an IP address, netmask, and
# corresponding CIDR notation value; can perform various calculations using
# these private attributes; best used with getipinfo.py module to get and return
# ip and mask as lists

import math as m


class Network:
    # ip and mask should be passed as lists containing four integers --
    # one for each octet in decimal form
    def __init__(self, ip_list=[], mask_list=[], cidr=0):
        self.ip = ip_list
        self.mask = mask_list
        self.cidr = cidr

    # override default __str__ method for easy testing/viewing of
    # object's stored ip/mask/cidr values
    def __str__(self):
        ip_str = ""
        netmask_str = ""

        n = 0  # used to find the correct index if there are duplicate integers
        for octet in self.ip:
            ip_str += str(octet)
            # don't print a dot if it's the last octet
            if self.ip.index(octet, n) != len(self.ip)-1:
                ip_str += "."
            n += 1

        n = 0  # used to find the correct index if there are duplicate integers
        for octet in self.mask:
            netmask_str += str(octet)
            # don't print a dot if it's the last octet
            if self.mask.index(octet, n) != len(self.mask)-1:
                netmask_str += "."
            n += 1

        return "IP: " + ip_str + "\\" + str(self.cidr) + "\n" + "Netmask: " + \
               netmask_str

    # AND the ip and mask octets to get the network address and return
    # it as a list
    def get_network_address(self):
        net_address_list = []

        for i in range(4):
            net_address = int(self.ip[i]) & int(self.mask[i])
            net_address_list.append(str(net_address))

        return tuple(net_address_list)

    # OR the ip and wildcard octets to get the broadcast address and
    # return it as a list
    def get_broadcast_address(self):
        broadcast_address_list = []
        wildcard_list = []

        # find wildcard octets by subtracting mask values from 255
        for n in self.mask:
            x = 255 - int(n)
            wildcard_list.append(x)

        for i in range(4):
            broad_address = int(self.ip[i]) | int(wildcard_list[i])
            broadcast_address_list.append(str(broad_address))

        return tuple(broadcast_address_list)

    # get the number of available networks and hosts
    def get_num_networks_hosts(self):
        for i in self.mask:
            # the significant octet will be the first one with a value
            # below 255, iterate thru the mask octets until it is found
            if 0 <= int(i) < 255:
                significant_index = self.mask.index(str(i))
                break
            else:
                # if all octets are 255 this will catch it
                significant_index = 3

        # use the cidr value to find number of hosts and number of networks
        # based on which octet is significant
        if significant_index == 0:
            number_of_hosts = int(m.pow(2, (32 - self.cidr)) - 2)
            number_of_networks = int(m.pow(2, self.cidr))
        elif significant_index == 1:
            number_of_hosts = int(m.pow(2, (24 - (self.cidr - 8))) - 2)
            number_of_networks = int(m.pow(2, self.cidr - 8))
        elif significant_index == 2:
            number_of_hosts = int(m.pow(2, (16 - (self.cidr - 16))) - 2)
            number_of_networks = int(m.pow(2, self.cidr - 16))
        elif significant_index == 3:
            number_of_hosts = int(m.pow(2, (8 - (self.cidr - 24))) - 2)
            number_of_networks = int(m.pow(2, self.cidr - 24))

        if int(self.mask[3]) == 255:
            number_of_networks = 0
            number_of_hosts = 1

        return number_of_networks, number_of_hosts

    # use the first octet of the ip to find network class
    def get_net_class(self):
        if '0' <= self.ip[0] <= '126':
            return "A"
        elif self.ip[0] == '127':
            return "A (loopback)"
        elif '128' <= self.ip[0] <= '191':
            return "B"
        elif '192' <= self.ip[0] <= '223':
            return "C"
        elif '224' <= self.ip[0] <= '239':
            print(type(self.ip[0]))
            return "D"
        else:
            return "E"

    # XOR each mask octet with 255 to get wildcard mask
    def get_wildcard(self):
        wildcard_list = []

        for octet in self.mask:
            wildcard = int(octet) ^ 255
            wildcard_list.append(str(wildcard))

        return tuple(wildcard_list)
