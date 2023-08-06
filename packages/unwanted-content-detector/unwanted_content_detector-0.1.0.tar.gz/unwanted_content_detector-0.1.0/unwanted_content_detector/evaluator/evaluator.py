import random

from data.loader import load_data
from unwanted_content_detector.entities import Label


def random_guess(_):
    return random.choice([Label.UNWANTED_CONTENT.value, Label.SAFE_CONTENT.value])


class Evaluator:
    """
    Performs evaluation on the complete set
    """

    def evaluate_distilbert(self):
        from unwanted_content_detector.models.distilbert_finetuned.inference import Inference
        inference = Inference()
        return self.evaluate_function(inference.infer)



    def evaluate_random(self):
        self.evaluate_function(random_guess)


    def evaluate_function(self, fn):
        """ Evaluates the entire dataset in a given model """
        from unwanted_content_detector.models.distilbert_finetuned.inference import Inference
        data = load_data()

        Y = data.iloc[:, -1:]
        X = data.iloc[:, 0:]

        total = len(Y)
        print(f"Total items: {total}")
        correct = 0
        for i in range(total):
            content = X.iloc[i, 0]
            result = fn(content)
            #print(result, " for content: ", content)
            if result == Y.iloc[i, 0].strip():
                correct += 1

        print(f"Final Accuracy: {correct/total}")
