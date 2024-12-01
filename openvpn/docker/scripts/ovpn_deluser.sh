#!/bin/bash

set -e

OVPN_USER_KEYS_DIR=/etc/openvpn/client/keys
EASY_RSA_DIR=/etc/openvpn/easy-rsa
PKI_DIR=$EASY_RSA_DIR/pki

for user in "$@"
do
  cd $EASY_RSA_DIR

  echo -e 'yes\n' | ./easyrsa revoke $user
  ./easyrsa gen-crl

  if [ -d "$OVPN_USER_KEYS_DIR/$user" ];
  then
    rm -rf $OVPN_USER_KEYS_DIR/${user}*
  fi
  sed -i '/'"$user"'/d' $PKI_DIR/index.txt
  rm -f /openvpn-docker/users/$user.zip
  kill -SIGHUP `ps -ef | grep openvpn\ \-\-config|grep -v grep|awk '{print $1}'`
done

exit 0
