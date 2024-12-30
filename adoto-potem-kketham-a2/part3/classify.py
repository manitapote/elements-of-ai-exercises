# classify.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE : { Kethamakka.Karthikeya-kketham,Andrew Doto-adoto,Manita Pote-potem }
#
# Based on skeleton code by D. Crandall, March 2021
#
# Some parts of the code were inspired from https://github.com/aishajv/Unfolding-Naive-Bayes-from-Scratch/blob/master/%23%20Unfolding%20Na%C3%AFve%20Bayes%20from%20Scratch!%20Take-2%20%F0%9F%8E%AC.ipynb


import sys
import pandas as pd
import numpy as np
from collections import defaultdict
import re


def preprocess_string(str_data):
    result = re.sub('[^a-z\s]+', ' ', str_data, flags=re.I).lower()
    return result


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to documents
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each document
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classloader for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

class NaiveBayes:

    def __init__(self):
        self.labels = np.array(train_data["labels"])
        self.texts = np.array(train_data["objects"])
        self.wrd_bag = np.array([defaultdict(int) for index in range(len(train_data["classes"]))])
        self.classes = np.array(train_data["classes"])
        self.test_text = np.array(test_data["objects"])

    def bag_of_words(self, text, index):
        text = text[0]
        k = text.split()
        for word in k:
            if word not in k:
                self.wrd_bag[word] = 0
                self.wrd_bag[index][word] = self.wrd_bag[index][word] + 1
            else:
                self.wrd_bag[index][word] = self.wrd_bag[index][word] + 1

    def train(self, text, labels):
        prob_classes = [0, 0]
        l_wrd_cnts = [0, 0]
        k = self.labels
        wrd_vocab = np.unique(np.array(train_data["objects"]))

        for item, countt in enumerate(train_data["classes"]):
            labels = self.texts[k == countt]
            prep_texts = [preprocess_string(labels_text) for labels_text in labels]
            prep_texts = pd.DataFrame(data=prep_texts)
            np.apply_along_axis(self.bag_of_words, 1, prep_texts, item)
            prob_classes[item] = np.sum(k == countt) / float(k.shape[0])
            l_wrd_cnts[item] = np.sum(
                np.array(list(self.wrd_bag[item].values()))) + 1
        denom = np.array([l_wrd_cnts[item] + wrd_vocab.shape[0] + 1 for item, countt in
                          enumerate(train_data["classes"])])

        self.train_set = np.array([(self.wrd_bag[item], prob_classes[item], denom[item]) for
                                   item, countt in
                                   enumerate(train_data["classes"])])

    def prob(self, test_message):
        l_prob = [0, 0]
        p_prob = [0, 0]

        for item, countt in enumerate(test_data["classes"]):
            k = test_message.split()
            for wrd in k:
                test_wrd_counts = self.train_set[item][0].get(wrd, 0) + 1
                test_wrd_prob = test_wrd_counts / float(self.train_set[item][2])
                l_prob[item] = l_prob[item] + np.log(test_wrd_prob)
            p_prob[item] = l_prob[item] + np.log(self.train_set[item][1])
        return p_prob

    def test(self, test_data):
        pred = []
        for i in test_data:
            prep_text = preprocess_string(i)
            posterier_prob = self.prob(prep_text)
            key = np.argmax(posterier_prob)
            n = self.classes[key]
            pred.append(n)
        op = np.array(pred)
        return op


def classifier(train_data, test_data):
    clf = NaiveBayes()
    clf.train(train_data["objects"], train_data["labels"])
    predict = clf.test(test_data["objects"])
    return predict


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)

    test_data = load_file(test_file)

    if (train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
