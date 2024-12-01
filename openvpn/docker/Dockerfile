FROM alpine:latest

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --update openvpn iptables bash easy-rsa unzip zip dnsmasq \
    && cp -r /usr/share/easy-rsa /etc/openvpn/ \
    && ln -s /etc/openvpn/easy-rsa/easyrsa /usr/local/bin \
    && mkdir -p /etc/openvpn/server/certs /etc/openvpn/client/keys /openvpn-docker/users /var/log/openvpn \
    && chown openvpn:openvpn /var/log/openvpn \
    && rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*

COPY conf/openvpn/server.conf /etc/openvpn/server.conf
COPY conf/sample.ovpn /etc/openvpn/client/sample.ovpn
COPY conf/vars /etc/openvpn/easy-rsa/vars
COPY scripts /openvpn-docker/scripts
RUN ln -sf /openvpn-docker/scripts/* /usr/local/bin/ \
    && chmod +x /openvpn-docker/scripts/*.sh \
    && mv /etc/openvpn /openvpn-docker/server

COPY conf/dnsmasq/dnsmasq.conf /etc/dnsmasq.conf
COPY conf/dnsmasq/resolv.dnsmasq /etc/resolv.dnsmasq

EXPOSE 1194/tcp 1194/udp

CMD ["entrypoint.sh"]
