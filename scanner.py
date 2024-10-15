# import pywifi
# from pywifi import const
# import time
# import nmap  # For scanning open ports

# # Function to get Wi-Fi encryption type
# def get_encryption_type(network):
#     akm = network.akm[0] if network.akm else "Unknown"
#     if akm == const.AKM_TYPE_NONE:
#         return "Open"
#     elif akm == const.AKM_TYPE_WPA:
#         return "WPA"
#     elif akm == const.AKM_TYPE_WPAPSK:
#         return "WPA-PSK"
#     elif akm == const.AKM_TYPE_WPA2:
#         return "WPA2"
#     elif akm == const.AKM_TYPE_WPA2PSK:
#         return "WPA2-PSK"
#     # elif akm == const.AKM_TYPE_WPA3:
#     #     return "WPA3"
#     elif akm == const.AKM_TYPE_WPA3PSK:
#         return "WPA3-PSK"
#     elif akm == const.AKM_TYPE_WEP:
#         return "WEP"
#     else:
#         return "Unknown"

# # Function to check if any password from list can connect to the SSID
# def check_password_in_list(ssid, password_file, iface):
#     with open(password_file, 'r') as f:
#         passwords = f.read().splitlines()

#     # Iterate through each password and try to connect
#     for password in passwords:
#         if connect_to_wifi(ssid, password, iface):
#             return True  # Return True if connection is successful
    
#     return False  # Return False if no passwords work

# # Function to connect to a Wi-Fi network with a given SSID and password
# def connect_to_wifi(ssid, password, iface):
#     # Disconnect any active connections first
#     iface.disconnect()
#     time.sleep(1)

#     profile = pywifi.Profile()
#     profile.ssid = ssid
#     profile.auth = const.AUTH_ALG_OPEN  # Most networks use open auth
#     profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Assume WPA2 for simplicity; you can adjust based on scan
#     profile.cipher = const.CIPHER_TYPE_CCMP  # Default for WPA2
#     profile.key = password  # Set the password

#     iface.remove_all_network_profiles()  # Clear any previous profiles
#     tmp_profile = iface.add_network_profile(profile)  # Add new profile

#     iface.connect(tmp_profile)  # Attempt to connect
#     time.sleep(10)  # Wait for 10 seconds for connection to establish

#     if iface.status() == const.IFACE_CONNECTED:
#         print(f"Successfully connected to {ssid} with password: {password}")
#         iface.disconnect()
#         return True
#     else:
#         print(f"Failed to connect to {ssid} with password: {password}")
#         return False

# # Function to scan for open ports using nmap
# def scan_open_ports(target_ip):
#     nm = nmap.PortScanner()
#     nm.scan(target_ip, '1-65535')  # Scan all ports (1-65535)

#     open_ports = []
#     for proto in nm[target_ip].all_protocols():
#         lport = nm[target_ip][proto].keys()
#         for port in lport:
#             if nm[target_ip][proto][port]['state'] == 'open':
#                 open_ports.append(port)
#     return open_ports

# # Function to scan nearby Wi-Fi networks and save results
# def scan_and_save_results(password_file, output_file, target_ip=None):
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0]  # Use the first Wi-Fi interface
#     iface.scan()  # Trigger scan
#     time.sleep(3)  # Wait for scan results
#     scan_results = iface.scan_results()  # Get scan results

#     with open(output_file, 'w') as f:
#         for i, network in enumerate(scan_results, start=1):
#             ssid = network.ssid
#             encryption = get_encryption_type(network)
#             f.write(f"Network {i} ({ssid}) : {encryption}\n")
        
#         f.write("---------------------------------------\n")
        
#         # Check if passwords are found for each network
#         for network in scan_results:
#             ssid = network.ssid
#             password_found = check_password_in_list(ssid, password_file, iface)
#             status = "Password found in list" if password_found else "Password not found in list"
#             f.write(f"{ssid}: {status}\n")
        
#         # If target_ip is provided, scan for open ports
#         if target_ip:
#             open_ports = scan_open_ports(target_ip)
#             if open_ports:
#                 f.write(f"\nOpen ports on {target_ip}: {', '.join(map(str, open_ports))}\n")
#             else:
#                 f.write(f"\nNo open ports found on {target_ip}.\n")

#     print(f"Scan completed! Results saved in {output_file}")

# # Main function to trigger scanning
# if __name__ == "__main__":
#     password_file = "passwords.txt"  # File containing list of passwords (one per line)
#     output_file = "scan_results.txt"  # Output file to save results
#     target_ip = "192.168.1.1"  # Example target IP for nmap port scan (usually the router's IP)
    
#     scan_and_save_results(password_file, output_file, target_ip)

import pywifi
from pywifi import const
import time
import nmap  # For scanning open ports
from scapy.all import ARP, Ether, srp, conf
# from scapy.all import get_if_list
# print(get_if_list())

# Function to get Wi-Fi encryption type
def get_encryption_type(network):
    akm = network.akm[0] if network.akm else "Unknown"
    if akm == const.AKM_TYPE_NONE:
        return "Open"
    elif akm == const.AKM_TYPE_WPA:
        return "WPA: Recommendation: Use Safer WPA3 encryption"
    elif akm == const.AKM_TYPE_WPAPSK:
        return "WPA-PSK: Recommendation: Use Safer WPA3 encryption"
    elif akm == const.AKM_TYPE_WPA2:
        return "WPA2: Recommendation: Use Safer WPA3 encryption"
    elif akm == const.AKM_TYPE_WPA2PSK:
        return "WPA2-PSK: Recommendation: Use Safer WPA3 encryption"
    else:
        return "WPA3"

# Function to check if any password from list can connect to the SSID
def check_password_in_list(ssid, password_file, iface):
    with open(password_file, 'r') as f:
        passwords = f.read().splitlines()

    # Iterate through each password and try to connect
    for password in passwords:
        if connect_to_wifi(ssid, password, iface):
            return True  # Return True if connection is successful
    
    return False  # Return False if no passwords work

# Function to connect to a Wi-Fi network with a given SSID and password
def connect_to_wifi(ssid, password, iface):
    # Disconnect any active connections first
    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN  # Most networks use open auth
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Assume WPA2 for simplicity; you can adjust based on scan
    profile.cipher = const.CIPHER_TYPE_CCMP  # Default for WPA2
    profile.key = password  # Set the password

    iface.remove_all_network_profiles()  # Clear any previous profiles
    tmp_profile = iface.add_network_profile(profile)  # Add new profile

    iface.connect(tmp_profile)  # Attempt to connect
    time.sleep(10)  # Wait for 10 seconds for connection to establish

    if iface.status() == const.IFACE_CONNECTED:
        print(f"Successfully connected to {ssid} with password: {password}")
        iface.disconnect()
        return True
    else:
        print(f"Failed to connect to {ssid} with password: {password}")
        return False

# Function to perform ARP scan to get IP and MAC addresses of connected devices
def get_connected_devices(ip_range):

    arp_request = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        print({'ip': received.psrc, 'mac': received.hwsrc})
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# Function to scan open ports on a given IP using nmap
def scan_open_ports(ip):
    print("Start port scanning on", ip)
    nm = nmap.PortScanner()
    nm.scan(ip, '1-65535')  # Scanning all ports (1-65535)
    open_ports = []
    closed_ports = []
    for proto in nm[ip].all_protocols():
        lport = nm[ip][proto].keys()
        for port in lport:
            print(nm[ip][proto][port]['state'])
            if nm[ip][proto][port]['state'] == 'open':
                open_ports.append(port)
            else :
                closed_ports.append(port)
                # print(nm[ip][proto][port]['state'])
    return open_ports, closed_ports

# Function to scan nearby Wi-Fi networks, check passwords, and scan connected devices
def scan_and_save_results(password_file, output_file, target_ip_range, iface):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Use the first Wi-Fi interface
    iface.scan()  # Trigger scan
    # time.sleep(3)  # Wait for scan results
    scan_results = iface.scan_results()  # Get scan results

    with open(output_file, 'w') as f:
        for i, network in enumerate(scan_results, start=1):
            ssid = network.ssid
            print(network)
            encryption = get_encryption_type(network)
            f.write(f"Network {i} ({ssid}) : {encryption}\n")

        # f.write("---------------------------------------\n")
        
        # Check passwords for each network
            
    with open(devices_output_file, 'w') as f:
        # Perform ARP scan to get connected devices
        devices = get_connected_devices(target_ip_range)
        f.write("\nConnected devices:\n")
        for device in devices:
            f.write(f"IP: {device['ip']}, MAC: {    device['mac']}\n")

        # Perform nmap scan on each device for open ports
       
        # for device in devices:
        # gateway_ip = conf.route.route("0.0.0.0")[2]
                
        
    with open(port_output_file, 'w') as f:    
        f.write("\nOpen ports:\n")
        gateway_ip = "0.0.0.0"
        open_ports, closed_ports = scan_open_ports(gateway_ip)
        if open_ports:
            f.write(f"Open ports on {device['ip']}: {', '.join(map(str, open_ports))}\n")
        else:
            f.write(f"No open ports found on {device['ip']}.\n")
        
        if closed_ports:
            f.write(f"Closed ports on {device['ip']}: {', '.join(map(str, closed_ports))}\n")
        else:
            f.write(f"No closed ports found on {device['ip']}.\n")
            
        # for network in scan_results:
        #     ssid = network.ssid
        #     password_found = check_password_in_list(ssid, password_file, iface)
        #     status = "Password found in list" if password_found else "Password not found in list"
        #     status = "Password found in list"
        #     f.write(f"{ssid}: {status}\n")
        


    print(f"Scan completed! Results saved in {output_file}")

# Main function to trigger scanning
if __name__ == "__main__":
    password_file = "rockyou.txt"  # File containing list of passwords (one per line)
    
    output_file = "scan_results.txt"  # Output file to save results
    port_output_file = "port_scan_results.txt" 
    devices_output_file = "devices_results.txt"
    
    
    # target_ip_range = "192.168.134.253/24"  # Replace with your network's IP range
    target_ip_range = "10.81.8.90/20"
    iface = pywifi.PyWiFi().interfaces()[0]  # Use first Wi-Fi interface

    scan_and_save_results(password_file, output_file, target_ip_range, iface)
