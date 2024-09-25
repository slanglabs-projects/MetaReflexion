from . import SYS_PROMPT, JUDGE_PROMPT, METAJUDGE_PROMPT, IMPROVE_PROMPT, MODEL_NAME
from downloadmodel import pipe
from hf_meta_reflexion import MetaReflexion


metareflexion_instance = MetaReflexion(
    model_name=pipe, 
    judge_prompt=JUDGE_PROMPT, 
    sys_prompt=SYS_PROMPT, 
    metajudge_prompt=METAJUDGE_PROMPT, 
    improve_prompt=IMPROVE_PROMPT
)

task = ""

output = metareflexion_instance.run(task, max_iterations=3, max_judgements=5)