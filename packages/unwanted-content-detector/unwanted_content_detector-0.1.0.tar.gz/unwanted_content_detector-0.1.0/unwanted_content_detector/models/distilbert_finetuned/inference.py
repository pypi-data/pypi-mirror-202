# inspiration documentation https://huggingface.co/docs/transformers/tasks/sequence_classification
import torch

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from .train import MODEL_NAME, evaluate_with_model_and_tokenizer


class Inference():

    def __init__(self):
        print(f"Loading model {MODEL_NAME}")
        base_folder = '/Users/jean.machado/projects/unwanted_content_detector'
        self.model = AutoModelForSequenceClassification.from_pretrained( f"{base_folder}/" + MODEL_NAME, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(f"{base_folder}/" + MODEL_NAME, local_files_only=True)

    def infer(self, text):
        return evaluate_with_model_and_tokenizer(self.model, self.tokenizer)(text)



