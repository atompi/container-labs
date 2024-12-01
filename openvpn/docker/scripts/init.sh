#!/bin/bash
mv /openvpn-docker/server/* /etc/openvpn
cd /etc/openvpn/easy-rsa
source /etc/openvpn/easy-rsa/vars
./easyrsa init-pki
echo ""|./easyrsa build-ca nopass
echo "yes"|./easyrsa build-server-full server nopass
./easyrsa gen-dh
./easyrsa gen-crl
openvpn --genkey secret ta.key
cd /etc/openvpn/server/certs/
cp /etc/openvpn/easy-rsa/pki/dh.pem ./
cp /etc/openvpn/easy-rsa/pki/ca.crt ./
cp /etc/openvpn/easy-rsa/pki/issued/server.crt ./
cp /etc/openvpn/easy-rsa/pki/private/server.key ./
cp /etc/openvpn/easy-rsa/ta.key ./
iptables -t nat -A POSTROUTING -s 192.168.254.0/24 -j MASQUERADE
touch /openvpn-docker/users/inited
