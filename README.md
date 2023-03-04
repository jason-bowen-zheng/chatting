# Chatting
Chatting is a B/S application built on fastapi and sqlchemy for talking to conversational AI.

An example of using [facebook/blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill) is built into it.

You can install dependencies and run chatting:
```bash
pip install -r requirements.txt
python -m chatting
```

Don't forget to create the database:
```python
from chatting.db import engine, models
models.Base.metadata.create_all(engine)
```
