#Example of ICMP packets being send in a fast manner which usually is a sign of maliciouse activity


import scapy.all as scapy

#Sending the ICMP packet from destination IP to the source IP
def send_ICMP_packet(dst_ip, src_ip):
    scapy.send(scapy.IP(dst=dst_ip, src=src_ip)/scapy.ICMP())


dst_ip = "192.168.0.122"
src_ip = "192.168.0.172"

#This amount is defined by rule
amount_to_iterate_from_rule = 10

for i in range(amount_to_iterate_from_rule):
    send_ICMP_packet(dst_ip,src_ip)