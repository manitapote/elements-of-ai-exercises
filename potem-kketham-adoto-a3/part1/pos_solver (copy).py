###################################
# Your names and user ids:

# (Based on skeleton code by D. Crandall)
#
###################################


import random
import math
from operator import itemgetter

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    word = {}
    emission = {}
    transition = {}
    prob_speech = {}
    transitions = 0
    part_of_speech = {}
    initial_state_dist = {}
    
    
    #store each element is a dictionary having every POS as its key and values as a tuple containing total number of occurence
    #of key in training data and it's probability for that index of list.
    s = []

    #Returns a list having dictionary elements. Member dictionary elements have have values as tuple containing total
    # number of occurences of key in training data and it's probability.
    def prob(self,prior_data):
        for i in range(0,len(prior_data)):
            total = sum(prior_data[i].values())
            for key in prior_data[i].keys():
                prior_data[i][key] = (prior_data[i][key],prior_data[i][key] / total)
        return prior_data

    
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, algorithm, sentence, label):
        multiplcation = math.log(1)
        sum_all = 0
        for x in range(0, len(sentence)):
            emission_value = self.emission[(sentence[x], label[x])]
            if emission_value == 0:
                emission_value = 1e-10
            sum_all += emission_value * self.prob_speech[label[x]]
            multiplcation += math.log(emission_value * self.prob_speech[label[x]])
            result = multiplcation - math.log(sum_all)
        return result


   
    #Training
    def train(self, data):
        self.transition_matrix = {}
        self.emission = {}
        self.word = {}
        self.part_of_speech = {}
        self.transition_matrixs = 0

        for row in data:
            #loop through each word
            for x in range(0, len(row[0])):
                try:
                    t = self.s[x].get(row[1][x],0)
                    self.s[x][row[1][x]] = t + 1
                except IndexError:
                    self.s += [{row[1][x]:1.0}]
                    
                    
                #Counting frequency of each word
                if row[0][x] not in self.word:
                    self.word[row[0][x]] = 1.0
                else:
                    self.word[row[0][x]] += 1.0
                    
                    
                #Counting frequency of each POS
                if row[1][x] not in self.part_of_speech:
                    self.part_of_speech[row[1][x]] = 1.0
                else:
                    self.part_of_speech[row[1][x]] += 1.0
                    
                    
                #Counting frequency of each POS for appearing at the start of sentence
                if x == 0:
                    if row[1][x] not in self.initial_state_dist:
                        self.initial_state_dist[row[1][x]] = 1.0
                    else:
                        self.initial_state_dist[row[1][x]] += 1.0
                else:
                    inp_string = (row[1][x-1], row[1][x])

                    if inp_string not in self.transition_matrix:
                        self.transition_matrix[inp_string] = 1.0
                        self.transition_matrixs += 1.0
                    else:
                        self.transition_matrix[inp_string] += 1.0
                        self.transition_matrixs += 1.0
                        
                        
                #Counting frequency of each word with each POS as appearing in the sentences
                if (row[0][x], row[1][x]) not in self.emission:
                    self.emission[(row[0][x], row[1][x])] = 1.0
                else:
                    self.emission[(row[0][x], row[1][x])] += 1.0
                    
                    
        #Calculating emission probability
        for row in self.word.keys():
            for column in self.part_of_speech.keys():
                if (row, column) in self.emission:
                    self.emission[(row, column)] /= self.part_of_speech[column]
                    
                    
        #Calculating initial state distribution
        for x in self.part_of_speech.keys():
            self.initial_state_dist[x] /= len(data)
            
        #calculating probability of each POS in the data
        for x in self.part_of_speech.keys():
            self.prob_speech[x] = self.part_of_speech[x] / sum(self.part_of_speech.values())
            
        #calculating probability for each transition transition(state i-1, state i)
        for x in self.part_of_speech.keys():
            for y in self.part_of_speech.keys():
                if (x, y) not in self.transition_matrix:
                    self.transition_matrix[(x, y)] = 1e-10
                else:
                    self.transition_matrix[(x, y)] /= self.part_of_speech[x]
                    
        #If any word for a given position doesn't have some POS tagged in whole training data, we assume it to have
        #occured 0.00001 time.
        for index in range(0,len(self.s)):
            if len(self.part_of_speech.keys()) != len(self.s[index].keys()):
                for pos in set(self.part_of_speech.keys()) - set(self.s[index].keys()):
                    self.s[index][pos] = 0.00001
        self.s = self.prob(self.s)

    # Functions for each algorithm.
    def simplified(self, sentence):
        pos = None
        output_list = []
        for word in sentence:
            max_s = 0.0
            for speech in self.part_of_speech.keys():
                if (word, speech) not in self.emission:
                    prob_each = self.emission[(word, speech)] = 1e-10
                else:
                    prob_each = self.emission[(word, speech)] * self.prob_speech[speech]
                    
                #storing max probability and respective POS
                if prob_each > max_s:
                    max_s = prob_each
                    pos = speech
                    
            #if probability is zero then tag 'noun' POS
            if max_s is 0.0:
                pos = 'noun'
            output_list.append(pos)
        return output_list

    def complex_mcmc(self, sentence):
        #S is a list of length equal to total words in given sentence and it stores POS for each word in sentence.
        S = ['noun']*len(sentence)
        
        #samples stores each sample generated.
        samples = [S]
        sample_threshold = 5
        
        #To discard initial 10 samples we are sampling total sample_threshold+10 samples
        for n in range(0,sample_threshold + 10):
            for i in range(0,len(S)):
                
                #Stored the probablity distribution for each for each POS
                s1_prob_dist = []
                s1_pos = []
                
                #for 1st word
                if i==0:
                    
                    #Sampling over all possible POS for given position and taking probability of each
                    for pos in self.prob_speech.keys():
                        #If any of the probability can not be derived training dataset, we take it as 0.001 and we do
                        try:
                            #S1: P(s_1)*P(s_2 | S_1)*P(w_1 | S_1).
                            #self.s = [{pos: (pos_count,pos_prob}]
                            s1_prob_dist += [self.s[0][pos][1]*self.transition_matrix.get((pos,S[1]),0.001)*self.emission.get((sentence[0],pos),0.001)]
                            s1_pos += [pos]
                        except IndexError:
                            #Exception for a sentence with single word
                            s1_prob_dist += [self.s[0][pos][1]*self.emission.get((sentence[0],pos),0.001)]
                            s1_pos += [pos]
                            
                #For last word
                elif i== len(S)-1:
                    for pos in self.prob_speech.keys():
                        s1_prob_dist += [self.transition_matrix.get((S[i-1],pos),0.001)*self.emission.get((sentence[-1],pos),0.001)]
                        s1_pos += [pos]
                else:
                    for pos in self.prob_speech.keys():
                        s1_prob_dist += [self.transition_matrix.get((S[i-1],pos),0.001)*self.transition_matrix.get((pos,S[i+1]),0.001)*self.emission.get((sentence[i],pos),0.001)]
                        s1_pos += [pos]
                temp = 0.0
                
                #doing normalization and also randomaly generating probability and assigning appropriate POS from CPT
                #generated from samples
                rand_temp = random.random()
                for j in range(0,len(s1_prob_dist)):
                    temp += s1_prob_dist[j]/sum(s1_prob_dist)
                    if rand_temp <= temp:
                        S[i] = s1_pos[j]
                        break
            samples += [S]
        temp = []
        
        #Calculating th maximum pos for each word
        labels = []
        
        for i in samples[-sample_threshold:]:
            temp.append(i)
        
        for i in range(len(samples[-1])):
            tmep_1 = list( map(itemgetter(i), temp ))
            pos = max(tmep_1, key=tmep_1.count)
            labels.append(pos)
        
        return labels

    def hmm_viterbi(self, sentence):
        output_list = []
        
        #dictioanary for saving value for states
        v = {}
        
        #dictionary for saving POS tag while calculating maximum probability for each state
        sequence = {}
        
        #finding values for state 0 for each POS for first word of the sequence
        for speech in self.part_of_speech.keys():
            if (sentence[0], speech) not in self.emission:
                self.emission[(sentence[0], speech)] = 0.001
            prob = self.initial_state_dist[speech] * self.emission[(sentence[0], speech)]
            v[(speech, 0)] = prob
            
        #finding value for each state
        for x in range(1, len(sentence)):
            for speech1 in self.part_of_speech.keys():
                max_prob = 0.0
                max_speech = None
                for speech2 in self.part_of_speech.keys():
                    prob = v[(speech2, x-1)] * self.transition_matrix[(speech2, speech1)]
                    if prob > max_prob:
                        max_prob = prob
                        max_speech = speech2
                        
                #if probability is zero then tag 'noun' POS
                if max_prob == 0:
                    max_prob = 0.01
                    max_speech = 'noun'
                v[(speech1, x)] = self.emission[(sentence[x], speech1)] * max_prob
                
                #storing POS with maximum probability for the state
                sequence[(speech1, x)] = max_speech
                
        tn = len(sentence) - 1
        max = 0.0
        
        #finding maximum probability for last state
        for speech in self.part_of_speech.keys():
            if v[(speech, tn)] > max:
                max = v[(speech, tn)]
                max_speech = speech
        output_list.append(max_speech)
        tn = len(sentence)
        
        #Backtracking the values of POS from last state to first by getting saved tag while finding maximum prob. of each state
        # with some POS
        for x in range(0, tn-1):
            speech = sequence[(max_speech, tn - x - 1)]
            max_speech = speech
            output_list.append(speech)

        output_list.reverse()
        return output_list


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
