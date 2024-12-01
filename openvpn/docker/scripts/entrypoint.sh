#!/bin/bash

if [[ -f '/openvpn-docker/users/inited' ]]; then
    echo "already inited, start openvpn server." > /var/log/openvpn/init.log
else
    init.sh
fi

iptables -t nat -A POSTROUTING -s 192.168.254.0/24 -j MASQUERADE

dnsmasq

exec openvpn --config /etc/openvpn/server.conf
