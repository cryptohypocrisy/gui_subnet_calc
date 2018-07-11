import subprocess


def ipconfig():
    return_string = "Host Information".center(65) + "\n\n"

    ipconfig = subprocess.Popen('ipconfig /all', stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
    ip_str = ""
    for item in ipconfig:
        ip_str += str(item)
    ip_str = ip_str.lower()

    adapters = ['ethernet adapter', 'wireless lan adapter']
    attributes = ['description', 'physical address', 'dhcp enabled',
                  'ipv4 address', 'subnet mask', 'default gateway',
                  'dhcp server', 'dns servers']
    other_info = ["host name", "primary dns suffix", ]

    for info in other_info:
        i0 = ip_str.find(info)
        if i0 != -1:
            i1 = ip_str.find(":", i0)
            i2 = ip_str.find("\\", i1)
            return_string += ip_str[i0:i0 + len(info)].title().replace("Dns", "DNS") + ": " + ip_str[i1 + 1:i2] +"\n"

    return_string += "\nNetwork Adapters:\n\n"

    for adapter in adapters:
        c = 0
        for n in range(ip_str.count(adapter)):
            i0 = ip_str.find(adapter, c)
            i1 = ip_str.find(":", i0)
            return_string += "\t" + ip_str[i0:i1].title() + "\n\t" + ("-" * len(ip_str[i0:i1])) + "\n"
            c = i1

            for attribute in attributes:
                a0 = ip_str.find(attribute, c)
                if a0 != -1:
                    a1 = ip_str.find(":", a0)
                    a2 = ip_str.find("\\", a1)
                    return_string += "\t" + \
                        ip_str[a0:a0+len(attribute)].title().replace("Dns",
                                                                     "DNS").replace("Dhcp",
                                                                                    "DHCP").replace("Ipv4",
                                                                                                    "IPv4") + ": "
                    return_string += ip_str[a1 + 1:a2].title() + "\n"
                    if attribute == "dns servers":
                        a3 = ip_str.find(ip_str[a1+1:a2], a1) + len(ip_str[a1+1:a2])+4
                        a4 = ip_str.find("netbios", a3)
                        #if ip_str[a3:a4].startswith()
                        return_string += "\t\t      " + \
                                         ip_str[a3:a4].strip().replace(" ", "").replace("\\r\\n", "\n\t\t      ")
            return_string += "\n"
    return_string += "\n\n"

    return return_string
