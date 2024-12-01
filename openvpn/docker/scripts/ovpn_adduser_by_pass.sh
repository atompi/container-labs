#!/bin/bash

set -e

OVPN_USER_KEYS_DIR=/etc/openvpn/client/keys
EASY_RSA_DIR=/etc/openvpn/easy-rsa
PKI_DIR=$EASY_RSA_DIR/pki

user=$1
pass=$2

if [ -d "$OVPN_USER_KEYS_DIR/$user" ];
then
rm -rf $OVPN_USER_KEYS_DIR/$user
rm -rf  $PKI_DIR/reqs/$user.req
sed -i '/'"$user"'/d' $PKI_DIR/index.txt
fi
cd $EASY_RSA_DIR
(echo $pass;echo "yes")|./easyrsa --passout=stdin build-client-full $user
mkdir -p $OVPN_USER_KEYS_DIR/$user
cp $PKI_DIR/ca.crt $OVPN_USER_KEYS_DIR/$user/
cp $PKI_DIR/issued/$user.crt $OVPN_USER_KEYS_DIR/$user/
cp $PKI_DIR/private/$user.key $OVPN_USER_KEYS_DIR/$user/
cp /etc/openvpn/client/sample.ovpn $OVPN_USER_KEYS_DIR/$user/$user.ovpn
sed -i 's/user/'"$user"'/g' $OVPN_USER_KEYS_DIR/$user/$user.ovpn
cp /etc/openvpn/server/certs/ta.key $OVPN_USER_KEYS_DIR/$user/ta.key
cd $OVPN_USER_KEYS_DIR
zip -r $user.zip $user
mv $user.zip /openvpn-docker/users/$user.zip

exit 0
