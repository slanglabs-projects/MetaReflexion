import torch
from transformers import pipeline
from . import MODEL_PATH
#please do "hugging-face cli login" on your command prompt before you run this file this makes sure that you will access all repos even gated ones if you have permissions without any issue.

pipe = pipeline(
    "text-generation",
    model=MODEL_PATH,
    model_kwargs={"torch_dtype: torch.bfloat16"},
    device = "cuda"
)

terminators = [
    pipe.tokenizer.eos_token_id,
    pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]