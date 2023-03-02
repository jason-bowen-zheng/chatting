# Chating
Chating is a B/S application built on fastapi and sqlchemy for talking to conversational AI.

An example of using [facebook/blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill) is built into it.

You can install dependencies and run chating:
```bash
pip install -r requirements.txt
python -m chating
```

Don't forget to create the database:
```python
from chating.db import engine, models
models.Base.metadata.create_all(engine)
```