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


def get_all_wiphy_info() -> list[dict]:
    """
    Get information about all wireless physical devices (wiphys).

    Returns:
        list[dict]: List of wiphy information dictionaries containing:
            - wiphy_name: Physical device name (e.g., 'phy0')
            - wiphy_index: Numeric index
            - interfaces: List of interface names using this wiphy
            - supported_modes: List of supported interface types
            - nan_supported: Boolean indicating NAN support

    Raises:
        RuntimeError: If no wireless devices found or query fails
    """
    iw = IW()
    try:
        # Get list of wireless physical devices (wiphys)
        wiphy_list = list(iw.list_wiphy())

        if not wiphy_list:
            raise RuntimeError("No wireless devices found")

        # Get all interfaces to map them to their wiphys
        iface_list = iw.get_interfaces_dump()

        # Build wiphy -> interfaces mapping
        wiphy_interfaces = {}
        for iface in iface_list:
            attrs_dict = dict(iface['attrs'])
            wiphy_idx = attrs_dict.get('NL80211_ATTR_WIPHY')
            ifname = attrs_dict.get('NL80211_ATTR_IFNAME')
            if wiphy_idx is not None and ifname is not None:
                if wiphy_idx not in wiphy_interfaces:
                    wiphy_interfaces[wiphy_idx] = []
                wiphy_interfaces[wiphy_idx].append(ifname)

        # Process each wiphy
        results = []
        for wiphy_data in wiphy_list:
            attrs_dict = dict(wiphy_data['attrs'])

            wiphy_idx = attrs_dict.get('NL80211_ATTR_WIPHY')
            wiphy_name = attrs_dict.get('NL80211_ATTR_WIPHY_NAME', 'unknown')
            supported_modes = attrs_dict.get('NL80211_ATTR_SUPPORTED_IFTYPES', [])

            # Check if NAN is in the supported modes
            nan_supported = 'nan' in [mode.lower() for mode in supported_modes]

            results.append({
                'wiphy_name': wiphy_name,
                'wiphy_index': wiphy_idx,
                'interfaces': wiphy_interfaces.get(wiphy_idx, []),
                'supported_modes': supported_modes,
                'nan_supported': nan_supported
            })

        return results

    finally:
        iw.close()
def main():
    """Main entry point for NAN support check."""
    try:
        wiphy_info_list = get_all_wiphy_info()

        print("WiFi Aware (NAN) Support Check")
        print("=" * 60)
        print()

        any_nan_supported = False

        for idx, wiphy_info in enumerate(wiphy_info_list):
            if idx > 0:
                print()
                print("-" * 60)
                print()

            print(f"Physical Device: {wiphy_info['wiphy_name']} (index: {wiphy_info['wiphy_index']})")

            # List interfaces
            if wiphy_info['interfaces']:
                print(f"Interfaces: {', '.join(wiphy_info['interfaces'])}")
            else:
                print("Interfaces: (none)")

            # List supported modes
            print(f"\nSupported interface modes:")
            for mode in wiphy_info['supported_modes']:
                marker = "✓" if mode.lower() == 'nan' else " "
                print(f"  {marker} {mode}")

            # NAN support status
            print()
            if wiphy_info['nan_supported']:
                print(f"✓ NAN support detected")
                print(f"  WiFi Aware functionality is available on this device.")
                any_nan_supported = True
            else:
                print(f"✗ NAN not supported")
                print(f"  WiFi Aware will not work with this device.")

        print()
        print("=" * 60)
        print()

        # Overall summary
        if any_nan_supported:
            print("✓ At least one device supports WiFi Aware (NAN)")
            sys.exit(0)
        else:
            print("✗ No devices support WiFi Aware (NAN)")
            print("  Consider using a USB WiFi adapter with NAN support.")
            sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        print(f"  Try running with sudo if you get permission errors.", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
