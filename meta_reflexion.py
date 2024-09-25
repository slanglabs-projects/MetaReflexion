import subprocess
import os
from constants import MODEL_NAME
from prompts import JUDGE_PROMPT, METAJUDGE_PROMPT, IMPROVE_PROMPT, SYS_PROMPT
from huggingface import hf_meta_reflexion, downloadmodel
from ollama import ollama_meta_reflexion


task = ""

def main():
    print("Select an option:")
    print("h for HuggingFace")
    print("o for Ollama")
    
    user_choice = input("Enter your choice: ").strip().lower()
    
    if user_choice == 'h':
        print("HuggingFace selected.")

        result = downloadmodel.download_model()
        pipe = result['pipe']
        terminators = result['terminators']

        meta_reflexion = hf_meta_reflexion.MetaReflexion(
            model=pipe,
            judge_prompt=JUDGE_PROMPT,
            metajudge_prompt=METAJUDGE_PROMPT,
            improve_prompt=IMPROVE_PROMPT, 
            sys_prompt=SYS_PROMPT
        )

        meta_reflexion.generational_args["eos_token_id"] = terminators

        task = "Your task prompt"
        output = meta_reflexion.run(task, max_iterations=3, max_judgements=5)
        
    elif user_choice == 'o':
        print("Ollama selected.")

        metareflexion_instance = ollama_meta_reflexion.MetaReflexion(
            model_name=MODEL_NAME, 
            judge_prompt=JUDGE_PROMPT, 
            sys_prompt=SYS_PROMPT, 
            metajudge_prompt=METAJUDGE_PROMPT, 
            improve_prompt=IMPROVE_PROMPT
        )

        task = ""

        output = metareflexion_instance.run(task, max_iterations=3, max_judgements=5)

    else:
        print("Invalid choice. Please run the file again and select 'h' or 'o'.")

if __name__ == "__main__":
    main()
