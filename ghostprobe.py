
import argparse
import ipaddress
from scapy.all import ARP, Ether, srp

parser = argparse.ArgumentParser(
    description='GhostProbe - Network Discovery Tool',
    epilog='Examples:\n  python3 ghostprobe.py -i wlan0 -t 192.168.1.0/28\n  python3 ghostprobe.py -i wlan0 --ip 192.168.1.10 --mask 255.255.255.240',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('-i', '--interface', required=True, help='Network interface to use, e.g. wlan0')
parser.add_argument('-t', '--target', help='Target network in CIDR notation, e.g. 192.168.1.0/24')
parser.add_argument('--ip', help='Network IP address; must be used with --mask')
parser.add_argument('--mask', help='Subnet mask to use with --ip')

args = parser.parse_args()

if not args.target and not args.ip and not args.mask:
    parser.error('Specify either --target or both --ip and --mask.')

if args.ip and not args.mask:
    parser.error('--ip requires --mask.')

if args.mask and not args.ip:
    parser.error('--mask requires --ip.')

if args.target and (args.ip or args.mask):
    parser.error('Do not combine --target with --ip or --mask.')

if args.target:
    try:
        network = ipaddress.ip_network(args.target, strict=False)
    except ValueError:
        parser.error('Invalid target network specified.')
elif args.ip and args.mask:
    try:
        network = ipaddress.ip_network(f'{args.ip}/{args.mask}', strict=False)
    except ValueError:
        parser.error('Invalid IP address or subnet mask specified.')

if network.num_addresses > 4096:
    parser.error('Network is too large. Use a smaller, authorized target network.')

hosts = list(network.hosts())

if not hosts:
    parser.error('The specified network contains no usable host addresses.')

if args.interface not in __import__('scapy.all', fromlist=['get_if_list']).get_if_list():
    parser.error(f"Interface '{args.interface}' was not found.")

packets = []

for host in hosts:
    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=str(host))
    packets.append(packet)

try:
    ans, uans = srp(packets, timeout=2, iface=args.interface, verbose=False)
except PermissionError:
    parser.error('Permission denied. Run GhostProbe with sudo.')
except OSError as exc:
    parser.error(f'Network operation failed: {exc}')

devices = {}

for res in ans:
    devices[res.answer[ARP].psrc] = res.answer[ARP].hwsrc

print('\nGhostProbe - Network Discovery Results')
print(f'Target network: {network}')
print(f'Interface: {args.interface}')
print('-' * 48)
print(f'{"IP ADDRESS":<20} {"MAC ADDRESS":<20}')
print('-' * 48)

if devices:
    for ip, mac in devices.items():
        print(f'{ip:<20} {mac:<20}')
    print('-' * 48)
    print(f'Responding IP/MAC mappings: {len(devices)}')
else:
    print('No ARP responses received.')
