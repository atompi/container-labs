```
mkdir -p data/{etcd0,etcd1,etcd2} certs
```

- 使用 https://github.com/atompi/self-signature 签发证书时使用的 CSR Json 文件：

```
cat > ../json/etcd-server-csr.json <<EOF
{
    "CN": "etcd",
    "hosts": [
        "0.0.0.0",
        "127.0.0.1",
        "etcd0",
        "etcd1",
        "etcd2"
    ],
    "key": {
        "algo": "rsa",
        "size": 4096
    },
    "names": [
        {
            "C": "CN",
            "ST": "Guangdong",
            "L": "Shenzhen",
            "O": "AtomPi",
            "OU": "AtomPi"
        }
    ]
}
EOF
```

```
cd ../out
../bin/cfssl gencert -ca=../ca/ca.pem -ca-key=../ca/ca-key.pem -config=../json/ca-config.json -profile=peer ../json/etcd-server-csr.json | ../bin/cfssljson -bare etcd

cp etcd*.pem certs
cp ../ca.pem certs
```

```
docker compose up -d
```

```
cat >> ~/.atompi.alias <<EOF
alias etcdctl="docker exec etcd0 etcdctl --endpoints=https://etcd0:2379,https://etcd1:2379,https://etcd2:2379 --cert=/certs/etcd.pem --key=/certs/etcd-key.pem --cacert=/certs/ca.pem"
EOF
```
