```
mkdir -p logs conf

cat > conf/frps.toml <<EOF
bindAddr = "0.0.0.0"
bindPort = 12590

transport.maxPoolCount = 5000

tls.force = true
transport.tls.certFile = "server.crt"
transport.tls.keyFile = "server.key"
transport.tls.trustedCaFile = "ca.crt"

enablePrometheus = true

log.to = "./logs/frps.log"
log.level = "info"
log.maxDays = 3
log.disablePrintColor = true

webServer.addr = "0.0.0.0"
webServer.port = 12570
webServer.user = "admin"
webServer.password = "secret_string"

auth.method = "token"
auth.token = "secret_string"

allowPorts = [
  { start = 32000, end = 32999 },
  { single = 80 },
  { single = 443 },
  { single = 25 },
  { single = 110 },
  { single = 143 },
  { single = 465 },
  { single = 587 },
  { single = 993 },
  { single = 995 }
]
EOF
```

gen atompi.cc certs via [self-signature](https://github.com/atompi/self-signature) and copy to `conf/`
