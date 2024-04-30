from scapy.all import *
import random

from scapy.layers.inet import IP, TCP

RCV_PACKET_TIMEOUT = 3


def scapy_send_post_get(ip, deport, sport, path, user_agent, file_name, file_content):
    # Check if source port is 0
    if sport == 0:
        sport = random.randint(1025, 65500)

    # Craft the SYN packet to establish TCP connection
    syn_packet = IP(dst=ip) / TCP(dport=deport, sport=sport, flags="S")

    # Send SYN packet and receive SYN-ACK response
    syn_ack_response = sr1(syn_packet, verbose=False)

    if syn_ack_response:
        # Extract sequence and acknowledgment numbers
        seq_num = syn_ack_response[TCP].ack
        ack_num = syn_ack_response[TCP].seq + 1

        # Craft ACK packet to complete TCP handshake
        ack_packet = IP(dst=ip) / TCP(dport=deport, sport=sport,
                                      flags="A", seq=seq_num, ack=ack_num)
        send(ack_packet, verbose=False)

        # Craft HTTP POST request with file content
        http_post_request = (
            b'POST ' + path.encode() + b' HTTP/1.1\r\n'
            b'Host: ' + ip.encode() + b':' + str(deport).encode() + b'\r\n'
            b'Connection: keep-alive\r\n'
            b'User-Agent: ' + user_agent.encode() + b' (Windows NT 10.0; Win64; x64)\r\n'
            b'Content-Type: multipart/form-data; '
            b'boundary=boundary123\r\n'
            b'\r\n'
            b'--boundary123\r\n'
            b'Content-Disposition: form-data; name="file"; filename="' + file_name.encode() + b'"\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            ) + file_content + (
            b'\r\n'
            b'--boundary123--\r\n'
            )

        print(http_post_request)

        # Send HTTP POST request within established TCP connection
        http_request_packet = IP(dst=ip) / TCP(dport=deport, sport=sport,
                                               flags="A", seq=seq_num, ack=ack_num) / http_post_request
        response = sr1(http_request_packet, verbose=False)

        if not response:
            raise ValueError("Response is None")

    else:
        raise ValueError("SYN-ACK response is None")
