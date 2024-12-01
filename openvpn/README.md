# docker 部署 openvpn server

## 运行

构建镜像

```
cd docker
docker build -t atompi/openvpn:2.6.11 .
```

创建持久化目录

```
mkdir -p ./data/{dnsmasq,users,status,etc} logs
cp -r docker/conf/dnsmasq ./data/
```

创建服务

```
docker network create conpeer
docker-compose up -d
```

修改配置文件

````
vim ./data/dnsmasq/dnsmasq.hosts/common-hosts    # hosts
vim ./data/etc/server.conf    # server push
vim ./data/etc/client/sample.ovpn    # remote
```

重启服务

```
docker-compose restart
```
