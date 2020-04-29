import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="interface",
                      help="Interface to change its MAC address")
    parser.add_option('-m', '--mac', dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(
            '[-] Please specify an interface, use --help for more info')
    elif not options.new_mac:
        parser.error(
            '[-] Please specify a MAC Address, use --help for more info')
    return options, arguments


def change_mac(interface, new_mac):
    print(f'[+] Changing MAC Address for {interface} to {new_mac}')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconfig_response = subprocess.check_output(['ifconfig', interface])
    mac_address_matches = re.search(
        r'\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_response))

    if mac_address_matches:
        return mac_address_matches.group(0)
    else:
        print('[-] Couldn not read MAC Address')


(options, values) = get_arguments()
print("[-] Current MAC: ", get_current_mac(options.interface))
change_mac(options.interface, options.new_mac)
if get_current_mac(options.interface) == options.new_mac:
    print(f'[+] MAC Address was succesfully changed to {options.new_mac}')
else:
    print('[-] MAC Addres did not get changed')
