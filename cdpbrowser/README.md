## CDP Browser

### Build

```
cd docker
docker build -t atompi/cdpbrowser:latest .
```

### Usage with OpenClaw

In your OpenClaw configuration (openclaw.json):

```
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "defaultProfile": "remote",
    "profiles": {
      "remote": {
        "cdpUrl": "http://localhost:9222",
        "color": "#FF4500"
      }
    }
  }
}
```
