import json
import numpy as np
import ollama

class MetaReflexion():
    def __init__ (self, model_name, judge_prompt, metajudge_prompt, improve_prompt, sys_prompt = None):
        self.model_name = model_name
        self.long_memory = []
        self.improve_prompt = improve_prompt
        self.metajudge_prompt = metajudge_prompt
        self.generational_args = {
            "max_new_tokens" : 256,
        }
        self.judge_prompt = judge_prompt
        self.sys_prompt = sys_prompt


    def generate_response(self, prompt, system_prompt, options = None):
        if generational_args == None:
            generational_args = self.generational_args
        output = ollama.generate(
            model = self.model_name,
            prompt = prompt,
            system = system_prompt,
            options = options,
            format = 'json'
        )
        return output


    def actor(self, task):
        output = self.generate_response(task, self.sys_prompt)
        output = output['response']
        output = json.loads(output)
        return output['response']

    def judge(self,task, response, max_judgements):
        options = {
            "temparature" : 0.7,
            "top_p":0.95
        }
        prompt = f"task:{task}\nresponse:{response}"
        judgements = []
        for i in range(0,max_judgements):
            temp = self.generate_response(prompt, self.judge_prompt, options)
            temp = temp['response']
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
                prompt =  f"UserQuestion:{question}\nResponse:{response}\nJudgement_a:{judgement_a}\nJudgement_b:{judgement_b}"
                output = self.generate_response(prompt, self.metajudge_prompt)
                output = output['response']
                output = json.loads(output)
                meta_judgements.append(output)

        #backward
        for i in range(length-1, 0, -1):
            judgement_a = judgements[i]
            for j in range(i-1, -1, -1):
                judgement_b = judgements[j]
                prompt =  f"UserQuestion:{question}\nResponse:{response}\nJudgement_a:{judgement_a}\nJudgement_b:{judgement_b}"
                output = self.generate_response(prompt, self.metajudge_prompt)
                output = output['response']
                output = json.loads(output)
                meta_judgements.append(output)

        return meta_judgements

    def get_dict_wins(self, meta_judgements, judgements):
        winner_dict = {i:0 for i in range (1, len(judgements)+1)}
        for i in meta_judgements:
            a = i["winner"]
            b = i[a]
            if b in judgements:
                k = judgements.index(b) + 1
                winner_dict[k] = winner_dict[k]+1

        return winner_dict

    def best_judgement_index(self, winner_dict):
        most_wins = max(winner_dict.values())
        best_judgement_index = [key-1 for key in winner_dict if winner_dict[key] == most_wins]
        return best_judgement_index


    def cal_variance_mean(self, judgements):
        appended_score = []
        for i in judgements:
            j = i["score"]
            appended_score.append(j)
        variance = np.var(appended_score)
        mean = np.mean(appended_score)
        return variance, mean


    def self_refine(self, task, output, best_judgement):
        prompt = f"response:{output}\nbest_judgement:{best_judgement}"
        improved_response = self.generate_response(prompt, self.improve_prompt)
        improved_response = improved_response['response']
        improved_response = json.loads(improved_response)
        return improved_response['improved_response']

    def run(self, task, max_iterations, max_judgements = 5):

        output = self.actor(task)

        for _ in range(max_iterations):
            judgements_arr = self.judge(task, output, max_judgements)
            variance, mean = self.cal_variance_mean(judgements_arr)

            if((variance >= 2.5) or (variance<= 2.5 and mean < 3.5)):
                meta_judgements = self.metajudge(task, output, judgements_arr)

                winner_dict = self.get_dict_wins(meta_judgements, judgements_arr)

                best_judgement_index =  self.best_judgement(winner_dict)
                best_judgement = judgements_arr[best_judgement_index]
                best_judgement = best_judgement["explanation"]

                output = self.self_refine(task, output, best_judgement)
            elif(variance <2.5 and mean >= 3.5):
                return output
