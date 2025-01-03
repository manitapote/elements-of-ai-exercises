###################################
# CS B551 Spring 2021, Assignment #3
# D. Crandall
#
# There should be no need to modify this file.
# Edit pos_solver.py instead!
#
# To get started, try running: 
#
#   python3 ./label.py bc.train bc.test.tiny
#

from pos_scorer import Score
from collections import Counter
import itertools
import operator
# sys.meta_path.append(NotebookFinder())
from pos_solver import *
import sys

# Read in training or test data file
#
def read_data_train(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        
        exemplars += [ (data[0::2], data[1::2]), ]
#         exemplars += list(zip(*(iter(data),)*2))
        
#         break

    return exemplars

def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        
        exemplars += [ (data[0::2], data[1::2]), ]

    return exemplars


####################
# Main program
#

if len(sys.argv) < 3:
    print("Usage: \npython3 ./label.py training_file test_file")
    sys.exit()

(train_file, test_file) = sys.argv[1:3]

# train_file = 'bc.train'
# test_file = 'bc.test'


print("Learning model...")
solver = Solver()
train_data = read_data_train(train_file)
# print(exemplars)



# print(train_data)
solver.train(train_data)
#
print("Loading test data...")
test_data = read_data(test_file)
# print(test_data)
print("Testing classifiers...")
scorer = Score()
# print(solver.S_W['the'])
#
Algorithms = ("Simple", "HMM", "Complex")
Algorithm_labels = [ str(i+1) + ". " + Algorithms[i] for i in range(0, len(Algorithms) ) ]
for (s, gt) in test_data:
# #
    outputs = {"0. Ground truth" : gt}

    # run all algorithms on the sentence
    for (algo, label) in zip(Algorithms, Algorithm_labels):
        outputs[label] = solver.solve(algo, s)

    # calculate posteriors for each output under each model
    posteriors = { o: { a: solver.posterior( a, s, outputs[o] ) for a in Algorithms } for o in outputs }
    Score.print_results(s, outputs, posteriors, Algorithms)

    scorer.score(outputs, gt)
    scorer.print_scores()

    print("----")
# #     break

