from netmiko import ConnectHandler
from datetime import datetime
from pprint import pprint
import re

# Obtendo endereços de IP
with open("ip.txt") as f:
    ips = f.readlines()

# Definindo parametros dos dispositivos
arista1 = {
        "device_type": "arista_eos",
        "host": ips[0].rstrip("\n"),
        "username": "admin",
        "password": "python1"
}

arista2 = {
        "device_type": "arista_eos",
        "host": ips[1].rstrip("\n"),
        "username": "admin",
        "password": "python2"
}

arista3 = {
        "device_type": "arista_eos",
        "host": ips[2].rstrip("\n"),
        "username": "admin",
        "password": "python3"
}

# Conectando nos dispositivos via SSHv2
switches = [arista1, arista2, arista3]

# Criando lista para as saídas
output_list = []

for switch in switches:
    connection = ConnectHandler(**switch)
    syslog_output = connection.send_command("show logging last 1 day")
    output_list.append(syslog_output)

# Dicionário para o output
output_map = {}

# Extraindo as informações do LLDP das mensagens de log messages
for output in output_list:
    # Obtendo hostname
    hostname_regex = re.findall(r".+\d\d:\d\d:\d\d\s(.+?)\s", output)
    hostname = hostname_regex[0]

    # Obtendo informações LLDP
    output_lines = output.split("\n")
    #pprint(output_lines)

    # Lista para armazenar as informações LLDP
    lldp_lines = []

    for line in output_lines:
        if re.search(r"LLDP", line, re.I) and re.search(r"neighbor", line, re.I):
            lldp_lines.append(line + "\n")

    # Criando hostname:output por dispositivo
    output_map[hostname] = lldp_lines

#pprint(output_map)

# Criando um relatório LLDP periodico e salvando na pasta local
# Salvando arquivo com a data
with open("lldp_{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M")), "w") as f:
    for entry in output_map.items():
        f.write(entry[0] + "\n")
        f.writelines(entry[1])
        f.write("\n\n")
