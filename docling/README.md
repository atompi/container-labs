## haiku.rag

```
mkdir -p data/cache/{docling-serve/1,docling-serve/2,vllm/rerank,vllm/embedding}

# for cpu
docker compose -f docker-compose-cpu.yaml up -d

# for gpu
docker compose up -d
```
