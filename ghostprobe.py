import argparse

parser = argparse.ArgumentParser(description='NetDiscover - Network Discovery Tool')
parser.add_argument('-i', '--interface', required=True, help='Network interface to use for scanning')
parser.add_argument('-t','--target')
parser.add_argument('--ip')
parser.add_argument('--mask')
args = parser.parse_args()

