import argparse
import ipaddress

parser = argparse.ArgumentParser(description='GhostProbe - Network Discovery Tool')
parser.add_argument('-i', '--interface', required=True, help='Network interface to use for scanning')
parser.add_argument('-t','--target')
parser.add_argument('--ip')
parser.add_argument('--mask')
args = parser.parse_args()

if not args.target and not args.ip and not args.mask:
    parser.error('Either --target or both --ip and --mask must be specified.')
if args.ip and not args.mask:
    parser.error('If --ip is specified, --mask must also be specified.')
if args.mask and not args.ip:
    parser.error('If --mask is specified, --ip must also be specified.')
if args.target and (args.ip or args.mask):
    parser.error('Cannot specify both --target and --ip/--mask together.')
if args.target:
    try:
        network = ipaddress.ip_network(args.target, strict=False)
    except ValueError:
        parser.error('Invalid network specified.')
elif args.ip and args.mask:
    try:
        network = ipaddress.ip_network(f"{args.ip}/{args.mask}", strict=False)
    except ValueError:
        parser.error('Invalid network specified.')
