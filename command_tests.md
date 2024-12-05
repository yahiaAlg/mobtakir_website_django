```bash
curl -X POST http://0.0.0.0:11434/api/generate -d '{"prompt": "hi there", "model": "phi3", "system": "you are a casual person", "format": ""}'
```

```json
{
    "prompt": "hi there",
    "model": "phi3",
    "system": "you are a casual person",
    "format": "",
}

```