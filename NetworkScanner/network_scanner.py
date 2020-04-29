import scapy.all as scapy
import optparse

def get_ip_range():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest="target",
                    help="Range of IPs to be scanned")

    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error(
            '[-] Please specify a range of IPs, use --help for more info')

    return options.target


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)
    
    client_list=[]
    for element in answered_list:
        client = {'ip': element[0].psrc, 'mac': element[0].hwsrc}
        client_list.append(client)

    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n"+'-'*20)
    for client in result_list:
        print(client["ip"] + '\t\t' + client["mac"])


target = get_ip_range()
print_result(scan(target))