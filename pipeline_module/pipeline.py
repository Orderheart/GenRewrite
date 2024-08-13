import sys
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import random
from pipeline_module.gpt import GPT
from correct_module.correct_candidate_rewrite import Nlr2Correction
from evaluate_module.evaluate_rewrite import EvaluateRewrite
from suggest_module.suggest_candidate_rewrite import suggest_candidate_rewrite
from suggest_module.suggest_group_rewrite import sugget_group_rewrite
from suggest_module.suggest_select_rewrite import suggest_select_rewrite

class GenRewrite:
    def __init__(self, queries, gpt, tester, budget, min_speedup,reportory_path):
        self.queries = queries
        self.gpt = GPT()
        self.tester = tester # what is tester ?? to be reconsidered.
        self.budget = budget
        self.min_speedup = min_speedup
        self.json_path = reportory_path
        self.res = []
        self.rewrite_rules = []

    # done
    def suggest_and_explain(self, query,hints):
        # Placeholder for suggesting and explaining rewrites using LLM and rewrite rules
        suggest = suggest_candidate_rewrite(self.gpt, query, hints)
        candidate_rewrite, explanation = suggest.suggest_and_explain(query, hints)
        return candidate_rewrite, explanation

    def suggest_group_rewrite(self, query, hints):
        
    # done
    def suggest_select_rewrite(self, input_query):
        selector = suggest_select_rewrite(self.json_path)
        best_nlr2s = selector.select_best_nlr2(input_query)[::-1] 
        return best_nlr2s
        

    # done
    def correct_for_equivalence(self, original_query, rewritten_query):
        # Placeholder for correcting the rewrite to ensure semantic equivalence
        correction = Nlr2Correction(original_query, rewritten_query)
        corrected_query = correction.correct_query()
        return corrected_query

    # done 
    def evaluate_rewrite(self, original_query, rewritten_query):
        # Placeholder for evaluating the rewrite
        # Here, we randomly determine if the rewritten query is equivalent and estimate the speedup
        # test = Evaluate_rewrite_model("./postgres.json")
        # speed_up = test.evalutate(input_query, rewrite_query_1)
        # print(f"Speedup: {speed_up:.2f}")
        evalute = EvaluateRewrite(self.json_path)
        is_equiv = random.choice([True, False])
        speedup = random.uniform(1, 10)
        return is_equiv, speedup
    
    def update_rules(self, explanation, speedup):
        # Placeholder for updating rewrite rules based on explanations and speedups
        self.rewrite_rules.append((explanation, speedup))



    def run(self):
        while self.queries:
            for query in self.queries:
                rewritten_query, explanation = self.suggest_and_explain(query,hints)
                corrected_query = self.correct_for_equivalence(query, rewritten_query)
                is_equiv, speedup = self.evaluate_rewrite(query, corrected_query)

                if is_equiv:
                    self.update_rules(explanation, speedup)
                    if speedup > self.min_speedup:
                        self.res.append((query, corrected_query, explanation))

            # Check termination condition
            if not self.queries or len(self.res) >= self.budget:
                return self.res

            # Remove optimized queries from the original set
            self.queries = [q for q in self.queries if q not in [r[0] for r in self.res]]

        return self.res

