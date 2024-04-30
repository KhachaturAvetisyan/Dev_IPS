from scapy.all import *
from scapy.layers.inet import IP, TCP
import random

RCV_PACKET_TIMEOUT = 3

def scapy_send_http_get(ip, deport, sport, path, user_agent):
    # Check if source port is 0
    if sport == 0:
        sport = random.randint(1025, 65500)

    # Craft the SYN packet to establish TCP connection
    syn_packet = IP(dst=ip) / TCP(dport=deport, sport=sport, flags="S")

    # Send SYN packet and receive SYN-ACK response
    syn_ack_response = sr1(syn_packet, verbose=False, timeout=RCV_PACKET_TIMEOUT)

    if syn_ack_response:
        # Extract sequence and acknowledgment numbers
        seq_num = syn_ack_response[TCP].ack
        ack_num = syn_ack_response[TCP].seq + 1

        # Craft ACK packet to complete TCP handshake
        ack_packet = IP(dst=ip) / TCP(dport=deport, sport=sport,
                                      flags="A", seq=seq_num, ack=ack_num)

        # Send ACK packet
        send(ack_packet, verbose=False, timeout=RCV_PACKET_TIMEOUT)

        # Craft HTTP GET request
        http_get_request = (
            b'GET ' + path.encode() + b' HTTP/1.1\r\n'
            b'Host: ' + ip.encode() + b':' + str(deport).encode() + b'\r\n'
            b'Connection: keep-alive\r\n'
            b'Cache-Control: max-age=0\r\n'
            b'Upgrade-Insecure-Requests: 1\r\n'
            b'User-Agent: ' + user_agent.encode() + b' (Windows NT 10.0; Win64; x64)\r\n'
            b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
            b'image/webp,image/apng,'
            b'*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n'
            b'Accept-Encoding: gzip,deflate\r\n'
            b'Accept-Language: en-US,en;q=0.9\r\n\r\n'
        )

        print(http_get_request)

        # Create HTTP GET request within established TCP connection
        http_request_packet = IP(dst=ip) / TCP(dport=deport, sport=sport,
                                               flags="A", seq=seq_num, ack=ack_num) / http_get_request

        # Send HTTP GET request and receive response
        response = sr1(http_request_packet, verbose=False, timeout=RCV_PACKET_TIMEOUT)

        if not response:
            raise ValueError("Response is None")

    else:
        raise ValueError("SYN-ACK response is None")
