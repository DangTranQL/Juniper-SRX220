from asyncio.windows_events import NULL
import os
from netmiko import ConnectHandler, Netmiko, NetmikoTimeoutException
import datetime

def check_device(type, ip, username, password):
    try:
        #cisco not necessary
        if type == 'cisco_os':
            cisco_ios = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'port': 22,
                'secret': '',
            }
            net_connect = ConnectHandler(**cisco_ios)
            config_commands = ('conf t', 'enable secret cisco',
                               'line console 0', 'password cisco', 'login', 'line vty 0 4', 'password cisco', 'login',
                               'exit', 'int vlan1', 'ip add 10.1.2.3 255.255.255.0', 'no shut', 'exit',
                               'show conf')
            output = net_connect.send_config_set(config_commands, exit_config_mode=False)
            print(output)
        elif type == 'juniper_os':
            juniper_ios = {
                'device_type' : 'juniper_junos',
                'host' : ip,
                'username' : username,
                'password' : password,
                'port' : 22,
                'secret' : '',
            }
            net_connect = ConnectHandler(**juniper_ios) 
            return net_connect
    except NetmikoTimeoutException as error:
        print("Error {}".format(error))

def configure(device):
    config_commands = ('set version 12.1X44-D35.5', 'set system autoinstallation interfaces ge-0/0/0',
                       'set system host-name J1', 'set system domain-name 209.0.9.10',
                       'set system root-authentication encrypted-password "$1$a3MgpMXS$Gs.LPJbRGUoJurXMX/Giw0"',
                       'set system name-server 208.67.222.222', 'set system name-server 208.67.220.220',
                       'set system login class noc-user-class idle-timeout 3', 'set system login class noc-user-class login-alarms',
                       'set system login class noc-user-class login-tip', 'set system login user nocuser uid 2004',
                       'set system login user nocuser class operator', 'set system login user nocuser authentication encrypted-password "$1$TwTsp7RM$.GMTPwC4./GmnVOP87LYW/"',
                       'set system services ftp', 'set system services ssh root-login allow',
                       'set system services telnet', 'set system services xnm-clear-text',
                       'set system services web-management http interface vlan.0', 'set system services web-management https system-generated-certificate',
                       'set system services web-management https interface vlan.0', 'set system services dhcp router 192.168.1.1',
                       'set system services dhcp pool 192.168.1.0/24 address-range low 192.168.1.2',
                       'set system services dhcp pool 192.168.1.0/24 address-range high 192.168.1.254', 'set system services dhcp propagate-settings ge-0/0/0.0',
                       'set system syslog archive size 100k', 'set system syslog archive files 3',
                       'set system syslog user * any emergency', 'set system syslog file messages any critical',
                       'set system syslog file messages authorization info', 'set system syslog file interactive-commands interactive-commands error',
                       'set system max-configurations-on-flash 5', 'set system max-configuration-rollbacks 5',
                       'set system license autoupdate url https://ae1.juniper.net/junos/key_retrieval', 'set interfaces ge-0/0/0 unit 0',
                       'set interfaces ge-0/0/1 unit 0 family inet address 10.151.125.162/25',
                       'set interfaces ge-0/0/2 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces ge-0/0/3 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces ge-0/0/4 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces ge-0/0/5 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces ge-0/0/6 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces ge-0/0/7 unit 0 family ethernet-switching vlan members vlan-trust',
                       'set interfaces vlan unit 0 family inet address 192.168.1.1/24',
                       'set vlans vlan-trust vlan-id 3', 'set vlans vlan-trust l3-interface vlan.0',
                       'set routing-options static route 0.0.0.0/0 next-hop 10.151.125.129',
                       'set protocols stp')

    security_commands = ('set security screen ids-option untrust-screen ip source-route-option',
                         'set security screen ids-option untrust-screen ip tear-drop',
                         'set security screen ids-option untrust-screen tcp syn-flood alarm-threshold 1024',
                         'set security screen ids-option untrust-screen tcp syn-flood attack-threshold 200',
                         'set security screen ids-option untrust-screen tcp syn-flood source-threshold 1024',
                         'set security screen ids-option untrust-screen tcp syn-flood destination-threshold 2048',
                         'set security screen ids-option untrust-screen tcp syn-flood timeout 20',
                         'set security screen ids-option untrust-screen tcp land',
                         'set security nat source rule-set trust-to-untrust from zone trust',
                         'set security nat source rule-set trust-to-untrust to zone untrust',
                         'set security nat source rule-set trust-to-untrust rule source-nat-rule match source-address 0.0.0.0/0',
                         'set security nat source rule-set trust-to-untrust rule source-nat-rule then source-nat interface',
                         'set security policies from-zone trust to-zone untrust policy trust-to-untrust match source-address any',
                         'set security policies from-zone trust to-zone untrust policy trust-to-untrust match destination-address any',
                         'set security policies from-zone trust to-zone untrust policy trust-to-untrust match application any',
                         'set security policies from-zone trust to-zone untrust policy trust-to-untrust then permit',
                         'set security policies default-policy permit-all',
                         'set security zones security-zone trust host-inbound-traffic system-services all',
                         'set security zones security-zone trust host-inbound-traffic protocols all')
    output = device.send_config_set(config_commands, exit_config_mode=False)
    output = device.send_config_set(security_commands, exit_config_mode=False)
    print(output)

def reset(device):
    output = device.send_command('rollback 0')
    print(output)

def backup(device):
    backup_commands = ('set system archival configuration transfer-interval 86400',
                       'set system archival configuration archive-sites "ftp://root@10.151.125.162:24/user" password"juniper123"')
    output = device.send_config_set(backup_commands, exit_config_mode=False)
    print(output)

def vlan_change(device):
    vlan_commands = ('delete interfaces ge-0/0/3 unit 0 family ethernet-switching vlan members vlan-trust',
                     'set vlans vlan-1 vlan-id 2', 'set vlans vlan-1 l3-interface vlan.1',
                     'set interfaces vlan unit 1 family inet address 10.10.1.4/24',
                     'set interfaces ge-0/0/3 unit 0 family ethernet-switching vlan members vlan-1',
                     'set security zones security-zone trust interfaces vlan.1',
                     'set security zones security-zone trust interfaces vlan.1 host-inbound-traffic system-services all',
                     'set security zones security-zone trust host-inbound-traffic protocols all')
    output = device.send_config_set(vlan_commands, exit_config_mode=False)
    print(output)

def firewall(device):
    firewall_commands = ('set firewall family inet filter ingress-port-filter term term-one from source-address 192.0.2.0',
                         'set firewall family inet filter ingress-port-filter term term-one then discard')
    output = device.send_config_set(firewall_commands, exit_config_ode=False)
    print(output)

def show(device):
    output = device.send_command('show interfaces')
    print(output)
    
try:
    type = 'juniper_os'
    ip = '10.151.125.162'
    username = 'root'
    password = 'juniper123'
    juniper = check_device(type, ip, username, password)
    configure(juniper)
    show(juniper)
except NetmikoTimeoutException as error:
    print('Wrong device information')
