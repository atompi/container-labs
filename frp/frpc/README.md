```
mkdir -p logs conf

cat > conf/frpc.toml <<EOF
user = "atompi"

serverAddr = "atompi.cc"
serverPort = 7000

log.to = "./logs/frpc.log"
log.level = "info"
log.maxDays = 3
log.disablePrintColor = true

auth.method = "token"
auth.token = "change_me"

transport.tls.enable = true
transport.tls.certFile = "server.crt"
transport.tls.keyFile = "server.key"
transport.tls.trustedCaFile = "ca.crt"


[[proxies]]
name = "test-tcp"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
transport.useEncryption = true
transport.useCompression = true
EOF
```

gen atompi.cc certs via [self-signature](https://github.com/atompi/self-signature) and copy to `conf/`
