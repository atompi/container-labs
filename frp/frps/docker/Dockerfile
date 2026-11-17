FROM alpine:3.26

WORKDIR /app

COPY . .

ENTRYPOINT ["/app/frps", "-c", "/app/frps.toml"]
