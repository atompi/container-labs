FROM alpine:3.26

WORKDIR /app

COPY . .

ENTRYPOINT ["/app/frpc", "-c", "/app/frpc.toml"]
