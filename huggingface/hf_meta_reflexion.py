import json
import numpy as np

class MetaReflexion():
    def __init__ (self,model,judge_prompt, metajudge_prompt, improve_prompt, sys_prompt = None):
        self.model = model
        self.long_memory = []
        self.improve_prompt = improve_prompt
        self.metajudge_prompt = metajudge_prompt
        self.generational_args = {
            "max_new_tokens" : 256,
            "do_sample": True,
            "temperature" : 0.7,
            "eos_token_id": None
        }
        self.judge_sys_prompt = judge_prompt
        self.sys_prompt = sys_prompt


    def generate_response(self, messages, generational_args = None):
        if generational_args == None:
            generational_args = self.generational_args
        output = self.model(
            messages,
            **generational_args
        )
        return output


    def actor(self, task, context=None):
        messages = [
            {"role": "system", "content": f"{self.sys_prompt}{context}"},
            {"role": "user", "content": f"{task}"},
        ]
        output = self.generate_response(messages)
        output = output[0]["generated_text"][-1]
        output = json.loads(output['content'])
        return output

    def judge(self, task, response, max_judgements=5):
        generation_args_judge = {
            "max_new_tokens" :256,
            "temparature" : 0.7,
            "top_p":0.95,
            "eos_token_id": self.generational_args["eos_token_id"]

        }
        messages = [
            {"role": "system", "content": f"{self.judge_sys_prompt}"},
            {"role": "user", "content": f"{response}"}
        ]
        judgements = []
        for i in range(0,max_judgements):
            temp = self.generate_response(messages, generation_args_judge)[0]["generated_text"][-1]
            temp = temp['content']
            print(temp)
            temp = json.loads(temp)
            judgements.append(temp)
        return judgements

    def metajudge(self, question, response, judgements):
        #forward
        meta_judgements = []
        length = len(judgements)
        for i in range(0,length-1):
            judgement_a = judgements[i]
            for j in range(i+1,length):
                judgement_b = judgements[j]
                messages = [
                    {"role":"system","content": self.metajudge_prompt},
                    {"role": "user","content": f"UserQuestion:{question}\nResponse:{response}\nJudgement_a:{judgement_a}\nJudgement_b:{judgement_b}\n"}
                ]
                output = self.generate_response(messages)[0]["generated_text"][-1]
                output = output['content']
                output = json.loads(output)
                meta_judgements.append(output)

        #backward
        for i in range(length-1, 0, -1):
            judgement_a = judgements[i]
            for j in range(i-1, -1, -1):
                judgement_b = judgements[j]
                messages = [
                    {"role":"system","content": self.metajudge_prompt},
                    {"role": "user","content": f"UserQuestion:{question}\nResponse:{response}\nJudgement_a:{judgement_a}\nJudgement_b:{judgement_b}\n"}
                ]
                output = self.generate_response(messages)[0]["generated_text"][-1]
                output = output['content']
                print(output)
                output = json.loads(output)
                meta_judgements.append(output)

        return meta_judgements

    def get_dict_wins(self, meta_judgements, judgements):
        winner_dict = {i:0 for i in range (1, len(judgements)+1)}
        for i in meta_judgements:
            a = i["winner"]
            b = i[a]
            if b in judgements:
                k = judgements.index(b)
                winner_dict[k+1] = winner_dict[k+1]+1

        return winner_dict

    def best_judgement_index(self, winner_dict):
        most_wins = max(winner_dict.values())
        best_judgement_index = [key-1 for key in winner_dict if winner_dict[key] == most_wins]
        return best_judgement_index


    def memory(self, task, output, best_judgement):
        if len(self.long_memory) > 10:
            self.long_memoty.pop(0)
        self.long_memory.append((task, output, best_judgement))

    def cal_variance_mean(self, judgements):
        appended_score = []
        for i in judgements:
            score = i.get("score", None)
            if score is not None:
                try:
                    score = float(score)
                    appended_score.append(score)
                except ValueError:
                    print("Warning: 'score' is not a valid number in one of the judgements:", i)
            else:
                print("Warning: 'score' key is missing in one of the judgements:", i)
        
        if not appended_score:
            raise ValueError("No valid scores found for variance and mean calculation.")
        
        variance = np.var(appended_score)
        mean = np.mean(appended_score)
        return variance, mean

    def returncontext(self):
        context = ""
        for mem in self.long_memory :
            context += f"Task: {mem[0]}\nOutput: {mem[1]}\nBest_feedback: {mem[2]}\n\n"
        if context == "":
            return None
        return context

    def self_refine(self, task, output, best_judgement):
        messages = [
            {"role":"system", "content":f"{self.improve_prompt}"},
            {"role":"user","content":f"response : {output} \n\n judgement:{best_judgement}"}
        ]
        improved_response = self.generate_response(messages)[0]["generated_text"][-1]
        improved_response = improved_response['content']
        return improved_response

    def run(self, task, max_iterations, max_judgements = 5):

        context = self.returncontext()
        output = self.actor(task, context)

        for iteration in range(max_iterations):
            judgements_arr = self.judge(task, output, max_judgements)

            variance, mean = self.cal_variance_mean(judgements_arr)
            if((variance >= 2.5) or (variance<= 2.5 and mean < 3.5)):
                meta_judgements = self.metajudge(task, output, judgements_arr)

                winner_dict = self.get_dict_wins(meta_judgements, judgements_arr)

                best_judgement_index =  self.bestJudgement(winner_dict)
                bestJudgement = judgements_arr[best_judgement_index]
                bestJudgement = bestJudgement["explanation"]

                output = self.self_refine(task, output, bestJudgement)


            elif(variance <2.5 and mean >= 3.5):
                return output