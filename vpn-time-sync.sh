#!/bin/bash
# vpn-time-sync.sh - keep system time synced with VPN timezone, no leaks

# Enable NTP for auto time sync
sudo timedatectl set-ntp true

# Get your current VPN IP's timezone from an online API (using curl)
VPN_IP=$(curl -s https://api.ipify.org)

# Grab timezone info from IP geolocation API (free tier, no keys)
TZ=$(curl -s "http://worldtimeapi.org/api/ip/$VPN_IP" | grep -Po '"timezone":"\K[^"]+')

if [ -z "$TZ" ]; then
  echo "Could not get timezone from VPN IP, defaulting to UTC"
  TZ="UTC"
fi

echo "Setting system timezone to $TZ"

# Set system timezone
sudo timedatectl set-timezone "$TZ"

# Show status for confirmation
timedatectl status
