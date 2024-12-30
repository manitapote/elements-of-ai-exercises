
import math
import random
import numpy as np
from collections import Counter

class Solver:
    def __init__(self):
        self.word_matrix = {}
        self.transition_matrix = {}
        self.training_length = 0
        self.hmm_v = []
        self.probability_matrix = {}
        self.part_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        self.s0 = 's0'
        self.s1 = 's1'
        self.w = 'w'
        self.num_words = 0
        self.mcmc_prob = []

        
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            sum_all = 0
            
            for word in sentence:
                if word not in self.word_matrix:
                    continue
                sum_all += -math.log(max(self.word_matrix[word]['pos'].values())/self.word_matrix[word]['count'])
                
            return sum_all
        elif model == "HMM":
            sum_all = 0
            
            for value in self.hmm_v:
                if value == 0:
                    continue
                sum_all += -math.log(value)
                
            self.hmm_v = []
            
            return sum_all
        elif model == "Complex":
            return -999
        else:
            print("Unknown algo!")

    # Do the training!

    def train(self, train_data):
        data = []
        self.word_matrix = {}
        self.transition_matrix = {}
        self.length = len(train_data)
        self.probability_matrix = {}

        for row in train_data:
            for i in range(len(row[0])):
                #conditions for word count matrix
                if row[0][i] not in self.word_matrix:
                    self.word_matrix[row[0][i]] = {
                        'pos':{row[1][i]:1},
                        'count': 1,
                    }   
                else:
                    if row[1][i] not in self.word_matrix[row[0][i]]['pos']:
                        self.word_matrix[row[0][i]]['pos'][row[1][i]] = 1
                    else:
                        self.word_matrix[row[0][i]]['pos'][row[1][i]] += 1
                    
                    
                    self.word_matrix[row[0][i]]['count'] += 1
                    
                #Conditions for transition matrix
                if row[1][i] in self.transition_matrix:
                    self.transition_matrix[row[1][i]]['count'] += 1
                else:
                    self.transition_matrix[row[1][i]] = {
                                            'pos':{row[1][i]: 0},
                                            'start': 0,
                                            'end': 0,
                                            'count': 1}
                if i == (len(row[1]) - 1):
                    self.transition_matrix[row[1][i]]['end'] += 1
                    break
                if i == 0:
                    self.transition_matrix[row[1][i]]['start'] += 1
                if row[1][i+1] in self.transition_matrix[row[1][i]]['pos']:
                    self.transition_matrix[row[1][i]]['pos'][row[1][i+1]] +=1
                else:
                    self.transition_matrix[row[1][i]]['pos'][row[1][i+1]] = 1
                    
                
                #probabilites for mcmc
                word = row[0][i]
                current_pos = row[1][i]
                
                for pos in self.part_speech:
                    for pos in self.part_speech:
                        self.probability_matrix[pos] = {}
                    
                    
                if i == 0:
                    initial_choice = random.choice(self.part_speech)
                    self.probability_matrix[word] = {initial_choice: {current_pos: 1}}
                    continue
               
                previous_pos = row[1][i-1]
                
                
                if word not in self.probability_matrix:
                    self.probability_matrix[word] = {previous_pos: {current_pos: 1}}
                else:
                    if previous_pos in self.probability_matrix[word]:
                        if current_pos in self.probability_matrix[word][previous_pos]:
                            self.probability_matrix[word][previous_pos][current_pos] += 1
                        else:
                            self.probability_matrix[word][previous_pos][current_pos] = 1
                
                self.num_words += 1
                        
    def simplified(self, sentence):
        result = []
        
        for word in sentence:
            if word in self.word_matrix:
                result.append(max(self.word_matrix[word]['pos'], key=self.word_matrix[word]['pos'].get))
            else:
                result.append('x')
                
        return result

    def hmm_viterbi(self, sentence):
        if len(sentence) == 1:
            self.hmm_v.append(max(self.word_matrix[sentence[0]]['pos'].values())/self.word_matrix[sentence[0]]['count'])
            
            return [max(self.word_matrix[sentence[0]]['pos'], key=self.word_matrix[sentence[0]]['pos'].get)]

        
        result = []
        v = {}
        path = []
        
        for word in sentence:
            if word not in self.word_matrix:
                self.word_matrix[word] = {
                    'pos': {key: 1e-5 for key in self.transition_matrix.keys()},
                    'count': 1
                }
                
                v[word] ={key: 1 for key in self.transition_matrix.keys()}
            else:
                v[word] = {word_pos: self.transition_matrix[word_pos]['start'] / 
                             self.length *
                             self.word_matrix[word]['pos'][word_pos] /
                             self.transition_matrix[word_pos]['count']
                             for word_pos in self.word_matrix[word]['pos']}
        
        for i in range(1, len(sentence)):
            temp = []
            
            path.append([sentence[i], {}])
    
            for next_pos in self.word_matrix[sentence[i]]['pos']:
                temp_path = ''
                max_value = -1
                             
                for previous_pos in self.word_matrix[sentence[i-1]]['pos']:
                    if next_pos not in self.transition_matrix[previous_pos]['pos']:
                        self.transition_matrix[previous_pos]['pos'][next_pos] = 0

                    value = v[sentence[i-1]][previous_pos] * self.transition_matrix[previous_pos]['pos'][next_pos] 
                    value = value / self.transition_matrix[previous_pos]['count']
                    vaue = value * self.word_matrix[sentence[i]]['pos'][next_pos] 
                    value = value / self.transition_matrix[next_pos]['count']
                    
                    if value > max_value:
                        max_value = value
                        temp_path = previous_pos
                
                path[i-1][1][next_pos] = [temp_path, next_pos, max_value]
                v[sentence[i]][next_pos] = max_value
        
        actual_path = []
        v_max = -1
        last_max = ''
        
        for value in path[-1][-1]:
            if v_max < path[-1][-1][value][-1]:
                v_max = path[-1][-1][value][-1]
                last_max = path[-1][-1][value][1]
                search = path[-1][-1][value][0]
        
        self.hmm_v.append(v_max)
        actual_path.append(last_max)
        actual_path.insert(0, search)
        
        for item in reversed(path[:-1]):
            self.hmm_v.append(item[1][search][-1])
            search = item[1][search][0]
            actual_path.insert(0, search)

        self.hmm_v.append(v[sentence[0]][actual_path[0]])
                
        return actual_path
    
    
    
    def conditional_prob(self, conditioned_var, new_sample):
        joint_probs = {}
        
        for v in self.part_speech:
            new_sample.update({conditioned_var: v})
            joint_probs[v] = self.joint_prob(new_sample)
            
        sum_all = sum(joint_probs.values())
        distro = {}
        
        for v in self.part_speech:
            k = float(joint_probs[v])/sum_all if  sum_all != 0 else 0
            distro[v] = k

        return distro

    def complex_mcmc(self, sentence):
        return ['noun']*len(sentence)
        s = random.choice(self.part_speech)
        s1 = random.choice(self.part_speech)
        
        iterations = 10000
        probable_sequence = []
        self.mcmc_prob = []
        
        for word in sentence:
            samples = [{self.s0:s, self.s1:s1, self.w:word }]
            count = []
            
            for i in range(iterations):
                new_sample = samples[-1].copy()

                for var in [self.s0, self.s1]:
                    new_sample.pop(var)
                    distro_var = self.conditional_prob(var, new_sample)
                    chosen_pos = self.sample(distro_var)
                    new_sample.update({var: chosen_pos})
            
                    samples.append(new_sample)
                    
                    
                    count.append[new_sample[self.s0], new_sample[self.s1]]
            
            probable_sequence.append(word_pos)
            self.mcmc_prob.append(max_pos)
                
        return probable_sequence


    
    def sample(self, distro):
        dist=list(distro.items())
        return np.random.choice([dist[i][0] for i in range(len(dist))],p=[dist[i][1] for i in range(len(dist))])
    
    def joint_prob(self, sample):
        (s0, s1, w) = sample[self.s0], sample[self.s1], sample[self.w]
        p = self.transition_matrix[s0]['count'] / self.num_words 
        
        if s1 in  self.transition_matrix[s0]['pos']:
            p = p * self.transition_matrix[s0]['pos'][s1] / self.transition_matrix[s0]['count']
        else:
            return 0
        
        k = 1
        
        if w in self.probability_matrix:
            if s0 in self.probability_matrix[w] and s1 in self.probability_matrix[w][s0]:
                k = self.probability_matrix[w][s0][s1]/self.transition_matrix[s0]['pos'][s1]
            
        p = p * k
    
        return p
    
    
#     def complex_mcmc(self, sentence):
#         samples = []
#         count_pos = []
#         #        sample = ["noun"] * len(words)  # initial sample, all tags are nouns
#         sample = self.simplified(sentence) # here I use the answer from the simplified model as the initial
#         iterations= 1500 # total number of iterations, can be changed according to the initial sample and observations
#         threshold = 20

#         for i in range(iterations):
#             sample = self.get_sample(sentence, sample)
        
#             if i >= threshold:
#                 samples.append(sample)

#             for i in range(len(sentence)):
#                 count = {}
#                 for sample in samples:
#                     if sample[i] in count:
#                         count[sample[i]] += 1
#                     else:
#                         count[sample[i]] = 1
#             count_pos.append(count_tags)

#         chosen_pos = [max(count_pos[i], key = count_pos[i].get) for i in range(len(sentence))]
#         return chosen_pos
    
    
#     def get_sample(self, sentence, sample):
#         for i in range(len(sentence)):
#             prob = [0] * len(self.part_speech)
            
#             for j in range(len(self.part_speech)):
#                 sample[i] = self.part_speech[j]
#                 prob[j] = self.calc_prob(sentence, sample)
                
#             print('probability ', prob)
                
#             sum_all = sum(prob)
#             normalized_prob = [x/sum_all for x in prob]
            
#             new_choice = np.random.choice([self.speech_pos],p=normalized_prob)
#             sample[i] = new_choice
            
#         print('final sample ', sample)
        
#         return sample
        
    
#     def calc_prob(self, sentence, sample):
# #         s0 = self.transition_matrix[sample[0]]['count'] / self.num_words
#         sum_all = 0
        
#         for i in range(len(sample)):
#             print(sentence[i], '  word')
#             print(sample[i], ' sample pos')
#             print(self.word_matrix[sentence[i]])
            
#             print('Transition matrix  ', self.transition_matrix[sample[i]])
#             if sentence[i] not in self.word_matrix:
#                 return 0
            
#             if sample[i] not in self.word_matrix[sentence[i]]['pos']:
#                 return 0
            
    
#             sum_all = math.log(self.word_matrix[sentence[i]]['pos'][sample[i]]/self.transition_matrix[sample[i]]['count'], 10)
            
#             if i != 0:
#                 if sample[i] not in self.transition_matrix[sample[i-1]]['pos']:
#                     return 0
                
#                 sum_all = sum_all +  math.log(self.transition_matrix[sample[i-1]]['pos'][sample[i]]/self.transition_matrix[sample[i-1]]['count'], 10)
            
#             if i != 0 and i != 1:
#                 if sentence[i] not in self.probability_matrix:
#                     return 0
                
#                 if sample[i-1] not in self.probability_matrix[sentence[i]]:
#                     return 0
                
#                 if sample[i] not in self.probability_matrix[sentence[i]][sample[i-1]]:
#                     return 0
                
#                 if sample[i] not in self.transition_matrix[sample[i-1]]['pos']:
#                     return 0
                
#                 sum_all = sum_all + math.log(self.probability_matrix[sentence[i]][sample[i-1]][sample[i]]/self.transition_matrix[sample[i-1]]['pos'][sample[i]], 10)
            
#             if i == 0:
#                 sum_all = sum_all + math.log(self.transition_matrix[sample[i]]['count'] / self.num_words)
                
#         return sum_all

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
#         print(sentence)
#         return
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
        
