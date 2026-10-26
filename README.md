# GhostProbe 👻

GhostProbe is a Python-based local network discovery tool that uses ARP (Address Resolution Protocol) to identify responding IP addresses and their corresponding MAC addresses on a network.

It is designed for authorized network discovery, home labs, and cybersecurity learning environments.

## Features

- Discover responding hosts on a local IPv4 network using ARP.
- Display IP address and MAC address mappings.
- Accept targets in CIDR notation or an IP address with a subnet mask.
- Select the network interface used for discovery.
- Validate command-line arguments before scanning.
- Display results in a readable table.

## Requirements

- Python 3
- [Scapy](https://scapy.net/)
- Linux (developed and tested on Kali Linux). Other platforms supported by Scapy have not been tested.
- Root privileges to send ARP packets

## Installation

Clone the repository:

```bash
git clone https://github.com/cyberghost-x/GhostProbe.git
cd GhostProbe
```

Install Scapy. On Kali and other Debian-based systems, the simplest option is:

```bash
sudo apt install python3-scapy
```

GhostProbe is run with `sudo`, so Scapy must be available to root's Python. A Scapy installed with `pip` for your normal user may not be visible there, and recent Python versions may refuse a plain `pip install` outside a virtual environment. If you use a virtual environment, run GhostProbe with that environment's Python, for example:

```bash
sudo ./venv/bin/python ghostprobe.py -i wlan0 -t 192.168.1.0/28
```

## Usage

GhostProbe requires a network interface and either a target network in CIDR notation or an IP address and subnet mask.

**Option 1: Specify a target network**

```bash
sudo python3 ghostprobe.py -i wlan0 -t 192.168.1.0/28
```

**Option 2: Specify an IP address and subnet mask**

```bash
sudo python3 ghostprobe.py -i wlan0 --ip 192.168.1.10 --mask 255.255.255.240
```

Replace `wlan0` with your actual network interface (find it with `ip a` or `ifconfig`) and use an IP range belonging to a network you are authorized to test.

Give the target in one way only: `-t`, or `--ip` together with `--mask`.

### Permissions

Sending ARP requests uses raw network access, which Linux only allows for root. Run GhostProbe with `sudo`. Without it, GhostProbe reports a permissions error and does not scan.

## Example Output

```text
GhostProbe - Network Discovery Results
Target network: 192.168.1.0/28
Interface: wlan0
------------------------------------------------
IP ADDRESS           MAC ADDRESS
------------------------------------------------
192.168.1.1          aa:bb:cc:dd:ee:ff
192.168.1.5          11:22:33:44:55:66
------------------------------------------------
Responding IP/MAC mappings: 2
```

The addresses above are illustrative examples, not results from an actual scan.

## How It Works

1. Parses and validates the command-line arguments.
2. Determines the target IPv4 network.
3. Generates ARP requests for usable host addresses in that network.
4. Sends the requests through the selected network interface.
5. Collects ARP responses and extracts the responding IP addresses and MAC addresses.
6. Displays the discovered mappings.

## Limitations

- GhostProbe currently performs ARP-based discovery only; it is not a port scanner.
- ARP discovery is limited to the local Layer 2 network of the selected interface. It does not cross routers.
- Devices that do not respond to ARP requests may not appear in the results.
- Scan size is limited to 4,096 total network addresses per run. Larger targets are refused, so scan a smaller range.
- Results can differ between runs. Wi-Fi can drop frames, and replies that arrive after the short waiting period are missed, so a device that is online may not always appear.
- Multiple IP addresses may map to the same MAC address, depending on network configuration and proxy ARP behavior. GhostProbe reports what it receives and does not interpret it.
- The tool does not currently identify device vendors or guarantee that every responding IP represents a unique physical device.

## Responsible Use

Use GhostProbe only on networks you own or have explicit permission to assess. Avoid scanning large or shared networks without authorization.

## Project Status

GhostProbe is under active development. The current version focuses on basic ARP-based IP and MAC address discovery, and is being tested on small authorized networks.

## Author

GitHub: [@cyberghost-x](https://github.com/cyberghost-x)
