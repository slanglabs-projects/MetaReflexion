import torch
from transformers import pipeline
from huggingface import MODEL_PATH

# Please do "hugging-face cli login" on your command prompt before running this file.

def download_model():
    pipe = pipeline(
        "text-generation",
        model=MODEL_PATH,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda"
    )

    terminators = [
        pipe.tokenizer.eos_token_id,
        pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    # Output as JSON
    output = {
        "pipe": pipe,
        "terminators": terminators
    }
    return output 

if __name__ == "__main__":
    download_model()