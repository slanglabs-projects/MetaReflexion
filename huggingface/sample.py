from huggingface import SYS_PROMPT, JUDGE_PROMPT, METAJUDGE_PROMPT, IMPROVE_PROMPT
from downloadmodel import download_model
from hf_meta_reflexion import MetaReflexion

def main():
    # Download the model and terminators
    result = download_model()
    pipe = result['pipe']
    terminators = result['terminators']

    # Initialize the MetaReflexion object with the downloaded model and terminators
    meta_reflexion = MetaReflexion(
        model=pipe,
        judge_prompt=JUDGE_PROMPT,
        metajudge_prompt=METAJUDGE_PROMPT,
        improve_prompt=IMPROVE_PROMPT, 
        sys_prompt=SYS_PROMPT
    )

    # Set the terminators in the generational args
    meta_reflexion.generational_args["eos_token_id"] = terminators

    # Now, you can proceed with using the MetaReflexion class
    task = "Your task prompt"
    output = meta_reflexion.run(task, max_iterations=3, max_judgements=5)

    print(output)

if __name__ == "__main__":
    main()