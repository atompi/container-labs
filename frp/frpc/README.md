```
mkdir -p logs conf

cat > conf/frpc.toml <<EOF
user = "atompi"

serverAddr = "atompi.cc"
serverPort = 12590

log.to = "./logs/frpc.log"
log.level = "info"
log.maxDays = 3
log.disablePrintColor = true

auth.method = "token"
auth.token = "secret_string"

transport.tls.enable = true
transport.tls.certFile = "server.crt"
transport.tls.keyFile = "server.key"
transport.tls.trustedCaFile = "ca.crt"

[[proxies]]
name = "test"
type = "tcp"
localIP = "192.168.220.128"
localPort = 80
remotePort = 80
transport.useEncryption = true
transport.useCompression = true
EOF
```

gen atompi.cc certs via [self-signature](https://github.com/atompi/self-signature) and copy to `conf/`
