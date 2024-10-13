import socket
import struct

# تنظیمات سوکت برای دریافت بسته‌ها از همه پروتکل‌ها (شامل Ethernet)
def create_raw_socket():
    try:
        # ایجاد سوکت خام برای دریافت بسته‌های Ethernet
        raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        return raw_socket
    except Exception as e:
        print(f"Error creating raw socket: {e}")
        exit()

# تابع برای تحلیل هدر Ethernet
def parse_ethernet_header(data):
    ethernet_header = struct.unpack('!6s6sH', data[:14])
    dest_mac = ':'.join(format(b, '02x') for b in ethernet_header[0])
    src_mac = ':'.join(format(b, '02x') for b in ethernet_header[1])
    eth_protocol = socket.ntohs(ethernet_header[2])
    return dest_mac, src_mac, eth_protocol

# تابع برای تحلیل هدر IP
def parse_ip_header(data):
    ip_header = data[14:34]
    unpacked_header = struct.unpack('!BBHHHBBH4s4s', ip_header)
    
    version_ihl = unpacked_header[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    
    src_ip = socket.inet_ntoa(unpacked_header[8])
    dest_ip = socket.inet_ntoa(unpacked_header[9])
    
    return src_ip, dest_ip, unpacked_header

# تابع برای تحلیل هدر TCP
def parse_tcp_header(data):
    tcp_header = data[34:54]
    unpacked_header = struct.unpack('!HHLLBBHHH', tcp_header)
    
    src_port = unpacked_header[0]
    dest_port = unpacked_header[1]
    
    return src_port, dest_port, unpacked_header

# تابع برای تحلیل هدر UDP
def parse_udp_header(data):
    udp_header = data[34:42]
    unpacked_header = struct.unpack('!HHHH', udp_header)
    
    src_port = unpacked_header[0]
    dest_port = unpacked_header[1]
    
    return src_port, dest_port, unpacked_header

# تابع اصلی برای شنود و نمایش بسته‌ها در تمام لایه‌ها
def sniff_packets():
    raw_socket = create_raw_socket()
    print("Starting packet sniffing...")
    
    while True:
        data, addr = raw_socket.recvfrom(65535)
        
        # تحلیل هدر Ethernet
        dest_mac, src_mac, eth_protocol = parse_ethernet_header(data)
        print(f"Ethernet Frame: {src_mac} -> {dest_mac} | Protocol: {eth_protocol}")
        
        # بررسی اینکه آیا پروتکل اترنت IP است
        if eth_protocol == 8:  # IPv4
            # تحلیل هدر IP
            src_ip, dest_ip, ip_header = parse_ip_header(data)
            print(f"IP Packet: {src_ip} -> {dest_ip} | Header: {ip_header}")
            
            # بررسی پروتکل‌های بالاتر (TCP/UDP)
            ip_protocol = ip_header[6]  # مقدار پروتکل در هدر IP
            if ip_protocol == 6:  # TCP
                src_port, dest_port, tcp_header = parse_tcp_header(data)
                print(f"TCP Segment: {src_ip}:{src_port} -> {dest_ip}:{dest_port} | Header: {tcp_header}")
            elif ip_protocol == 17:  # UDP
                src_port, dest_port, udp_header = parse_udp_header(data)
                print(f"UDP Datagram: {src_ip}:{src_port} -> {dest_ip}:{dest_port} | Header: {udp_header}")

if __name__ == "__main__":
    sniff_packets()
