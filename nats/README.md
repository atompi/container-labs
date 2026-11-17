```
mkdir -p data/{nats-1,nats-2,nats-3}

sudo apt install apache2-utils
htpasswd -bnBC 10 "" "change_me" | tr -d ':\n'


docker compose up -d
```
