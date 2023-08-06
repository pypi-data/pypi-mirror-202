import torch
import os

from data.loader import load_data
from unwanted_content_detector.evaluator.evaluator import Evaluator

MODEL_NAME = "unwanted_detector_distilbert_04"

def train():
    # read data and apply one-hot encoding
    data = load_data()
    print(data)
    X = data.iloc[:,0]
    y = data.iloc[:,-1:]

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.4, random_state = 123)

    train_df = train_y.to_dict('records')
    train_X = train_X.to_list()
    for i in range(len(train_df)):
        tokenizer_result = tokenizer(train_X[i], truncation=True, padding=True)
        train_df[i] = { **train_df[i], **tokenizer_result}
        train_df[i]['text'] = train_X[i]
        train_df[i]['label'] = train_df[i]['label'].strip()
        train_df[i]['label'] = 1 if train_df[i]['label'].strip() == 'UNWANTED_CONTENT' else 0


    test_df = test_y.to_dict('records')
    test_X = test_X.to_list()
    for i in range(len(test_df)):

        tokenizer_result = tokenizer(test_X[i], truncation=True, padding=True)
        test_df[i] = { **test_df[i], **tokenizer_result}
        test_df[i]['text'] = test_X[i]
        test_df[i]['label'] = 1 if test_df[i]['label'].strip() == 'UNWANTED_CONTENT' else 0


    print(train_df[0])
    print(test_df[0])

    from transformers import DataCollatorWithPadding

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    import evaluate
    accuracy = evaluate.load("accuracy")
    import numpy as np


    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=labels)

    id2label = {0: "SAFE_CONTENT", 1: "UNWANTED_CONTENT"}
    label2id = {"UNWANTED_CONTENT": 0, "SAFE_CONTENT": 1}


    from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2, id2label=id2label, label2id=label2id
    )
    training_args = TrainingArguments(
        output_dir=MODEL_NAME,
        learning_rate=0.000005,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=70,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        push_to_hub=True,
    )
    # Logs evaluation accuracy
    # 70 epochs, 0.00005, accuracy = 87.%
    # 100 epochs, 0.00005, accuracy = 87%
    # 100 epochs, 0.000005, accuracy = 90%
    # 50 epochs, 0.000005, accuracy = 90%
    # 50 epochs, 0.0000005, accuracy = 70%
    # 100 epochs, 0.0000005, accuracy = 48%
    # 200 epochs, 0.0000005, accuracy = 61%
    # 300 epochs, 0.0000005, accuracy = 70%

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_df,
        eval_dataset=test_df,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,

    )

    trainer.train()
    evaluate = evaluate_with_model_and_tokenizer(model, tokenizer)


    Evaluator().evaluate_function(evaluate)

    os.system('du -h . | tail')

def evaluate_with_model_and_tokenizer(model, tokenizer):
    def evaluate(text):
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        return (model.config.id2label[predicted_class_id])
    return evaluate
