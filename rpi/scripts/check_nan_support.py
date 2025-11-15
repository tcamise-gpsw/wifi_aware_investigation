#!/usr/bin/env python3
"""
Check WiFi Aware (NAN) support on Raspberry Pi wireless interface.

This script queries the Linux kernel's nl80211 netlink API to determine
if the wireless hardware and driver support NAN (Neighbor Awareness Networking)
operations required for WiFi Aware functionality.

References:
- pyroute2 Documentation: https://pyroute2.org/
- Linux nl80211 API: https://www.kernel.org/doc/html/latest/userspace-api/netlink/intro.html
- nl80211.h Interface Types: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/nl80211.h
  (see enum nl80211_iftype for NL80211_IFTYPE_NAN)

Usage:
    python check_nan_support.py [interface]

    interface: Wireless interface name (default: wlan0)

Example:
    python check_nan_support.py
    python check_nan_support.py wlan0
"""

import sys
from pyroute2 import IW


def check_nan_support(interface: str = 'wlan0') -> bool:
    """
    Check if wireless interface supports NAN (Neighbor Awareness Networking) mode.

    Uses nl80211 netlink interface to query supported interface types.
    The NL80211_IFTYPE_NAN interface type indicates hardware and driver support
    for WiFi Aware/NAN operations.

    Args:
        interface: Wireless interface name (e.g., 'wlan0')

    Returns:
        bool: True if NAN is supported, False otherwise

    Raises:
        KeyError: If interface doesn't exist
        PermissionError: If insufficient permissions to query netlink
    """
    iw = IW()
    try:
        # Get physical device (wiphy) for this interface
        phyname = iw.get_interface_by_ifname(interface)['attrs']['NL80211_ATTR_WIPHY']

        # Query wiphy capabilities
        wiphy = iw.get_wiphy(phyname)

        # Check supported interface types for NL80211_IFTYPE_NAN
        for attr in wiphy['attrs']:
            if attr[0] == 'NL80211_ATTR_SUPPORTED_IFTYPES':
                modes = [mode[1]['nla'][1] for mode in attr[1]['attrs']]
                if 'NL80211_IFTYPE_NAN' in modes:
                    return True
        return False
    finally:
        iw.close()


def main():
    """Main entry point for NAN support check."""
    # Get interface from command line or use default
    interface = sys.argv[1] if len(sys.argv) > 1 else 'wlan0'

    try:
        if check_nan_support(interface):
            print(f"✓ NAN support detected on interface '{interface}'")
            print("  WiFi Aware functionality should be available.")
            sys.exit(0)
        else:
            print(f"✗ NAN not supported on interface '{interface}'")
            print("  WiFi Aware will not work with this hardware/driver combination.")
            print("  Consider using a USB WiFi adapter with NAN support.")
            sys.exit(1)

    except KeyError:
        print(f"✗ Error: Interface '{interface}' not found", file=sys.stderr)
        print("  Available interfaces:", file=sys.stderr)

        # Try to list available wireless interfaces
        try:
            iw = IW()
            interfaces = iw.get_interfaces()
            for iface in interfaces:
                ifname = dict(iface['attrs']).get('NL80211_ATTR_IFNAME', 'unknown')
                print(f"    - {ifname}", file=sys.stderr)
            iw.close()
        except Exception:
            print("    (unable to enumerate interfaces)", file=sys.stderr)

        sys.exit(2)

    except PermissionError:
        print(f"✗ Error: Insufficient permissions to query interface '{interface}'", file=sys.stderr)
        print("  Try running with sudo: sudo python check_nan_support.py", file=sys.stderr)
        sys.exit(3)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == '__main__':
    main()
