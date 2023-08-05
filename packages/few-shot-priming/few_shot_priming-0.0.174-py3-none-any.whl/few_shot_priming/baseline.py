import numpy as np
import torch
import random

from debater_python_api.api.debater_api import DebaterApi
from random import randint
from torch import nn
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertModel
from few_shot_priming.few_shot_stance import *

class Dataset(torch.utils.data.Dataset):
    def __init__(self,df, labels, path=None):
        if path:
            tokenizer = BertTokenizer.from_pretrained(path)
        else:
            tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        self.labels = [labels[label] for label in df["claims.stance"]]
        self.texts = []
        for i, record in df.iterrows():
            self.texts.append(tokenizer( record["topicText"], record['claims.claimCorrectedText'], padding="max_length", max_length=512,
                                        truncation=True, return_tensors="pt"))
        print(f"size of labels {len(self.labels)} and size of texts is {len(self.texts)}")

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        return self.texts[idx]
    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)
        return batch_texts, batch_y

class BertClassifier(nn.Module):
    def __init__(self, hyperparameters, path=None):
        super(BertClassifier, self).__init__()
        self.lr = hyperparameters["learning-rate"]
        self.head_size = hyperparameters["head-size"]
        self.batch_size = hyperparameters["batch-size"]
        self.linear = nn.Linear(768, self.head_size)
        self.classifier_head = nn.Linear(self.head_size, 1)
        if path:
            self.bert = BertModel.from_pretrained(path)
        else:
            self.bert = BertModel.from_pretrained('bert-base-cased')
        self.labels = {"CON": 0, "PRO":1}


    def forward(self, input_ids, mask):
        _, pooled_output = self.bert(input_ids=input_ids, attention_mask=mask, return_dict=False)
        linear_output = self.linear(pooled_output)
        head_output = self.classifier_head(linear_output)
        return head_output


def get_baseline_params():
    config = load_config()
    print(config)
    return config["baseline-params"]


def parse_args():
    """
    Parse the arguments of the scripts
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--random", action="store_true")
    parser.add_argument("--majority", action="store_true")
    parser.add_argument("--ibm-api", action="store_true")
    return parser.parse_args()

def run_finetuning_experiment_baseline(params=None, offline=True, validate=False):
    splits = load_splits()
    #splits["test"] = splits["test"].sample(10)
    use_cuda = torch.cuda.is_available()

    if use_cuda:
        print("-.-.-.- using cuda -.-.-.-.-")
    else:
        print("-.-..-. using cpu -.-.-.-.-..")

    path = None
    if offline:
        save_pre_trained_model()
        path = params["model-path"]

    if not params:
        params = get_baseline_params()
    else:
        print("params are input online")

    train_dataset = Dataset(splits["training"], {"PRO": 1, "CON": 0}, path=path)
    if validate:
        experiment_type = "validate"
        test_dataset = Dataset(splits["validation"], {"PRO": 1, "CON": 0}, path=path)
    else:
        experiment_type = "test"
        test_dataset = Dataset(splits["test"], {"PRO": 1, "CON": 0}, path=path)

    train_dataloader = DataLoader(train_dataset, batch_size=params["batch-size"], shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=params["batch-size"], shuffle=True)

    device = torch.device("cuda" if use_cuda else "cpu")


    bert = BertClassifier(params, path=path)
    if use_cuda:
        bert = bert.cuda()
        print("bert is on cuda")
    optimizer = AdamW(bert.parameters(), lr=float(params["learning-rate"]))
    epochs = params["epochs"]
    criterion = nn.BCEWithLogitsLoss().cuda()


    sigmoid = nn.Sigmoid()
    bert.train()
    metrics = {}
    for epoch in range(epochs):
        train_loss = 0
        all_test_labels = []
        all_test_preds = []
        for step, (train_input, train_label) in enumerate(train_dataloader):
            train_label = train_label.to(device)
            mask = train_input["attention_mask"].to(device)
            input_ids = train_input["input_ids"].squeeze(1).to(device)
            output = bert(input_ids, mask)
            batch_loss = criterion(output.squeeze(1), train_label.float())
            train_loss += batch_loss.item()
            batch_loss.backward()
            optimizer.step()
            metrics["train/loss"] = train_loss / (step +1)
            wandb.log(metrics)
        test_loss = 0
        for step, (test_input, test_labels) in enumerate(test_dataloader):
            test_labels = test_labels.to(device)
            mask = test_input["attention_mask"].to(device)
            input_ids = test_input["input_ids"].squeeze(1).to(device)
            output = bert(input_ids, mask)
            predictions = sigmoid(output.squeeze(1))
            print(predictions)
            predictions = [score > 0.5 for score in predictions.cpu().tolist()]
            all_test_preds.extend(predictions)
            all_test_labels.extend(test_labels.cpu().tolist())
            batch_loss = criterion(output.squeeze(1), test_labels.float())
            test_loss += batch_loss.item()
            metrics[f"{experiment_type}/loss"] = test_loss / (step+1)
            wandb.log(metrics)
        test_accuracy = accuracy_score(all_test_labels, all_test_preds)
        metrics[f"{experiment_type}/accuracy"] = test_accuracy
        wandb.log(metrics)
    metrics["score"] = metrics[f"{experiment_type}/accuracy"]
    wandb.log(metrics)
    return metrics["score"]


def baseline(params, offline=True, validate=True, majority=False):
    splits = load_splits()
    if validate:
        test_split = splits["validation"]
    else:
        test_split = splits["test"]

    if offline:
        save_pre_trained_model()
        path = params["model-path"]

    test_dataset = Dataset(test_split, {"PRO": 1, "CON": 0}, path=path)
    test_dataloader = DataLoader(test_dataset, batch_size=8, shuffle=True)
    predictions = []
    labels = []
    for step, (test_input, test_labels) in enumerate(test_dataloader):
        labels.extend(test_labels)
        if majority:
            predictions.extend([1 for _ in test_labels])
        else:
            predictions.extend([randint(0,1) for _ in test_labels])
    print(f"size of test is {test_labels}")
    return accuracy_score(labels,predictions)


def run_ibm_baseline(params, validate=True):
    splits = load_splits()
    if validate:
        test_split = splits["validation"]
    else:
        test_split = splits["test"]
    api_key = params["api-key"]
    debater_api = DebaterApi(api_key)
    pro_con_client = debater_api.get_pro_con_client()
    if validate:
        df_test = splits["validation"]
    else:
        df_test = splits["test"]
    list_of_instances = []
    for i, record in df_test.iterrows():
        list_of_instances.append({"sentence" : record['claims.claimCorrectedText'], "topic": record["topicText"]})
    scores = pro_con_client.run(list_of_instances)
    predictions = [score > 0 for score in scores]
    labels_map = {"PRO": 1, "CON": 0}
    labels = [labels_map[label] for label in test_split["claims.stance"]]

    return accuracy_score(labels, predictions)

if __name__ == "__main__":
    args = parse_args()
    params = get_baseline_params()
    if args.random:
        accuracy = baseline(params, offline=args.offline, validate=args.validate)
        print(f"accuracy of random baseline is {accuracy}")
    elif args.majority:
        accuracy = baseline(params, offline=args.offline, validate=args.validate, majority=True)
        print(f"accuracy of majority baseline is {accuracy}")
    elif args.ibm_api:
        accuracy = run_ibm_baseline(params, args.validate)
        print(f"accuracy of stance ibm api is {accuracy}")
    else:
        init_wandb(args.offline, params)
        run_finetuning_experiment_baseline(params, args.offline, args.validate)

