from queue import Queue
from time import sleep

from chatting.db.crud import *
from transformers import (BlenderbotForConditionalGeneration,
                          BlenderbotTokenizerFast)

msg_queue = Queue()


def generate_loop():
    model_name = "facebook/blenderbot-400M-distill"
    tokenizer = BlenderbotTokenizerFast.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    while True:
        try:
            user_uuid, msg = msg_queue.get_nowait()
        except:
            sleep(0.01)
        else:
            if user_uuid == "system":
                if msg == "shutdown":
                    break
            else:
                history = get_dialog(user_uuid)
                dialog = "</s> <s>".join([str(elem)
                                         for elem in history[len(history)-3:]])
                input_ids = tokenizer(
                    [(dialog)], return_tensors="pt", max_length=512, truncation=True)
                next_reply_ids = model.generate(
                    **input_ids, max_length=512, pad_token_id=tokenizer.eos_token_id)
                msg = tokenizer.batch_decode(
                    next_reply_ids, skip_special_tokens=True)[0]
                new_dialog(user_uuid, 1, msg)
