#!/bin/bash
# vpn-dns-webrtc-lockdown.sh
# Run this to block DNS leaks and prepare for WebRTC checks

# 1. Mark all DNS (UDP 53) packets going out tun0
sudo iptables -t mangle -A OUTPUT -p udp --dport 53 -o tun0 -j MARK --set-mark 0x1

# 2. Block any DNS (UDP 53) packets NOT going out tun0
sudo iptables -I OUTPUT ! -o tun0 -p udp --dport 53 -j DROP

# 3. Mark all traffic leaving via tun0 with mark 0x1 (if you haven’t done already)
sudo iptables -t mangle -A OUTPUT -o tun0 -j MARK --set-mark 0x1

# 4. Route marked packets through vpn table
sudo ip rule add fwmark 0x1 table vpn 2>/dev/null

# 5. Add default route via tun0 gateway to vpn table (adjust for your setup)
VPN_GW=$(ip route show dev tun0 | grep default | awk '{print $3}')
if [ -z "$VPN_GW" ]; then
  VPN_GW=$(ip route show dev tun0 | grep -m1 -oP 'via \K[\d.]+')
fi
sudo ip route add default via $VPN_GW dev tun0 table vpn 2>/dev/null

# 6. Lock down /etc/resolv.conf to VPN DNS servers (example: Cloudflare)
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
echo "nameserver 1.0.0.1" | sudo tee -a /etc/resolv.conf

echo "VPN DNS leak lockdown engaged, Chapta."
